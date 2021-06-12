package ChatBot;

import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.tokenize.SimpleTokenizer;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@RestController
public class Comm {
    private static String  	sResponse = new String("");
    private static GraphDatabaseFactory dbFactory = new GraphDatabaseFactory();
    private static GraphDatabaseService db = dbFactory.newEmbeddedDatabase(new File("J:/FYP2/neo4j-extraction_test/data/databases/graph.db"));
    ArrayList<String> answer_message=new ArrayList<String>();
    @GetMapping("/getdata")
    public String getdata(@RequestParam("question") String question){
        System.out.println(question);
        return question+"aaa";
    }

    @GetMapping("/postdata")
    public String postdata(@RequestParam("question") String question){
        setMessage(question);
        try{
            Thread thread = Thread.currentThread();
            thread.sleep(5000);
        }catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        System.out.println("---------------------"+answer_message);
        return (String) answer_message.toArray()[0];
    }
    public void setMessage(String message){
        try {
            if(get_input(message)!=null) {
                answer_message = get_input(message);
            }
            else{ //User end the chat proactively
                System.exit(0);
            }
        }
        catch(Exception e) {
            e.printStackTrace();
        }
//        sResponse = sResponse.substring(0,sResponse.length()-4); //remove the line break in the end of sentence
//        sResponse = "";
    }
    static String keywords[][][]={
            {{  "What is the definition of", "what is the definition of",
                "What is the meaning of", "what is the meaning of",
                "What is", "what is",
                "How xxx work", "how xxx work",
                "Can you explain", "can you explain",
                "Could you explain", "could you explain",
                "Can you explain what is", "can you explain what is",
                "Can you tell me what is", "can you tell me what is",
                "Can you tell me", "can you tell me",
                "Can you tell me what is the definition of", "can you tell me what is the definition of",
                "Can you explain what is the definition of", "can you explain what is the definition of",
            },
                    {"example"}
            },
            {{  "How xxx works", "how xxx works",
                "How xxx work", "how xxx work",
                "How do xxx work", "how do xxx work",
                "How does xxx work", "how does xxx work",
                "How a computer understand and process xxx","how a computer understand and process xxx",
            },
                    {"method"}
            },
            {{  "Why the", "why the",
                "What is the reason of", "what is the reason of",
                "Why the xxx is xxx", "why the xxx is xxx",
                "Can you explain why", "can you explain why",
            },
                    {"reason"}
            },
            {{  "Who develop xxx", "who develop xxx",
                "Who is the developer of xxx", "who is the developer of xxx",
                "What works has published by", "what works has published by",
                "What works has developed by","what works has developed by",
                "What works has proposed by", "what works has proposed by",
            },
                    {"developer"}
            },
            {{  "How to express xxx", "how to express xxx",
            },
                    {"use_to"}
            },
            {{  "What is xxx used to do", "what is xxx used to do",
                "What can xxx do", "what can xxx do",
                "What can be the xxx used to", "what can be the xxx used to",
            },
                    {"use_to"}
            },
            {{  "What are the contents of","what are the contents of",
                "How many types of", "how many types of",
                "What is the main components of xxx", "what is the main components of xxx",
            },
                    {"contain"}
            },
            {{  "What is the drawback of", "what is the drawback of",
                "What is the con of", "what is the con of",
                "What is the limitation of", "what is the limitation of"
            },
                    {"drawback"}
            }
    };
    static int positionI;
    static int positionJ;
    public static ArrayList<String> get_input(String sInput) {
        //System.out.print("&gt");
        //System.out.println(sInput);
        if(sInput.indexOf("BYE") == 0){
            return null;
        }
        String tokens[] = tokenization(sInput);
        Stream<String> steam1 = Arrays.stream(tokens);
        String tags[] = POSTagging(tokens);
        for (String tag : tags) {
            System.out.print(tag + " ");
        }
        ArrayList<String> entityList = filterEntity(tokens, tags);
        String[] entity = (String[]) entityList.toArray(new String[0]);
        String searchEntity = new String();
        for (int i = 0; i < entity.length; i++) {
            System.out.println(entity[i]);
            if (i == 0) {
                searchEntity = searchEntity + entity[i];
            } else {
                searchEntity = searchEntity + " " + entity[i];
            }

        }
        String relation = filter_question_type(sInput);
        String complex_entity=filter_hard_question(sInput);
        ArrayList<String> answer=new ArrayList<String>();
        answer = match_answer(db, searchEntity, complex_entity,relation);
        return answer;
    }
    /*
     * This function is used to filter the hard structure question
     * @param sInput: the string which users enter
     * @Return input: the entity which has been extracted
     */
    public static String filter_hard_question(String sInput){
        String input=sInput.replace(keywords[positionI][0][positionJ],"");
        input=input.replace("?","");
        input=input.trim();
        return input;
    }

    /*
     * This function is used to match the answer from the database
     * @param db: the neo4j database service
     * @param entity: the string of the entity you want to search
     * @param complex_entity: the string of entity in complex structure of sentence
     * @param relation: the relation you want to match*/
    public static ArrayList<String> match_answer(GraphDatabaseService db, String entity, String complex_entity, String relation){
        try(Transaction tx=db.beginTx()){
            /*-----Get Definition--------------*/
            System.out.println("searchEntity: "+entity);
            System.out.println("complex_entity: " + complex_entity);
            StringBuilder sb = new StringBuilder();
            sb.append("MATCH (n1) WHERE n1.name=~" + "\"" + "(?i)" + entity + "\"");
            sb.append("MATCH p=(n1)-[r]->(n2) WHERE type(r)=" + "\"" + relation + "\"");
            sb.append("RETURN n1.definition");
            Result definition = db.execute(sb.toString());
            StringBuilder sb_complex = new StringBuilder();
            sb_complex.append("MATCH (n1) WHERE n1.name=~" + "\"" + "(?i)" + complex_entity + "\"");
            sb_complex.append("MATCH p=(n1)-[r]->(n2) WHERE type(r)=" + "\"" + relation + "\"");
            sb_complex.append("RETURN n1.definition");
            Result complex_definition = db.execute(sb_complex.toString());
            String answer = null;
            ArrayList<String> result=new ArrayList<String>();
            if (definition.hasNext() == false && complex_definition.hasNext() == false) {
                System.out.println("Sorry, I don't know.");
            }
            else if (definition.hasNext() == true && complex_definition.hasNext() == false){
                while (definition.hasNext()) {
                    answer = definition.next().get("n1.definition").toString();
                    result.add(answer);
                    System.out.println(answer);
                }
            }
            else if (definition.hasNext() == false && complex_definition.hasNext() == true) {
                while (complex_definition.hasNext()) {
                    answer = complex_definition.next().get("n1.definition").toString();
                    result.add(answer);
                    System.out.println(answer);
                }
            }
            tx.success();
            if (result.toArray().length>0){
                return result;
            }
            else{
                ArrayList<String> result2=new ArrayList<String>();
                result2.add("Sorry, I do not know. Do you ask: \"What is the definition?\"");
                return result2;
            }
        }
    }

    /*
     * This function is used to match the question type
     * @param String sInput: the input question
     * @Return relationship: the string of the name of the question type
     */
    public static String filter_question_type(String sInput){
        positionI=0;
        positionJ=0;
        double sim=0.0;
        double tempSim=0.0;
        String questionType=null;
        for(int i = 0; i < keywords.length; ++i)
        {
            String[] keyWordList = keywords[i][0];
            String[] relation=keywords[i][1];

            for(int j = 0; j < keyWordList.length; ++j)
            {
                String keyWord = keyWordList[j];
                sim=calculateCosine(sInput,keyWord);
                if(sim>tempSim){
                    tempSim=sim;
                    questionType=relation[0];
                    positionI=i;
                    positionJ=j;
                    //System.out.println(sim+": "+questionType);
                }
            }
        }
        System.out.println(tempSim+" "+questionType);
        //System.out.println(keywords[0][0][1]);
        return questionType;
    }
    /*
     * This function is used to calculate cosine similarity between sentences
     * @param s1: the first sentence
     * @param s2: the second sentence
     * @Return double: return the cosine similarity of two sentences
     */
    public static double calculateCosine(String s1, String s2){
        //split the sentence into words, which means tokenization
        Stream<String> stream1=Stream.of(s1.toLowerCase().split("\\W+")).parallel();
        Stream<String> stream2=Stream.of(s2.toLowerCase().split("\\W+")).parallel();
        //Get the frequency of words in each sentence
        Map<String,Long> wordFreq1=stream1.collect(Collectors.groupingBy(
                String::toString, Collectors.counting()));
        Map<String,Long> wordFreq2=stream2.collect(Collectors.groupingBy(
                String::toString, Collectors.counting()));
        //remove the duplicated words
        Set<String> wordSet1=wordFreq1.keySet();
        Set<String> wordSet2=wordFreq2.keySet();
        //create a set which contains the common string
        Set<String> intersection=new HashSet<String>(wordSet1);
        intersection.retainAll(wordSet2);

        //calculate the numerator
        double numerator = 0;
        for (String common: intersection){
            numerator += wordFreq1.get(common) * wordFreq2.get(common);
        }

        //calculate the denominator
        double param1 = 0, param2 = 0;
        for(String w1: wordSet1){
            param1 += Math.pow(wordFreq1.get(w1), 2);
        }
        param1 = Math.sqrt(param1);

        for(String w2: wordSet2){
            param2 += Math.pow(wordFreq2.get(w2), 2);
        }
        param2 = Math.sqrt(param2);

        double denominator = param1 * param2;
        double cosineSimilarity = numerator/denominator;
        return cosineSimilarity;
    }

    /*
     * This function is used to filter the entity in the quesion
     * @param tokens: the String array of tokens
     * @param tags: the Sting array of tags
     * @Return EntityList<>: Return arraylist of string which contains the entities which are filtered
     */
    public static ArrayList<String> filterEntity(String[] tokens, String[] tags){
        //String[] EntityList={};
        ArrayList<String> EntityList=new ArrayList<String>();
        for(int i=0;i< tokens.length;i++){
            if(tags[i].equals("NN") || tags[i].equals("NNP") || tags[i].equals("NNPS") || tags[i].equals("NNS") || tokens[i].equals("in") || tokens[i].equals("knowledge") || tokens[i].equals("Knowledge") ||tokens[i].equals("top") ||tokens[i].equals("Top")||tokens[i].equals("-")||tokens[i].equals("domain")||tokens[i].equals("Domain")||tokens[i].equals("engineer")||tokens[i].equals("computational")||tokens[i].equals("lexical")
                    || tokens[i].equals("search")|| tokens[i].equals("hidden")|| tokens[i].equals("natural")
            ){
                if(tokens[i].equals("works") || tokens[i].equals("work") || tokens[i].equals("mean") || tokens[i].equals("means")|| tokens[i].equals("definition")|| (tokens[i].equals("is")&&tokens[i+1].equals("popular"))
                        || (tokens[i-1].equals("is")&&tokens[i].equals("popular"))|| tokens[i].equals("components")|| tokens[i].equals("limitation")){
                    continue;
                }
                else{
                    EntityList.add(tokens[i]);
                }
            }
        }
        return EntityList;
    }

    /*
     * This function is used to tokenize the sentence
     *  @Param sentence: A string which store sentences
     *  @Return tokens[]: An array which store each token of each word in each sentence*/
    public static String[] tokenization(String sentence){
        //Tokenization step
        SimpleTokenizer simpleTokenizer=SimpleTokenizer.INSTANCE;
        String tokens[]=simpleTokenizer.tokenize(sentence);
        return tokens;
    }

    /*
     * This function is used to POS tag
     * @Param tokens[]: An array which store each token of word in sentences
     * @Return tags[]: An array which store the tag of each word
     */
    public static String[] POSTagging(String[] tokens){
        String tags[]=null;
        //POS tag
        try(InputStream modelIn=new FileInputStream(new File("J:/FYP/NLP_Bin_file/","en-pos-maxent.bin"));){
            POSModel model=new POSModel(modelIn);
            POSTaggerME tagger=new POSTaggerME(model);
            tags=tagger.tag(tokens);
        }catch(IOException ex){
            ex.printStackTrace();
        }
        return tags;
    }
}
