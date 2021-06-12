#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from transformers import pipeline
classifier = pipeline("zero-shot-classification",model="facebook/bart-large-mnli")


# In[12]:


# sequence_to_classify = "We also introduce deep neural networks in data mining."
# candidate_labels = ['developer', 'drawback', 'example','contain','reason','the same as','use to']
# print(classifier(sequence_to_classify, candidate_labels)['labels'][0])


# In[51]:


# ex= 'DM is an interdisciplinary subfield of computer science and statistics with an overall goal to extract information (with intelligent methods) from a dataset and transform the information into a comprehensible structure for use.'

# def preprocess(sent):
#     sent= nltk.word_tokenize(sent)
#     sent= nltk.pos_tag(sent)
#     return sent

# sent= preprocess(ex)
# pattern = r"""
#        Entity: {<DT|PRP\$>? <JJ> * <NN|NNP>+}
#        {<DT>? <NN> * <NNP>}
#        """
# cp = nltk.RegexpParser(pattern)
# tree = cp.parse(sent)
# #tree.draw()
# entity_num = 0
# entity_index = 0
# entities = []
# for tem in tree.subtrees(filter = lambda x: x.label() == "Entity"):
#     entity_num = entity_num + 1
# for tr in tree.subtrees(filter = lambda x: x.label() == "Entity"):
#     leanves_num = len(tr.leaves())
#     entity = ""
#     for i in range(leanves_num):
#         entity = entity + tr.leaves()[i][0] + " "
#     print(entity_index)
#     entities.append(entity)
#     entity_index = entity_index + 1
# print(entities)


# In[2]:


def preprocess(sent):
    sent= nltk.word_tokenize(sent)
    sent= nltk.pos_tag(sent)
    return sent
pattern = r"""
       Entity: {<DT|PRP\$>? <JJ> * <NN|NNP>+}
       {<DT>? <NN> * <NNP>}
       """
file = open('chapter.doc','r',encoding='UTF-8',errors='ignore')
with open('SPO_result.txt','a',encoding='utf-8') as f:
    for text in file:
        for line in sent_tokenize(text):
            sent= preprocess(line)
            cp = nltk.RegexpParser(pattern)
            tree = cp.parse(sent)
            entity_num = 0
            entity_index = 0
            entities = []
            for tem in tree.subtrees(filter = lambda x: x.label() == "Entity"):
                entity_num = entity_num + 1
            for tr in tree.subtrees(filter = lambda x: x.label() == "Entity"):
                leanves_num = len(tr.leaves())
                entity = ""
                for i in range(leanves_num):
                    entity = entity + tr.leaves()[i][0] + " "
                entities.append(entity)
                if entity_index == 0:
                    if entity == "":
                        f.write("<Subject><Subject>"+"\n")
                    else:
                        f.write("<Subject>"+entity[:-1]+"<Subject>"+"\n")
                        if entity_num ==1:
                            f.write("<Object> <Object>"+"\n")
                else:
                    f.write("<Object>"+entity[:-1]+"<Object>"+"\n")
                    break;
                entity_index = entity_index + 1
            if entity_num>0:
                sequence_to_classify = line
                candidate_labels = ['developer', 'drawback', 'example','contain','reason','the same as','use to']
                if classifier(sequence_to_classify, candidate_labels)['labels'][0]=="the same as":
                    f.write("<relation>the_same_as<relation>"+"\n")
                elif classifier(sequence_to_classify, candidate_labels)['labels'][0]=="use to":
                    f.write("<relation>use_to<relation>"+"\n")
                else:
                    f.write("<relation>"+classifier(sequence_to_classify, candidate_labels)['labels'][0]+"<relation>"+"\n")
                f.write("<line>"+line+"<line>"+"\n")
            f.write("\n")
f.close()


# In[15]:


# def preprocess(sent):
#     sent= nltk.word_tokenize(sent)
#     sent= nltk.pos_tag(sent)
#     return sent
# pattern = r"""
#        Entity: {<DT|PRP\$>? <JJ> * <NN|NNP>+}
#        {<DT>? <NN> * <NNP>}
#        """
# file = open('chapter4.doc','r',encoding='UTF-8',errors='ignore')
# for text in file:
#     for line in sent_tokenize(text):
#         sent= preprocess(line)
#         cp = nltk.RegexpParser(pattern)
#         tree = cp.parse(sent)
#         entity_num = 0
#         entity_index = 0
#         entities = []
#         for tem in tree.subtrees(filter = lambda x: x.label() == "Entity"):
#             entity_num = entity_num + 1
#         for tr in tree.subtrees(filter = lambda x: x.label() == "Entity"):
#             leanves_num = len(tr.leaves())
#             entity = ""
#             for i in range(leanves_num):
#                 entity = entity + tr.leaves()[i][0] + " "
#             if entity_index == 0:
#                 if entity == " ":
#                     print("<Subject><Subject>")
#                 else:
#                     print("<Subject>"+entity[:-1]+"<Subject>")
#                     if entity_num ==1:
#                         print("<Object> <Object>")
#             else:
#                 if entity == " ":
#                     print("<Object><Object>")
#                 else:
#                     print("<Object>"+entity[:-1]+"<Object>")
#             entity_index = entity_index + 1
#         print()

