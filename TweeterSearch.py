from TwitterSearch import *
import json
import datetime
import csv
import time

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# this function return a tuple containing the diffrents fields of a tweet according to my need.
#Of course you can add other fields if needed
def processTweetSearch(tweet):    	
        contributors=tweet['contributors'] 
	truncated=tweet['truncated'] 
	text=tweet['text'] 
	is_quote_status=tweet['is_quote_status'] 
	in_reply_to_status_id=tweet['in_reply_to_status_id']  
	id=tweet['id']  
	favorite_count=tweet['favorite_count']  	
	retweeted=tweet['retweeted']  
	coordinates=tweet['coordinates']  
	source=tweet['source']  
	in_reply_to_screen_name=tweet['in_reply_to_screen_name'] 
	in_reply_to_user_id=tweet['in_reply_to_user_id']  
	retweet_count=tweet['retweet_count']  
	id_str=tweet['id_str'] 
	favorited=tweet['favorited']  
	user_followers=tweet['user']['followers_count']
        user_location=tweet['user']['location']
        user_name=tweet['user']['screen_name']
	geo=tweet['geo'] 
	in_reply_to_user_id_str=tweet['in_reply_to_user_id_str']  	
	lang=tweet['lang'] 
	created_at=tweet['created_at'] 
	in_reply_to_status_id_str=tweet['in_reply_to_status_id_str']  
	place=tweet['place'] 

        return (contributors, truncated, text, is_quote_status, in_reply_to_status_id, id, favorite_count, retweeted, coordinates, source, in_reply_to_screen_name,in_reply_to_user_id, retweet_count, id_str,favorited, retweeted,      user_followers,user_location,user_name, geo, in_reply_to_user_id_str, lang,  created_at, in_reply_to_status_id_str, place)

   
with open('Brandt.dz_Tweeter.csv', 'wb') as file:
      i=0        
      w = csv.writer(file)        
      w.writerow(["contributors", "truncated", "text","is_quote_status", "in_reply_to_status_id", "id", "favorite_count", "retweeted", "coordinates", "source", "in_reply_to_screen_name", "in_reply_to_user_id", "retweet_count","id_str", "favorited", "retweeted", "user_followers","user_location","user_name","geo","in_reply_to_user_id_str", "lang", "created_at", "in_reply_to_status_id_str", "place"])                
            
      print "Scraping Tweeter Page: \n"        
      tso = TwitterSearchOrder() 
      tso.set_keywords(['keyWORD'])    #Give here the diffrent key words to filter the returned tweets      
      tso.set_include_entities(False)         
      ts = TwitterSearch( #Put here the access tokeN, and the keys of your twitter app.
        	consumer_key='ck',
        	consumer_secret='cs',
        	access_token='at',
        	access_token_secret='ats'         
        )
      for tweet in ts.search_tweets_iterable(tso):             
            w.writerow(processTweetSearch(tweet))  # insert the fields in the CSV file.             

print "\nDone!Statuses Processed " 
