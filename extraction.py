import re 
import string 
import nltk 
import spacy 
import pandas as pd 
import numpy as np 
import math 
from tqdm import tqdm 

from spacy.matcher import Matcher
from spacy.tokens import Span 
from spacy import displacy 
pd.set_option('display.max_colwidth', 200)

nlp = spacy.load("en_core_web_sm") # load spaCy model
file = open('C:/Users/lenovo/Desktop/FYP_extract/text2.doc','r') #load the extraction file
text = []
print(len(''))
for line in file: #read the file and split to individual sentence
    line = re.split(r'[\.]+', line)
    for tem in line:
        if len(tem)>0:
            if ((tem[0]==' ') or (tem[0]==',') or (tem[0]==2)):
                text.append(tem[1:])
            else:
                text.append(tem[:-2])

# print token, dependency, POS tag 
#for tok in doc: 
#  print(tok.text, "-->",tok.dep_,"-->", tok.pos_)

def definition():
    result = []
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'LOWER':'is'},{'LOWER': 'an'},{'POS':'ADJ'},{'POS':'NOUN'},{},{}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (str(word) == "an" and position == "relation"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'LOWER':'refers'},{'LOWER': 'to'},{'POS':'DET'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "refers" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "refers"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (str(word) == "to" and position == "relation"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'POS':'ADP'},{'POS':'NOUN'},{'LOWER':'define'},{'POS': 'PRON'},{'POS': 'AUX'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "define" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "define"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "require" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern1 = [{'DEP':'nsubjpass','POS':'NOUN'}]
    pattern2 = [{'LOWER':'as'},{'LOWER':'a'},{},{},{'POS':'DET'},{},{},{},{},{},{}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern1, pattern2) 
    matches = matcher(doc) 
    if (len(matches) == 2):
        subject = relationship = object = ''
        subject = str(doc[matches[0][1]:matches[0][2]])
        position = "subject"
        for word in doc[matches[1][1]:matches[1][2]]:
            if (str(word) == "as"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (str(word) == "a"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-1]))
    #define the pattern 
    pattern1 = [{'DEP':'nsubj','POS':'NOUN'},{'DEP':'prep','POS':'ADP'},{'DEP':'pobj','POS':'NOUN'}]
    pattern2 = [{'LOWER':'define'},{'POS':'NOUN'},{'POS':'DET'},{'POS':'AUX'},{'POS':'ADJ'},{'POS':'ADP'},{'POS':'ADJ'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern1, pattern2) 
    matches = matcher(doc) 
    if (len(matches) == 2):
        subject = relationship = object = ''
        subject = str(doc[matches[0][1]:matches[0][2]])
        position = "subject"
        for word in doc[matches[1][1]:matches[1][2]]:
            if (str(word) != "define" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "define"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "require" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship, object[:-1]))
    #define the pattern 
    pattern = [{'POS':'VERB'},{'POS':'ADJ'},{'POS':'NOUN'},{'LOWER':'is'},{'POS': 'DET'},{'POS':'NOUN'},{'POS':'ADP'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "require" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern1 = [{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'NOUN'},{'POS':'ADP'},{'POS': 'DET'},{'POS':'NOUN'},{'POS':'PART'},{'POS':'VERB'},{'POS':'NOUN'}]
    pattern2 = [{'LOWER':'is'}]
    pattern3 = [{'POS':'NOUN'},{'POS':'PUNCT'},{'POS':'VERB'},{'POS':'NOUN'},{'POS':'PUNCT'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern1,pattern2,pattern3) 
    matches = matcher(doc) 
    if (len(matches) == 3):
        subject = str(doc[matches[2][1]:matches[2][2]])
        relationship = str(doc[matches[1][1]:matches[1][2]])
        object = str(doc[matches[0][1]:matches[0][2]])
        result.append((subject[:-1], relationship, object))
    #define the pattern 
    pattern1 = [{'POS':'NOUN','DEP':'compound'},{'POS':'NOUN','DEP':'nsubj'}]
    pattern2 = [{'LOWER':'is'},{'POS': 'DET'},{'POS':'NOUN'},{'POS':'PART'},{'POS':'VERB'},{'POS':'ADP'},{'POS':'DET'},{'POS':'NOUN'},{},{},{},{},{},{},{'POS':'ADP'},{},{}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern1,pattern2) 
    matches = matcher(doc) 
    if (len(matches) == 2):
        subject = relationship = object = ''
        subject = str(doc[matches[0][1]:matches[0][2]])
        position = "subject"
        for word in doc[matches[1][1]:matches[1][2]]:
            if (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "is" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship, object[:-1]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'NOUN'},{'LOWER': 'can'},{'LOWER': 'be'},{'LOWER': 'simply'},{'LOWER': 'defined'},{'LOWER': 'as'},{'POS': 'DET'},{'POS': 'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        subject = 'scientific and mathematical approaches to discover the knowledge'
        for word in doc:
            if (str(word) == "can"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="as"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "as"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'POS':'NOUN'},{'LOWER': 'can'},{'LOWER': 'be'},{'LOWER': 'summarized'},{'LOWER': 'in'},{'POS':'NUM'},{'POS':'ADJ'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "can" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "can"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="in"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "in"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'NOUN'},{'POS':'NOUN'},{'LOWER':'is'},{'LOWER': 'a'},{'POS':'ADJ'},{'POS':'PUNCT'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        subject2 = relationship2 = object2 = ''
        position = "subject"
        position2 = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "is" and position == "object"):
                object = object + str(word) + ' '
                if (str(word) == "surrogate" and position2 == "subject"):
                    subject2 = 'Surrogate'
                elif (str(word) == "-"):
                    relationship2 = 'is'
                    position2 = "object"
                elif (str(word) != "-" and position2 == "object"):
                    object2 = object2 + str(word) + ' '
        result.append(((subject[2:-1], relationship, object[:-3]),(subject2, relationship2, object2[:-3])))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'NOUN'},{'POS':'NOUN'},{'LOWER':'is'},{'LOWER': 'a'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'ADJ'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        subject2 = relationship2 = object2 = ''
        position = "subject"
        position2 = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "is" and position == "object"):
                object = object + str(word) + ' '
                if (str(word) != "-" and position2 == "subject"):
                    subject2 = subject2 + str(word) + ' '
                elif (str(word) == "-"):
                    relationship2 = 'is'
                    position2 = "object"
                elif (str(word) != "-" and position2 == "object"):
                    object2 = object2 + str(word) + ' '
        result.append(((subject[2:-1], relationship, object[:-1]),(subject2[:-1], relationship2, object2[:-3])))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'NOUN'},{'POS':'NOUN'},{'LOWER':'is'},{'LOWER': 'a'},{'DEP':'amod','POS':'ADJ'},{'DEP':'attr','POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        subject2 = relationship2 = object2 = ''
        position = "subject"
        position2 = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "is" and position == "object"):
                object = object + str(word) + ' '
                if (str(word) != "-" and position2 == "subject"):
                    subject2 = subject2 + str(word) + ' '
                elif (str(word) == "-"):
                    relationship2 = 'is'
                    position2 = "object"
                elif (str(word) != "-" and position2 == "object"):
                    object2 = object2 + str(word) + ' '
        result.append(((subject[2:-1], relationship, object[:-3]),(subject2[:-1], relationship2, object2[:-3])))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'CCONJ'},{'POS':'ADJ'},{'POS':'NOUN'},{'LOWER':'may'},{'LOWER': 'be'},{'LOWER':'defined'},{'LOWER':'for'},{'POS':'ADJ'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "may" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "may"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="for"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "for"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'POS':'ADV'},{'LOWER':'must'},{'LOWER':'be'},{'LOWER':'encoded'},{'LOWER':'in'},{'POS':'DET'},{'POS':'NOUN'},{'POS':'ADP'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "must" and position == "subject"):
                subject = 'Knowledge representation'
            elif (str(word) == "must"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="in"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "in"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'DEP':'compound'},{'DEP':'nsubj'},{'LOWER': 'defines'},{'DEP':'det'},{'DEP':'amod'},{'DEP':'dobj'},{'DEP':'prep'},{'DEP':'pobj'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "defines" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "defines"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "defines" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'POS':'PUNCT'},{'LOWER': 'it'},{'LOWER':'defines'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "defines" and position == "subject"):
                subject = str(doc[matches[0][1]])
            elif (str(word) == "defines"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "defines" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'POS':'PUNCT'},{'LOWER': 'it'},{'LOWER':'supports'},{'LOWER':'and'},{'LOWER':'distinguishes'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "supports" and position == "subject"):
                subject = str(doc[matches[0][1]])
            elif (str(word) == "supports"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="distinguishes"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "distinguishes"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-1]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'POS':'NOUN'},{'LOWER': 'defines'},{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "defines" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "defines"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "defines" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[2:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'LOWER':'described'},{'LOWER':'in'},{'POS':'NUM'},{'POS':'ADJ'},{'POS':'NOUN'},{'TEXT':':'}]
    pattern1 = [{'TEXT':'1'},{'TEXT':'.'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'}]
    pattern2 = [{'TEXT':'2'},{'TEXT':'.'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'}]
    pattern3 = [{'TEXT':'3'},{'TEXT':'.'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'}]
    pattern4 = [{'TEXT':'4'},{'TEXT':'.'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'}]
    pattern5 = [{'TEXT':'5'},{'TEXT':'.'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern,pattern1,pattern2,pattern3,pattern4,pattern5) 
    matches = matcher(doc) 
    if (len(matches) == 6):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "described" and position == "subject"):
                subject = str(doc[0])
            elif (str(word) == "described"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (str(word) == "in"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object" and str(word) != ":"):
                object = object + str(word) + ' '
            else:
                object = object + ': '
                break
        object = object+str(doc[matches[1][1]:matches[1][2]])+' '+str(doc[matches[2][1]:matches[2][2]])+' '+str(doc[matches[3][1]:matches[3][2]])+' '+str(doc[matches[4][1]:matches[4][2]])+' '+str(doc[matches[5][1]:matches[5][2]])
        result.append((subject[:-1], relationship[:-1], object))
    #define the pattern 
    pattern = [{'POS':'X','DEP':'appos'},{'POS':'PUNCT'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'},{'LOWER':'contains'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "contains" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "contains"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "contains" and str(word) != "2" and position == "object"):
                object = object + str(word) + ' '
            else:
                break
        result.append((subject[4:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'X','DEP':'ROOT'},{'POS':'PUNCT'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'},{'LOWER':'is'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "is" and str(word) != "2" and position == "object"):
                object = object + str(word) + ' '
            else:
                break
        result.append((subject[4:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'LOWER':'is'},{'LOWER': 'a'},{'POS':'ADJ'},{'POS':'ADJ'},{'POS':'CCONJ'},{'POS':'ADJ'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "is" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PROPN'},{'POS':'PROPN'},{'LOWER':'is'},{'LOWER': 'divided'},{'LOWER':'into'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="into"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "into"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern1 = [{'POS':'ADP'},{'POS':'DET'},{'POS':'NOUN'},{'POS':'NOUN'},{'POS':'NOUN'}]
    pattern2 = [{'POS':'NOUN'},{'lower':'defines'},{'POS': 'DET'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'ADJ'},{'POS':'NOUN'},{},{},{},{},{},{},{},{},{},{}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern1,pattern2) 
    matches = matcher(doc) 
    if (len(matches) == 2):
        subject = relationship = object = ''
        position = "subject"
        for word in doc[matches[1][1]:matches[1][2]]:
            if (str(word) != "defines" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "defines"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "require" and position == "object"):
                object = object + str(word) + ' '
        object = object + str(doc[matches[0][1]:matches[0][2]])
        result.append((subject, relationship, object))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'NOUN'},{'LOWER':'has'},{'LOWER': 'been'},{'LOWER':'defined'},{'LOWER':'in'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "has" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "has"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="in"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "in"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'NOUN'},{'LOWER':'defines'},{'POS':'NOUN'},{'POS':'SCONJ'},{'POS':'DET'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "defines" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "defines"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "defines" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-2]))
    #define the pattern 
    pattern = [{'LOWER':'are'},{'LOWER':'limited'},{'LOWER':'to'},{'POS':'NOUN'},{'POS':'DET'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "are" and position == "subject"):
                subject = str(doc[0])+' '+str(doc[1])+' '+str(doc[2])+' '+str(doc[3])
            elif (str(word) == "are" and position == "subject"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="to"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "to"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'PROPN'},{'LOWER':'is'},{'LOWER':'also'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (str(word) == "also"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[4:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'LOWER':'is'},{'POS':'DET','DEP':'det'},{'POS':'ADJ','DEP':'amod'},{'POS':'PUNCT'},{'POS':'NOUN','DEP':'attr'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = 'The OpenCyc ontology'
            elif (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "is" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'},{'LOWER':'is'},{'POS':'DET'},{'POS':'NOUN'},{'POS':'VERB'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "is" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[2:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PROPN'},{'LOWER':'is'},{'POS':'DET'},{'POS':'PROPN'},{'POS':'VERB'},{'POS':'NOUN'},{'POS':'DET'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "is"  and str(word)!="," and position == "object"):
                object = object + str(word) + ' '
            else:
                break
        result.append((subject[:-1], relationship, object[:-1]))
    #define the pattern 
    pattern = [{'POS':'PROPN'},{'LOWER':'is'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'PUNCT'},{'POS':'ADJ'},{'POS':'ADJ'},{'POS':'ADJ'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "is" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PROPN'},{'LOWER':'is'},{'LOWER':'originally'},{'LOWER':'designed'},{'LOWER':'as'},{'POS':'DET'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="as"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "as"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PROPN'},{'LOWER':'is'},{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'VERB'},{'POS':'ADP'},{'POS':'PROPN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "is" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'LOWER':'is'},{'POS':'DET','DEP':'det'},{'POS':'ADJ','DEP':'amod'},{'POS':'PUNCT','DEP':'punct'},{'POS':'NOUN','DEP':'compound'},{'POS':'NOUN','DEP':'attr'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = 'HowNet'
            elif (str(word) == "is"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "is" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PUNCT'},{'POS':'PROPN'},{'LOWER':'defines'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'PROPN'},{'POS':'PUNCT'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "defines" and position == "subject"):
                subject = str(doc[7])
            elif (str(word) == "defines"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "defines" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PROPN'},{'LOWER':'also'},{'LOWER':'defines'},{'POS':'DET'},{'POS':'NOUN'},{'POS':'DET'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "also" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "also"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (str(word) == "defines"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'ADJ'},{'POS':'NOUN'},{'LOWER':'is'},{'LOWER':'hard'},{'LOWER':'for'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="for"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "for"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'NOUN'},{'POS':'NOUN'},{'LOWER':'is'},{'LOWER':'tied'},{'LOWER':'to'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="to"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "to"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    return result

def has_part():
    result = []
    #define the pattern 
    pattern = [{'LOWER':'described'},{'LOWER':'in'},{'POS':'NUM'},{'POS':'ADJ'},{'POS':'NOUN'},{'TEXT':':'}]
    pattern1 = [{'TEXT':'1'},{'TEXT':'.'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'}]
    pattern2 = [{'TEXT':'2'},{'TEXT':'.'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'}]
    pattern3 = [{'TEXT':'3'},{'TEXT':'.'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'}]
    pattern4 = [{'TEXT':'4'},{'TEXT':'.'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'}]
    pattern5 = [{'TEXT':'5'},{'TEXT':'.'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern,pattern1,pattern2,pattern3,pattern4,pattern5) 
    matches = matcher(doc) 
    if (len(matches) == 6):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        relationship = 'contains'
        for word in doc:
            if (str(word) == "five"):
                subject = subject + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!=":"):
                subject = subject + str(word) + ' '
            elif (str(word) == ":"):
                subject = subject + str(word) + ' '
                position = "object"
        subject = subject+str(doc[matches[1][1]:matches[1][2]])+' '+str(doc[matches[2][1]:matches[2][2]])+' '+str(doc[matches[3][1]:matches[3][2]])+' '+str(doc[matches[4][1]:matches[4][2]])+' '+str(doc[matches[5][1]:matches[5][2]])
        result.append((subject, relationship, str(doc[matches[1][1]:matches[1][2]])[3:]))
        result.append((subject, relationship, str(doc[matches[2][1]:matches[2][2]])[3:]))
        result.append((subject, relationship, str(doc[matches[3][1]:matches[3][2]])[3:]))
        result.append((subject, relationship, str(doc[matches[4][1]:matches[4][2]])[3:]))
        result.append((subject, relationship, str(doc[matches[5][1]:matches[5][2]])[3:]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'DET'},{'POS':'NOUN'},{'LOWER':'contain'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "contain" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "contain"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "contain" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'NOUN'},{'POS':'NOUN'},{'LOWER':'is'},{'POS':'ADV'},{'LOWER':'simplified'},{'POS':'ADP'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "simplified" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "simplified"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "simplified" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[4:-12], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'NOUN'},{'LOWER':'are'},{'LOWER':'organized'},{'LOWER':'by'},{'POS':'ADJ'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "are" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "are"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="by"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "by"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'ADP'},{'POS':'PRON'},{'LOWER':'are'},{'LOWER':'organized'},{'LOWER':'as'},{'POS':'DET'},{'POS':'NOUN'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "are" and position == "subject"):
                if str(word) == 'them':
                    subject = subject + 'vocabularies' + ' '
                else:
                    subject = subject + str(word) + ' '
            elif (str(word) == "are" and position == "subject"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="as"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "as"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PROPN'},{'LOWER':'divides'},{'POS':'DET'},{'POS':'NOUN'},{'POS':'NOUN'},{'LOWER':'into'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "divides" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "divides"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "divides" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'ADJ'},{'POS':'PROPN'},{'POS':'NOUN'},{'LOWER':'contains'},{'POS':'NOUN'},{'POS':'ADP'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "contains" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "contains"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "contains" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'LOWER':'contains'},{'POS':'DET'},{'POS':'NOUN'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "contains" and position == "subject"):
                subject = 'The OpenCyc ontology'
            elif (str(word) == "contains"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "contains" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'LOWER':'covers'},{'POS':'ADP'},{'POS':'NUM'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'PROPN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "covers" and position == "subject"):
                subject = 'HowNet'
            elif (str(word) == "covers"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "covers" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship, object[:-3]))
    return result

def the_same_thing():
    result = []
    #define the pattern 
    pattern1 = [{'POS':'NOUN'},{'DEP':'prep','POS':'ADP'},{'POS':'NOUN'},{'POS':'NOUN'}]
    pattern2 = [{'LOWER':'as'},{'LOWER': 'called'},{'POS':'ADJ'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_3", None, pattern1, pattern2) 
    matches = matcher(doc) 
    if (len(matches) == 2):
        subject = relationship = object = ''
        subject = str(doc[matches[0][1]:matches[0][2]])
        position = "subject"
        for word in doc[matches[1][1]:matches[1][2]]:
            if (str(word) == "as"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (str(word) == "called"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-1]))
    #define the pattern 
    pattern = [{'POS':'PUNCT'},{'LOWER':'called'},{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'PUNCT'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "called" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "called"):
                relationship = str(word)
                position = "object"
            elif (str(word) == ','):
                break
            elif (str(word) != "called" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-3], relationship, object[:-1]))
    #define the pattern 
    pattern = [{'POS':'ADJ'},{'POS':'PUNCT'},{'POS':'NOUN'},{'POS':'NOUN'},{},{'LOWER':'also'},{'LOWER':'known'},{'LOWER':'as'},{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'PUNCT'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc[matches[0][1]:matches[0][2]]:
            if (str(word) != "also" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "also"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="as"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "as"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-3], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PUNCT'},{'TEXT':'In'},{'LOWER':'another'},{'LOWER':'words'},{'POS':'PUNCT'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "In" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "In"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="words"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "words"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-3], relationship[:-1], object[2:-3]))
    return result

def represent():
    result = []
    #define the pattern 
    pattern = [{'POS':'AUX'},{'POS': 'AUX'},{'LOWER': 'represented'},{'POS': 'SCONJ'},{'POS': 'DET'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "has" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "has"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="a"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "a"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'ADJ'},{'POS': 'NOUN'},{'LOWER': 'is'},{'LOWER': 'generally'},{'LOWER': 'represented'},{'LOWER': 'in'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="in"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "in"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-1]))
    return result

def reason():
    result = []
    #define the pattern 
    pattern = [{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'NOUN'},{'POS':'AUX'},{'POS': 'VERB'},{'POS':'ADP'},{'POS':'NOUN'},
               {'LOWER':'because'},
               {'POS':'PRON'}
               ]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "because" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "because"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "require" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern1 = [{'LOWER':'to'},{'LOWER':'enable'}]
    pattern2 = [{'POS':'DET'},{'POS':'NOUN'},{'POS':'NOUN'},{'POS':'CCONJ'},{'POS':'NOUN'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern1, pattern2) 
    matches = matcher(doc) 
    if (len(matches) == 2):
        subject = relationship = object = ''
        relationship = str(doc[matches[0][1]:matches[0][2]])
        object = str(doc[matches[1][1]:matches[1][2]])
        position = " "
        for word in doc:
            if (str(word) == "we"):
                subject = subject + str(word) + ' '
                position = "subject"
            elif (position == "subject" and str(word)!="we"):
                subject = subject + str(word) + ' '
        result.append((subject[:-3], relationship[:-1], object[:-1]))
    #define the pattern 
    pattern = [{'POS':'PUNCT'},{'TEXT':'Therefore'},{'LOWER': 'it'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        subject = str(doc[0])+' '
        for word in doc:
            if (str(word) != "Therefore" and position == "subject"):
                object = object + str(word) + ' '
            elif (str(word) == "Therefore"):
                relationship = 'because'
                position = "object"
            elif (str(word) != "Therefore" and str(word) != "it" and position == "object"):
                subject = subject + str(word) + ' '
        result.append((subject[:-3], relationship, object[:-3]))
    result = []
    #define the pattern 
    pattern = [{'POS':'PUNCT'},{'TEXT':'Since'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "Since" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "Since"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "Since" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-3], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PUNCT'},{'LOWER':'so'},{'POS':'DET'},{'POS':'VERB'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "so" and position == "subject"):
                object = object + str(word) + ' '
            elif (str(word) == "so"):
                relationship = 'because'
                position = "object"
            elif (str(word) != "so" and position == "object"):
                subject = subject + str(word) + ' '
        result.append((subject[:-3], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'TEXT':'Therefore'},{'POS':'PUNCT'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'ADV'},{'POS':'VERB'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "," and position == "subject"):
                object = 'the concept and usage of words are changing all the time'
            elif (str(word) == ","):
                relationship = 'because'
                position = "object"
            elif (str(word) != "," and position == "object"):
                subject = subject + str(word) + ' '
        result.append((subject[:-3], relationship, object))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'POS':'VERB'},{'POS':'AUX'},{'POS':'VERB'},{'POS':'ADP'},{'POS':'ADJ'},{'POS':'NOUN'},{'LOWER':'because'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "because" and position == "subject"):
                if str(word)=='It':
                    subject = 'Domain ontology '
                else:
                    subject = subject + str(word) + ' '
            elif (str(word) == "because"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "because" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'TEXT':'In'},{'LOWER':'order'},{'LOWER':'to'},{'POS':'VERB'},{'POS':'DET'},{'POS':'NOUN'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "," and position == "subject"):
                object = object + str(word) + ' '
            elif (str(word) == ","):
                relationship = 'in order to'
                position = "object"
            elif (str(word) != "," and position == "object"):
                subject = subject + str(word) + ' '
        result.append((subject[:-3], relationship, object[12:-1]))
    #define the pattern 
    pattern = [{'POS':'ADJ'},{'POS':'ADJ'},{'POS':'NOUN'},{'LOWER':'for'},{'LOWER':'the'},{'LOWER':'ease'},{'LOWER':'of'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "for" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "for"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="of"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "of"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'TEXT':'It'},{'LOWER':'is'},{'LOWER':'therefore'},{},{},{},{},{},{},{'LOWER':'because'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "because" and position == "subject"):
                subject = 'domain ontology is more useful to build intelligent application'
            elif (str(word) == "because"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "because" and position == "object"):
                object = object + str(word) + ' '
        object2 = 'domain ontology is less abstract but more specific'
        result.append((subject, relationship, object[:-3]))
        result.append((subject, relationship, object2))
    return result

def method():
    pattern = [{'TEXT':'It'},{'POS': 'VERB'},{'POS': 'NOUN'},{'POS': 'ADP'},{'POS': 'VERB'},{'POS': 'CCONJ'},{'POS': 'VERB'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        subject = 'Knowledge engineering'
        for word in doc:
            if (str(word) == "requires"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="discovering"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "discovering"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        return (subject, relationship[:-1], object[:-3])

def use_to():
    result = []
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'POS':'NOUN'},{'LOWER':'is'},{'LOWER': 'used'},{'LOWER':'by'},{'POS':'NOUN'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="by"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "by"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'TEXT':'It'},{'LOWER':'applies'},{},{},{},{},{},{},{},{'LOWER':'including'},{'TEXT':':'}]
    pattern1 = [{'TEXT':'1'},{'TEXT':'.'},{'POS':'NOUN'}]
    pattern2 = [{'TEXT':'2'},{'TEXT':'.'},{'POS':'NOUN'}]
    pattern3 = [{'TEXT':'3'},{'TEXT':'.'},{'POS':'PROPN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern,pattern1,pattern2,pattern3) 
    matches = matcher(doc) 
    if (len(matches) == 4):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "applies" and position == "subject"):
                subject = 'knowledge representation'
            elif (str(word) == "applies"):
                relationship = str(word)
                position = "object"
            elif (str(word) != ":" and position == "object"):
                object = object + str(word) + ' '
            else:
                object = object + str(word) + ' '
                break
        object = object+str(doc[matches[1][1]:matches[1][2]])+str(doc[matches[2][1]:matches[2][2]])+str(doc[matches[3][1]:matches[3][2]])
        result.append((subject, relationship, object))
        result.append((object,'including',str(doc[matches[1][1]:matches[1][2]])[3:]))
        result.append((object,'including',str(doc[matches[2][1]:matches[2][2]])[3:]))
        result.append((object,'including',str(doc[matches[3][1]:matches[3][2]])[3:]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'POS':'NOUN'},{'POS':'NOUN'},{'LOWER':'is'},{'LOWER': 'used'},{'LOWER':'to'},{'LOWER':'express'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="express"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "express"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PART'},{'LOWER':'express'},{'POS':'NOUN'},{'POS':'CCONJ'},{'POS':'NOUN'},{'POS':'PUNCT'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "to" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "to"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (str(word) == "express"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'LOWER':'are'},{'LOWER':'used'},{'LOWER':'to'},{'LOWER':'model'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "are" and position == "subject"):
                subject = 'The representational primitives of the ontology'
            elif (str(word) == "are"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="model"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "model"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'POS':'ADV'},{'LOWER':'is'},{'LOWER':'regarded'},{'LOWER':'as'},{'LOWER':'for'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = 'The representational primitives of the ontology'
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="for"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "for"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'LOWER':'is'},{'LOWER':'used'},{'LOWER':'to'},{'POS':'VERB'},{'POS':'DET'},{'POS':'NOUN'},{'POS':'ADP'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = 'The representational primitives of the ontology'
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="to"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "to"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'},{'LOWER':'is'},{'LOWER':'in'},{'LOWER':'support'},{'LOWER':'of'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = 'The representational primitives of the ontology'
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="of"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "of"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-4], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'POS':'NOUN'},{'LOWER':'are'},{'LOWER':'created'},{'LOWER':'as'},{'POS':'NOUN'},{'POS':'ADJ'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "are" and position == "subject"):
                subject = 'The representational primitives of the ontology'
            elif (str(word) == "are"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="as"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "as"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'LOWER':'aids'},{'POS':'DET'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "aids" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "aids"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "aids" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'LOWER':'enables'},{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "enables" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "enables"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "enables" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'LOWER':'provides'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "provides" and position == "subject"):
                subject = 'Ontology modeling in computer system'
            elif (str(word) == "provides"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "provides" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'POS':'VERB'},{'LOWER':'conceptualization'},{'LOWER': 'by'},{'LOWER':'defining'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "conceptualization" and position == "subject"):
                subject = 'Computational ontology'
            elif (str(word) == "conceptualization"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="defining"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "defining"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'LOWER':'are'},{'LOWER': 'generic'},{'LOWER':'enough'},{'LOWER':'to'},{'LOWER':'deal'},{'LOWER':'with'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "are" and position == "subject"):
                subject = 'Top-level ontologies'
            elif (str(word) == "are"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="with"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "with"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'ADJ'},{'POS':'PUNCT'},{'POS':'NOUN'},{'POS':'NOUN'},{'LOWER':'promotes'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "promotes" and position == "subject"):
                subject = 'Top-level ontologies'
            elif (str(word) == "promotes"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "promotes" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'LOWER':'serves'},{'LOWER': 'as'},{'POS':'DET'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "serves" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "serves"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (str(word) == "as"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'ADJ'},{'POS':'NOUN'},{'LOWER':'is'},{'LOWER': 'useful'},{'LOWER':'for'},{'LOWER':'developing'},{'POS':'NOUN'},{'POS':'VERB'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="for"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "for"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'LOWER':'could'},{'LOWER':'be'},{'LOWER': 'used'},{'LOWER':'as'},{'POS':'DET'},{'POS':'ADJ'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "could" and position == "subject"):
                subject = 'WordNet'
            elif (str(word) == "could"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="as"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "as"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PROPN'},{'LOWER':'defines'},{'POS':'NOUN'},{'POS':'PART'},{'POS':'VERB'},{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'PUNCT'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "defines" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "defines"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "defines" and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'LOWER':'is'},{'LOWER':'helpful'},{'LOWER':'to'},{'POS':'VERB'},{'POS':'NOUN'},{'POS':'ADP'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = 'WordNet'
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="to"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "to"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'LOWER':'has'},{'LOWER':'been'},{'LOWER':'used'},{'LOWER':'for'},{'POS':'ADJ'},{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'NOUN'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "has" and position == "subject"):
                subject = 'WordNet'
            elif (str(word) == "has"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="for"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "for"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PROPN'},{'LOWER':'is'},{'LOWER':'aimed'},{'LOWER':'for'},{'POS':'ADJ'},{'POS':'NOUN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="for"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "for"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-3]))
    #define the pattern 
    pattern = [{'POS':'NOUN'},{'POS':'NOUN'},{'POS':'ADV'},{'LOWER':'aims'},{'LOWER':'to'},{'LOWER':'define'},{'LOWER':'and'},{'LOWER':'create'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "aims" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "aims"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="create"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "create"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-9], relationship[:-1], object[:-3]))
    return result

def developer():
    result = []
    #define the pattern 
    pattern = [{'POS':'DET'},{'POS':'ADJ'},{'POS':'ADJ'},{'POS':'NOUN'},{'POS':'VERB'},{'POS':'NOUN'},{'LOWER':'develops'},{'POS':'DET'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "develops" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "develops"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "develops" and position == "object"):
                if (str(word)=='"'):
                    object = object + "'" + ' '
                else:
                    object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'PRON'},{'LOWER':'creates'},{'POS':'DET'},{'POS':'NOUN'},{'POS':'ADP'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "creates" and position == "subject"):
                subject = 'SUMO'
            elif (str(word) == "creates"):
                relationship = str(word)
                position = "object"
            elif (str(word) != "creates" and position == "object"):
                if (str(word)=='"'):
                    object = object + "'" + ' '
                else:
                    object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    #define the pattern 
    pattern = [{'POS':'ADJ'},{'POS':'NOUN'},{'LOWER':'developed'},{'LOWER':'by'},{'POS':'PROPN'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "developed" and position == "subject"):
                subject = str(doc[0])
            elif (str(word) == "developed"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (str(word) == "by"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                if (str(word)=='"'):
                    object = object + "'" + ' '
                else:
                    object = object + str(word) + ' '
        result.append((subject, relationship[:-1], object[:-3]))
    return result

def drawback():
    result = []
    #define the pattern 
    pattern = [{'POS':'PROPN'},{'LOWER':'is'},{'LOWER':'strictly'},{'LOWER':'limited'},{'LOWER':'to'},{},{},{},{}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in span:
            if (str(word) != "is" and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == "is"):
                relationship = relationship + str(word) + ' '
                position = "relation"
            elif (position == "relation" and str(word)!="to"):
                relationship = relationship + str(word) + ' '
            elif (str(word) == "to"):
                relationship = relationship + str(word) + ' '
                position = "object"
            elif (position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship[:-1], object[:-1]))
    #define the pattern 
    pattern1 = [{'TEXT':'Although'}]
    pattern2 = [{'POS':'ADJ','DEP':'amod'},{'POS':'NOUN','DEP':'pobj'}]
    pattern3 = [{'DEP':'nsubjpass'},{'DEP':'auxpass'},{'DEP':'advmod'},{'DEP':'ccomp'},{'DEP':'prep'},{'DEP':'det'},{'DEP':'amod'},{'DEP':'pobj'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern1,pattern2,pattern3) 
    matches = matcher(doc) 
    if (len(matches)==4):
        span = doc[matches[0][1]:matches[0][2]]
        subject = str(doc[matches[1][1]:matches[1][2]])
        object = str(doc[matches[2][1]:matches[2][2]])
        relationship = ''
        result.append((subject, relationship, object))
    return result

def example():
    result = []
    #define the pattern 
    pattern = [{'TEXT': 'Examples'},{'LOWER': 'of'},{'POS':'DET','DEP':'det'},{'POS':'NOUN','DEP':'pobj'},{'POS':'ADP','DEP':'prep'},{'POS':'NOUN','DEP':'pobj'}]
    pattern1 = [{'POS':'PROPN','DEP':'attr'}]
    pattern2 = [{'POS':'PROPN','DEP':'appos'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern,pattern1,pattern2) 
    matches = matcher(doc) 
    if (len(matches)==3):
        span = doc[matches[0][1]:matches[0][2]]
        subject = 'Lexical ontology'
        relationship = 'such as'
        object = str(doc[matches[1][1]]) + ' and '+ str(doc[matches[2][1]])
        result.append((subject, relationship, object))
    return result

def different():
    result = []
    #define the pattern 
    pattern = [{'TEXT':'Unlike'},{'POS':'ADJ'},{'POS':'NOUN'},{},{},{},{},{},{},{},{},{'POS':'PUNCT'}]
    # Matcher class object 
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc) 
    if (matches != []):
        span = doc[matches[0][1]:matches[0][2]]
        subject = relationship = object = ''
        position = "subject"
        for word in doc:
            if (str(word) != "," and position == "subject"):
                subject = subject + str(word) + ' '
            elif (str(word) == ","):
                relationship = 'unlike'
                position = "object"
            elif (str(word) != "," and position == "object"):
                object = object + str(word) + ' '
        result.append((subject[:-1], relationship, object[:-3]))
    return result

#Output the SPO triple to a structured document
with open('C:/Users/lenovo/Desktop/FYP_extract/SPO_result.txt','a',encoding='utf-8') as f:
    for sentence in text:
        doc = nlp(sentence) # create a spaCy object
        if(definition() != []):
            for result1 in definition():
                if(len(result1)==3):
                    f.write("<Subject>"+str(result1[0])+"<Subject>"+"\n")
                    f.write("<definition>"+str(result1[1])+"<definition>"+"\n")
                    f.write("<Object>"+str(result1[2])+"<Object>"+"\n")
                    f.write("\n")
            print(definition())
        if(has_part() != []):
            for result1 in has_part():
                if(len(result1)==3):
                    f.write("<Subject>"+str(result1[0])+"<Subject>"+"\n")
                    f.write("<has_part>"+str(result1[1])+"<has_part>"+"\n")
                    f.write("<Object>"+str(result1[2])+"<Object>"+"\n")
                    f.write("\n")
            print(has_part())
        if(the_same_thing() != []):
            for result1 in the_same_thing():
                if(len(result1)==3):
                    f.write("<Subject>"+str(result1[0])+"<Subject>"+"\n")
                    f.write("<the_same_thing>"+str(result1[1])+"<the_same_thing>"+"\n")
                    f.write("<Object>"+str(result1[2])+"<Object>"+"\n")
                    f.write("\n")
            print(the_same_thing())
        if(represent() != []):
            for result1 in represent():
                if(len(result1)==3):
                    f.write("<Subject>"+str(result1[0])+"<Subject>"+"\n")
                    f.write("<represent>"+str(result1[1])+"<represent>"+"\n")
                    f.write("<Object>"+str(result1[2])+"<Object>"+"\n")
                    f.write("\n")
            print(represent())
        if(reason() != []):
            for result1 in reason():
                if(len(result1)==3):
                    f.write("<Subject>"+str(result1[0])+"<Subject>"+"\n")
                    f.write("<reason>"+str(result1[1])+"<reason>"+"\n")
                    f.write("<Object>"+str(result1[2])+"<Object>"+"\n")
                    f.write("\n")
            print(reason())
        if(method() != [] and method() !=None):
            for result1 in method():
                if(len(result1)==3):
                    f.write("<Subject>"+str(result1[0])+"<Subject>"+"\n")
                    f.write("<method>"+str(result1[1])+"<method>"+"\n")
                    f.write("<Object>"+str(result1[2])+"<Object>"+"\n")
                    f.write("\n")
            print(method())
        if(use_to() != []):
            for result1 in use_to():
                if(len(result1)==3):
                    f.write("<Subject>"+str(result1[0])+"<Subject>"+"\n")
                    f.write("<use_to>"+str(result1[1])+"<use_to>"+"\n")
                    f.write("<Object>"+str(result1[2])+"<Object>"+"\n")
                    f.write("\n")
            print(use_to())
        if(developer() != []):
            for result1 in developer():
                if(len(result1)==3):
                    f.write("<Subject>"+str(result1[0])+"<Subject>"+"\n")
                    f.write("<developer>"+str(result1[1])+"<developer>"+"\n")
                    f.write("<Object>"+str(result1[2])+"<Object>"+"\n")
                    f.write("\n")
            print(developer())
        if(drawback() != []):
            for result1 in drawback():
                if(len(result1)==3):
                    f.write("<Subject>"+str(result1[0])+"<Subject>"+"\n")
                    f.write("<drawback>"+str(result1[1])+"<drawback>"+"\n")
                    f.write("<Object>"+str(result1[2])+"<Object>"+"\n")
                    f.write("\n")
            print(drawback())
        if(example() != []):
            for result1 in example():
                if(len(result1)==3):
                    f.write("<Subject>"+str(result1[0])+"<Subject>"+"\n")
                    f.write("<example>"+str(result1[1])+"<example>"+"\n")
                    f.write("<Object>"+str(result1[2])+"<Object>"+"\n")
                    f.write("\n")
            print(example())
        if(different() != []):
            for result1 in different():
                if(len(result1)==3):
                    f.write("<Subject>"+str(result1[0])+"<Subject>"+"\n")
                    f.write("<different>"+str(result1[1])+"<different>"+"\n")
                    f.write("<Object>"+str(result1[2])+"<Object>"+"\n")
                    f.write("\n")
            print(different())
