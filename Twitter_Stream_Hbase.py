# Import needed libraries
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import csv
import json
import json
import happybase
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#Give the credentials of your twitter app that you've created
ckey= 'consumer key'
csecret= 'consumer secret'
atoken= 'access token'
asecret= 'access token secret'

#Initialise the infos about your Hbase 
batch_size = 1000
host = "127.0.0.1" #precise the ip adress of your hbase server
namespace = "hbase_namespace" 
table_name = "hbae_table_name"


def connect_to_hbase():    
    conn = happybase.Connection(host = host,
        table_prefix = namespace,
        table_prefix_separator = ":")
    conn.open()
    table = conn.table(table_name)
    batch = table.batch(batch_size = batch_size)
    return conn, batch

#This function transfrom the Json data row into a bacht form supported by Hbase
def insert_row(batch, row):
    batch.put(str(row[0]),{
               "TweetData:truncated": str(row[1]), 
               "TweetData:text": str(row[2]),
               "TweetData:is_quote_status":str(row[3]),
               "TweetData:in_reply_to_status_id": str(row[4]), 
               "TweetData:id": str(row[5]),
               "TweetData:favorite_count":str(row[6]),
               "TweetData:retweeted":str(row[7]),
               "TweetData:coordinates": str(row[8]),
               "TweetData:source":str(row[9]),
               "TweetData:in_reply_to_screen_name": str(row[10]), 
               "TweetData:in_reply_to_user_id": str(row[11]),
               "TweetData:retweet_count":str(row[12]),
               "TweetData:id_str": str(row[13]), 
               "TweetData:favorited": str(row[14]),               
               "TweetData:user_followers": str(row[15]), 
               "TweetData:user_location": str(row[16]),
               "TweetData:user_name":str(row[17]),
               "TweetData:geo": str(row[18]), 
               "TweetData:in_reply_to_user_id_str": str(row[19]),
               "TweetData:lang":str(row[20]),
               "TweetData:created_at": str(row[21]),
               "TweetData:in_reply_to_status_id_str": str(row[22]),
               "TweetData:place": str(row[23])})



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
    #@ each time that a new data is captured from twitter, we should transform the json form into list data
    #then, we pass it into the processTweetSearch function defined above
    # so to get a record with the nedded fields, 
    # after that, we insert it into Hbase via the function insert_row which add into a bach, then we store the bach into Hbase.
    def on_data(self, data):        
        tweet=json.loads(data)
        row=processTweetSearch(tweet)
        insert_row(batch, row)
        batch.send()
        print("yes")
        return True
    # in case of error, we return this message
    def on_error (self, status):
        print "erreur: %s",status

#Initialize a connection into Hbase
conn, batch = connect_to_hbase()
print "Connect to HBase. table name:batch size"

#We strat listening into Twitter data
auth= OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream=Stream(auth, listener())
twitterStream.filter(track=["key word1","key word2",...]) # here we should specify a key word, or a set of key words that we will use for searchning data in twiter.
