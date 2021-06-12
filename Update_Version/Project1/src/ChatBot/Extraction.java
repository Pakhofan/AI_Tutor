package ChatBot;

import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class Extraction {
    public static void main(String[] args) {
        ArrayList<String> text_file = readTxt("C:/Users/lenovo/Desktop/SPO_result/SPO_result5.txt");
        //Create the database to store the data
        GraphDatabaseFactory dbFactory = new GraphDatabaseFactory();
        GraphDatabaseService db = dbFactory.newEmbeddedDatabase(new File("J:/FYP2/neo4j-FYP_Presentation/data/databases/graph.db"));
        //System.out.println(text_file);
        ArrayList<String> subject=new ArrayList<String>();
        ArrayList<String> relationship=new ArrayList<String>();
        ArrayList<String> property=new ArrayList<String>();
        ArrayList<String> object=new ArrayList<String>();
        ArrayList<String> definition=new ArrayList<String>();
        for(int i=0;i<text_file.toArray().length;i++){
            if(text_file.toArray()[i].toString().length()>0){
                if(text_file.toArray()[i].toString().charAt(1)=='S'){
                    String sentence = text_file.toArray()[i].toString();
                    int begin_index = sentence.indexOf("<Subject>")+9;
                    subject.add(sentence.substring(begin_index,sentence.length()-9));
                }
                else if(text_file.toArray()[i].toString().charAt(1)=='O'){
                    String sentence = text_file.toArray()[i].toString();
                    int begin_index = sentence.indexOf("<Object>")+8;
                    object.add(sentence.substring(begin_index,sentence.length()-8));
                }
                else if (text_file.toArray()[i].toString().charAt(1)=='r') {
                    String sentence = text_file.toArray()[i].toString();
                    int begin_index = sentence.indexOf(">")+1;
                    String sentence2 = sentence.substring(begin_index);
                    int end_index = sentence2.indexOf("<");
                    property.add(sentence2.substring(0,end_index));
                    relationship.add(sentence.substring(1,sentence.indexOf(">")));
                }
                else if(text_file.toArray()[i].toString().charAt(1)=='l'){
                    String sentence = text_file.toArray()[i].toString();
                    int begin_index = sentence.indexOf("<line>")+6;
                    definition.add(sentence.substring(begin_index,sentence.length()-6));
                }
            }
        }
        for(int i=0;i<subject.toArray().length;i++) {
            System.out.println(subject.toArray()[i]);
            Node subjectNode=createEntity(db,subject.toArray()[i].toString(),definition.toArray()[i].toString());
            Node objectNode=createEntity(db,object.toArray()[i].toString(),definition.toArray()[i].toString());
            createRelation(db,subject.toArray()[i].toString(),object.toArray()[i].toString(),property.toArray()[i].toString());
        }
    }
    /*
     *  This function is used to create the node in the graph database
     * @param db: the database you used to store the data
     * @param name: the name of the entity
     * @Return node: Return neo4j node
     */
    public static Node createEntity(GraphDatabaseService db, String name, String definition){
        try(Transaction tx=db.beginTx()){
            Node node=db.createNode(Extraction_agent.Tutorials.Node);
            node.setProperty("name",name);
            node.setProperty("definition",definition);
            tx.success();
            return node;
        }
    }

    /*
     *  This function is create the relationship between two nodes
     * @param db: the database you used to store the data
     * @param node1: the node 1
     * @param node2: the node 2
     * @param relation: the relation between two nodes
     */
    public static void createRelation(GraphDatabaseService db,String node1, String node2,String relation){
        try(Transaction tx=db.beginTx()){
            StringBuilder sb = new StringBuilder();
            sb.append("MATCH (n:Node{name:" + "\"" +node1 + "\"}),");
            sb.append("(m:Node{name:" + "\"" +node2 + "\"})");
            sb.append("create(n)-[relation:" + relation +"]->(m)");
            sb.append("return relation");
            db.execute(sb.toString());
            tx.success();
        }
    }

    /*
     *  This function is used to check whether there is an existing node
     * @param db: the database you used to store the data
     * @param name: the name of the node you want to check
     */
    public static Node checkNode(GraphDatabaseService db,String name){
        try(Transaction tx=db.beginTx()){
            Node resultNode=null;
            StringBuilder sb=new StringBuilder();
            sb.append("MATCH (result:Node{name:"+"\""+name+"\"})");
            sb.append("RETURN result");
            Result result=db.execute(sb.toString());
            while(result.hasNext()){
                Node subjectNode=(Node) result.next().get("result");
                resultNode=subjectNode;
            }
            tx.success();
            return resultNode;
        }
    }

    /*
     * This function is used to read txt file
     * @Param filePath: a string which represent the path of the txt file
     * @Return String: return a string which contains the content in the txt file
     */
    public static ArrayList<String> readTxt(String filePath){
        ArrayList<String> sentence_reader=new ArrayList<String>();
        try{
            File file=new File(filePath);
            if(file.isFile() && file.exists()){
                InputStreamReader reader=new InputStreamReader(
                        new FileInputStream(file),"UTF-8"
                );
                BufferedReader bufferedReader=new BufferedReader(reader);
                String lineTxt=null;
                while((lineTxt=bufferedReader.readLine())!=null){
                    //System.out.println(lineTxt);
                    sentence_reader.add(lineTxt);
                }
                reader.close();
            }
            else{
                System.out.println("Cannot find the file");
            }
        }catch(Exception e){
            e.printStackTrace();
        }
        return sentence_reader;
    }
}
