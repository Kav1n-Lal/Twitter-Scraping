import streamlit as st                        #GUI
import snscrape.modules.twitter as sntwitter  #scraping library
import pandas as pd                           #dataframe
import pymongo                                #connect to mongodb 
import json                                   #read json data
import datetime                               #formatting

st.title(':blue[TWITTER SCRAPING]')
form=st.form('TWITTER SCRAPING')
keywords=form.text_input(':violet[Enter your keyword/Hashtag]')
maxTweets = form.number_input(':violet[Tweet_count]',min_value=1,max_value=1000,value=50,step=50)
sinc=form.date_input(':violet[Enter the starting date]')
sin=str(sinc)
st1='since:'+sin
unti=form.date_input(':violet[Enter the ending date]')
unt=str(unti)
st2='until:'+unt
ok=form.form_submit_button('OK')
less_year=int(sin[:4])
great_year=int(unt[:4]) 
less_date=int(sin[-2:])
great_date=int(unt[-2:])
st3=keywords+' '+st1+' '+st2

current_time = datetime.datetime.now()
time_stamp = current_time.timestamp()
from datetime import datetime 
date_time = datetime.fromtimestamp(time_stamp)


def JSON_FORMAT():
    if keywords=='':
        st.warning('Please Enter Some Keyword :thinking_face:')
        st.warning('Starting date must be older than ending date! :thinking_face:')
    else:
        st.success("Please wait! fetching data")
        tweets_list_comb=[]
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(st3).get_items()):
                if i>maxTweets-1:
                    break
                tweets_list_comb.append({"Datetime":str(tweet.date),"Hashtags":str(tweet.hashtags),"Tweet Id":str(tweet.id),
                                    "Text":str(tweet.content),"Username":str(tweet.user.username),
                                    "Like Count":str(tweet.likeCount),"Display Name":str(tweet.user.displayname),
                                    "Language":str(tweet.lang),"RetweetCount":str(tweet.retweetCount),
                                    "InReplyToUser":str(tweet.inReplyToUser),"SourceLabel":str(tweet.sourceLabel)})

        st4=str(date_time)+' '+'-'+str(maxTweets)+' '+'scraped data of'+' '+st3  
        data={str(st4):tweets_list_comb}
        json_string = json.dumps(data)
        st.write(':point_down: **Scraped Data In JSON Format** ')
        st.json(json_string, expanded=False)
        f1_name=st4+'.'+'json'
        st.download_button(label="**Download JSON**",
                                file_name=f1_name,
                                mime="application/json",
                                data=(json_string)
                                )    
        def upload():
                    client = pymongo.MongoClient("mongodb+srv://KPKAVIN:kasaan@cluster0.3bc5s5h.mongodb.net/?retryWrites=true&w=majority")
                    db=client.Streamlit
                    db.st_col.insert_one(data)
                    st.success('Successfully uploaded to database')
        up=st.button('**Press Here to upload data**',on_click=upload)    
    
def DATAFRAME_FORMAT():
    if keywords=='':
        st.warning('Please Enter Some Keyword') 
        st.warning('Starting date must be older than ending date!')
    else:
        st.success("Please wait! fetching data")
        # Using TwitterSearchScraper to scrape data and append tweets to list
        tweets_list2 = []
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(st3).get_items()):
                if i>maxTweets-1:
                    break
                tweets_list2.append([tweet.date,tweet.hashtags,tweet.id,
                                    tweet.content,tweet.user.username,
                                    tweet.likeCount,tweet.user.displayname,
                                    tweet.lang,tweet.retweetCount,
                                    tweet.inReplyToUser,tweet.sourceLabel])
                
            # Creating a dataframe from the tweets list above
        tweets_df3 = pd.DataFrame(tweets_list2, columns=['Datetime','Hashtags','Tweet Id', 
                                                            'Text', 'Username', 'Like Count', 
                                                            'Display Name', 'Language',
                                                    'RetweetCount','InReplyToUser','SourceLabel'])        
        
        st.write(':point_down: **Scraped Data In A Table** ')
        st.dataframe(tweets_df3)
        df = tweets_df3
        @st.experimental_memo
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        st4=str(date_time)+' '+'-'+str(maxTweets)+' '+'scraped data of'+' '+st3   
        csv = convert_df(df)
        f_name=st4+'.'+'csv'
        st.download_button(
        "**Download CSV**",
        csv,
        f_name,
        "text/csv",
        key='download-csv'
        )

if 'key' not in st.session_state:
            st.session_state['key']=JSON_FORMAT()

table=st.button('**Press Here to View and Download in CSV**')
json_format=st.button('**Press Here To View, Upload and Download in JSON**')
if table:
                    st.session_state.key=DATAFRAME_FORMAT()   
if json_format:
                    st.session_state.key=JSON_FORMAT()
    
                                  
    

if ok:
    if keywords=="" :
            st.warning('Enter keyword field! :thinking_face:')
    if less_year>great_year :
            st.warning('Starting YEAR must be older than ending YEAR! 	:thinking_face:')
    elif (less_year==great_year) and (less_date==great_date):
            st.warning('Starting date must be LESSER than ending date! 	:thinking_face:')
    
    elif keywords!="" and (less_year<great_year):
        JSON_FORMAT()
        
    elif keywords!="" and (less_year==great_year) and (less_date<great_date):
        JSON_FORMAT()
        
        
    


    


 