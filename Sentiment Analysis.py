#We import all the needed librairies 
import pandas as pd  #we use this library to import data from CSV as a Dataframe
import csv
import json
from textblob import TextBlob # Textblob is a library used to treat & analyze english text
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer #extblob_fr is used to treat & analyze french text
from textblob.sentiments import NaiveBayesAnalyzer #we use the naive bayes algorithm to do sentiment analysis
import re

#This function return the value of the sentiment (0 neutre, 1: positive, -1: negative). the input is the text , and the language of the statement
def on_data(tweet, lang):
    #we declare the global variables 
    global positive
    global negative
    global compound
    global count
    count+=1
    senti=0
    sentimentdata=0
    
    if (lang=='en'):
        tweet=" ".join(re.findall("[a-zA-Z]+",tweet))
        blob=TextBlob(tweet.strip(),analyzer=NaiveBayesAnalyzer())    #here I speciified Naive bayes 

        for sen in blob.sentences:           
            if sen.sentiment.classification =='pos':
                positive=positive+1
                sentimentdata=1
            elif sen.sentiment.classification=='neg':
                negative=negative+1
                sentimentdata=-1
            else:
                compound=compound+1 
                sentimentdata=0
                
    elif (lang=='fr'):
        tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()) #Here I choose PatternAnalyzer 
        blob1 = tb(tweet)
        sentim=blob1.sentiment        
        if (sentim[0])>0.0:
            positive=positive+1
            sentimentdata= 1            

        elif (sentim[0])<0.0:
            negative=negative+1
            sentimentdata=-1
        elif (sentim[0])==0.0:
            compound=compound+1  
            sentimentdata=0
            
    elif (lang=='ar'):
        blob=TextBlob(tweet)
        tweet=blob.translate(to='en')  #we translate the arab text into english     
        
        tweet=" ".join(re.findall("[a-zA-Z]+",str(tweet)))
        blob=TextBlob(tweet.strip(),analyzer=NaiveBayesAnalyzer())     

        for sen in blob.sentences:
            
            if sen.sentiment.classification=='pos':
                positive=positive+1
                sentimentdata=1
            elif sen.sentiment.classification=='neg':
                negative=negative+1
                sentimentdata=-1
            else:
                compound=compound+1
                sentimentdata=0
    return (int(sentimentdata))

#Import the CSV file as a DataFrame
Tweets=pd.read_csv('url_file/name_file.csv', delimiter=',', encoding="utf-8", index_col=False)
#I add this column for sentiment , and I initialze it to 0
Tweets['sentiment']=0
for i in range(len(Tweets['text'])):    
    Tweets['sentiment'][i]=on_data(Tweets['text'][i],Tweets['lang'][i])
    print(Tweets['text'][i])
    print (Tweets['sentiment'][i])

