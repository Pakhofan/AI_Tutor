package src.main.java.ChatBat;

import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.tokenize.SimpleTokenizer;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Model {
    private int counter;
    private ArrayList<ModelListener> listeners;
    private String new_message[] = new String[100];
    ArrayList<String> answer_message=new ArrayList<String>();
    private static String  	sResponse = new String("");
    private static GraphDatabaseFactory dbFactory = new GraphDatabaseFactory();
    private static GraphDatabaseService db = dbFactory.newEmbeddedDatabase(new File("J:/FYP/neo4j-community-3.5.21-windows/neo4j-community-3.5.21/data/databases/graph.db"));
    public Model() {
        counter = 0;
        listeners = new ArrayList<ModelListener>();
    }
    public void addListener(ModelListener l) {
        listeners.add(l);
    }
    public int getCounter() {
        return counter;
    }
    public void setCounter(int counter) {
        this.counter = counter;
        notifyListeners(); // Counter changed so notify the listeners.
    }
    public String[] getMessage(){
        return new_message;
    }
    public void setMessage(String message){
        int i = 0;
        while(new_message[i]!=null){
            i++;
        }
        this.new_message[i] = "<div style='color:red'>User:</div>" + message;
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
        for(int index=0;index<answer_message.toArray().length;index++) {
            sResponse = sResponse + answer_message.toArray()[index] + "<br>";
        }
        sResponse = sResponse.substring(0,sResponse.length()-4); //remove the line break in the end of sentence
        this.new_message[i + 1] = "<div style='color:blue'>Christopher:</div>" + sResponse;
        sResponse = "";
        notifyListeners(); // Counter changed so notify the listeners.
    }
    private void notifyListeners() {
        for(ModelListener l: listeners) {
            l.update(); // Tell the listener that something changed.
        }
    }

    static String keywords[][][]={
            {{"What is","What is the definition of","What is the meaning of","What is xxx mean?"},
                    {"definition"}
            },
            {{"How a computer understand and process xxx"},
                    {"reason"}
            },
            {{"How xxx works", "How xxx work","How do xxx work", "How does xxx work"},
                    {"method"}
            },
            {{"How to express xxx"},
                    {"use_to"}
            },
            {{"Why the","What is the reason of","Why the xxx is xxx"},
                    {"reason"}
            },
            {{"Who develop xxx","Who is the developer of xxx"},
                    {"developer"}},
            {{"What is xxx used to do","What can xxx do","What can be the xxx used to"},
                    {"use_to"}
            },
            {{"What are the contents of"},
                    {"has_part"}},
            {{"What is the drawback of","What is the con of"},
                    {"drawback"}}
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
            System.out.println(searchEntity);
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
        //System.out.println(keywords[positionI][0][positionJ]);
        String input=sInput.replace(keywords[positionI][0][positionJ],"");
        input=input.replace("?","");
        input=input.trim();
        //System.out.println(input);
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
            ArrayList<String> relationList=new ArrayList<String>();
            ArrayList<String> relationList_complex=new ArrayList<String>();
            ArrayList<String> result1=new ArrayList<String>();
            ArrayList<String> result2=new ArrayList<String>();
            StringBuilder sb=new StringBuilder();
            sb.append("MATCH (n1) WHERE n1.name=~"+"\""+"(?i)"+entity+"\"");
            sb.append("MATCH p=(n1)-[r]->(n2) WHERE type(r)="+"\""+relation+"\"");
            sb.append("RETURN r.content");
            Result relationContent=db.execute(sb.toString());

            StringBuilder sb_complex=new StringBuilder();
            sb_complex.append("MATCH (n1) WHERE n1.name=~"+"\""+"(?i)"+complex_entity+"\"");
            sb_complex.append("MATCH p=(n1)-[r]->(n2) WHERE type(r)="+"\""+relation+"\"");
            sb_complex.append("RETURN r.content");
            Result relationContent2=db.execute(sb_complex.toString());
            if(relationContent.hasNext()==false && relationContent2.hasNext()==false){
                result1.add("Sorry, I don't know!");
                result1.add("Do you mean "+"\"" +"What is the definition of "+entity+"?"+"\"");
                return result1;
            }
            else if(relationContent.hasNext()==true && relationContent2.hasNext()==false){
                while (relationContent.hasNext()) {
                    //System.out.println(relationContent.next().get("r.content"));
                    relationList.add(relationContent.next().get("r.content").toString());
                }
            }
            else if(relationContent.hasNext()==false && relationContent2.hasNext()==true){
                while (relationContent2.hasNext()) {
                    //System.out.println(relationContent.next().get("r.content"));
                    relationList_complex.add(relationContent2.next().get("r.content").toString());
                }
            }
            else{
                while (relationContent.hasNext()) {
                    //System.out.println(relationContent.next().get("r.content"));
                    relationList.add(relationContent.next().get("r.content").toString());
                }
            }

            ArrayList<String> entity2List=new ArrayList<String>();
            ArrayList<String> entity2List_complex=new ArrayList<String>();
            StringBuilder sb2=new StringBuilder();
            sb2.append("MATCH (n1) WHERE n1.name=~"+"\""+"(?i)"+entity+"\"");
            sb2.append("MATCH p=(n1)-[r]->(n2) WHERE type(r)="+"\""+relation+"\"");
            sb2.append("RETURN n2.name");
            Result Entity2=db.execute(sb2.toString());

            StringBuilder sb2_complex=new StringBuilder();
            sb2_complex.append("MATCH (n1) WHERE n1.name=~"+"\""+"(?i)"+complex_entity+"\"");
            sb2_complex.append("MATCH p=(n1)-[r]->(n2) WHERE type(r)="+"\""+relation+"\"");
            sb2_complex.append("RETURN n2.name");
            Result Entity2_complex=db.execute(sb2_complex.toString());
            if(Entity2.hasNext()==false &&Entity2_complex.hasNext()==false){
                result1.add("Sorry, I don't know!");
                result1.add("Do you mean "+"\"" +"What is the definition of "+entity+"?"+"\"");
                return result1;
            }
            if(Entity2.hasNext()==true &&Entity2_complex.hasNext()==false) {
                while (Entity2.hasNext()) {
                    entity2List.add(Entity2.next().get("n2.name").toString());
                }
            }
            else if(Entity2.hasNext()==false &&Entity2_complex.hasNext()==true){
                while (Entity2_complex.hasNext()) {
                    entity2List_complex.add(Entity2_complex.next().get("n2.name").toString());
                }
            }
            else{
                while (Entity2.hasNext()) {
                    entity2List.add(Entity2.next().get("n2.name").toString());
                }
            }

            for(int i=0;i<entity2List.toArray().length;i++){
                result1.add(entity + " " + relationList.toArray()[i] + " " + entity2List.toArray()[i] + ".");
                System.out.println(entity+" "+relationList.toArray()[i]+" "+entity2List.toArray()[i]+".");
            }

            for(int i=0;i<entity2List_complex.toArray().length;i++){
                result2.add(complex_entity + " " + relationList_complex.toArray()[i] + " " + entity2List_complex.toArray()[i] + ".");
                System.out.println(complex_entity+" "+relationList_complex.toArray()[i]+" "+entity2List_complex.toArray()[i]+".");

            }
            tx.success();
            if(result1.toArray().length > 0){
                return result1;
            }
            else{
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
            if(tags[i].equals("NN") || tags[i].equals("NNP") || tags[i].equals("NNPS") || tags[i].equals("NNS") || tokens[i].equals("in") || tokens[i].equals("knowledge") || tokens[i].equals("Knowledge") ||tokens[i].equals("top") ||tokens[i].equals("Top")||tokens[i].equals("-")||tokens[i].equals("domain")||tokens[i].equals("Domain")||tokens[i].equals("engineer")||tokens[i].equals("computational")||tokens[i].equals("lexical")){
                if(tokens[i].equals("works") || tokens[i].equals("work") || tokens[i].equals("mean") || tokens[i].equals("means")|| tokens[i].equals("definition")){
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

