# Import needed libraries
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import csv
import json

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#Give the credentials of your twitter app that you've created
ckey= 'consumer key'
csecret= 'consumer secret'
atoken= 'access token'
asecret= 'access token secret'

#This function return a record with different fileds from the twitter data captured (tweet)
def processTweetSearch(tweet):            
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

        return (truncated, text, is_quote_status, in_reply_to_status_id, id, favorite_count, retweeted, coordinates, source, in_reply_to_screen_name,in_reply_to_user_id, retweet_count, id_str,favorited, retweeted,      user_followers,user_location,user_name, geo, in_reply_to_user_id_str, lang,  created_at, in_reply_to_status_id_str, place)

#At this level we redefine the class listner, mainly the functions on-data & on-error
class listener (StreamListener):
    #@ each time that a new data is captured from twitter, we pass it into the processTweetSearch function defined above
    # so to get a record weith the nedded fields, 
    # then we write it at the end of the CSV file
    def on_data(self, data):        
        file=open('/url file/name_file.csv', 'ab') # open the csv file in updating mode (create a new line at the end of the file)
        w = csv.writer(file)
        tweet=json.loads(data)
        w.writerow(processTweetSearch(tweet))
        file.close()
        return True
    # in case of error, we return this message
    def on_error (self, status):
        print "erreur: %s",status

file=open('/url file/name_file.csv', 'ab')
w = csv.writer(file)        
w.writerow(["truncated", "text","is_quote_status", "in_reply_to_status_id", "id", "favorite_count", "retweeted", "coordinates", "source", "in_reply_to_screen_name", "in_reply_to_user_id", "retweet_count","id_str", "favorited", "retweeted", "user_followers","user_location","user_name","geo","in_reply_to_user_id_str", "lang", "created_at", "in_reply_to_status_id_str", "place"])                
file.close()     
auth= OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream=Stream(auth, listener())
twitterStream.filter(track=["key word1","key word2",...]) # here we should specify a key word, or a set of key words that we will use for searchning data in twiter.
