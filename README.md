# AI_Tutor
### This project is the Knowledge Graph-Based QA System, it contains the knowledge extraction part and QA part.
#### File description
1. ***Document*** contain the original text for knowledge extraction and the result of SPO triple after extraction.
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
2. Download the ***[OpenNLP](http://maven.tamingtext.com/opennlp-models/models-1.5/)***
#### Operation
1. We use the book ***Knowledge Seeker - Ontology Modelling for Information Search and Management*** as the original text. In this project, we use the first chapter as an example. The file ***text2.doc*** shows the content of the book.
2. Run the ***extraction.py***, we can extract the SPO triples from the text. The result after running the python file:
![program result](https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/result.jpg)
And then the program will store the result to a structured document:
![structured document](https://raw.githubusercontent.com/Pakhofan/AI_Tutor/main/Program%20image/structured%20document.png)
