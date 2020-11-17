# AI_Tutor
### This project is the Knowledge Graph-Based QA System, it contains the knowledge extraction part and QA part.
#### File description
1. ***Document*** contain the original text for knowledge extraction, the result of SPO triple after extraction, and some library files.
2. ***JADE platform*** contain the source code for the project. It is a java-based project implemented in IntelliJ IDEA.
3. ***extraction.py*** is a python file to extract SPO triples from the original text to a structured document.
4. ***Knowledge*** is the NEO4J graphical database to store and maintain the knowledge information.
#### Main technology
1. ***Spacy*** toolkit to perform common natural language process tasks for knowledge generation.
2. ***OpenNLP*** toolkit to perform common natural language process tasks for question in QA system.
3. ***JADE*** platform to implement the multi-agent framwork.
4. ***MVC*** framework to achieve the GUI for user to input question and output answer.
#### Source
1. Download the ***[JADE platform](https://jade.tilab.com/download/jade/)***
2. Download the files of ***[OpenNLP](http://maven.tamingtext.com/opennlp-models/models-1.5/)***
#### Operation
1. We use the book ***Knowledge Seeker - Ontology Modelling for Information Search and Management*** as the original text. In this project, we use the first chapter as an example. The file ***text2.doc*** shows the content of the book.
2. Run the ***extraction.py***, we can extract the SPO triples from the text. The result after running the python file:
<img src="https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/result.jpg" width = "300" height = "200" alt="program result" align=center></image>
And then the program will store the result to a structured document ***SPO_result.txt***:
<img src="https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/structured%20document.png" width = "300" height = "200" alt="structured document" align=center />
3. Use IntelliJ IDEA to open the ***Project1***, we can see the compiler interface:
<img src="https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/compiler%20interface.png" width = "300" height = "200" alt="structured document" align=center />
4. To launch the project, we need to configure the external libraries. Firstly, we configure the NEO4J. Import the jar files in ***neo4j-community-3.5.21/lib/*** to the project structure:
<img src="https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/neo4j%20configuration.png" width = "300" height = "200" alt="structured document" align=center />
5. Then we configure OpenNLP. Similarly, import the ***opennlp-tools-1.9.2.jar*** in ***Document/apache-opennlp-1.9.2/lib/*** to the project structure:
<img src="https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/OpenNLP%20configuration.png" width = "300" height = "200" alt="structured document" align=center />
6. Then we configure JADE platform. Similarly, import the ***lib*** in ***Document/JADE-all-4.5.0/JADE-bin-4.5.0/jade/*** to the project structure:
<img src="https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/JADE%20configuration.png" width = "300" height = "200" alt="structured document" align=center />
7. Before we run the project, we should congifure the running object. We can choose to run the Agent_management to manipulate the multiple agents. Add a new application and set the Program arguments:
<img src="https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/Agent_management.png" width = "300" height = "200" alt="structured document" align=center />
And we can see the running result:
<img src="https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/agent%20management.jpg" width = "300" height = "200" alt="structured document" align=center />
Or we can choose to run the Extraction_agent individually. Similarly, add a new application and set the Program arguments:
<img src="https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/extraction_agent.png" width = "300" height = "200" alt="structured document" align=center />
We can see the instruction for finishing extraction in the IDEA terminal after running the Extraction_agent successfully.
Or we can choose to run the QA_agent individually. Similarly, add a new application and set the Program arguments:
<img src="https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/QA_agent.png" width = "300" height = "200" alt="structured document" align=center />
Finally, we can see the GUI chat window:
<img src="https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/GUI.png" width = "300" height = "200" alt="structured document" align=center />
