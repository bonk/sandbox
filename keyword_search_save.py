#!/usr/bin/env python
# -*- coding=utf-8 -*-

import tweepy
import sqlite3
import random
import datetime
import locale
import re
import sys
import codecs
from textwrap import TextWrapper
import time

argvs = sys.argv  # コマンドライン引数を格納したリストの取得
argc = len(argvs) # 引数の個数

sqlite3file='./twitter_' + argvs[1] + '_log.sqlite'
credential = {
    'CONSUMER_KEY': argvs[2],
    'CONSUMER_SECRET': argvs[3],
    'ACCESS_KEY': argvs[4],
    'ACCESS_SECRET': argvs[5]}
maxcount=-1

# http://apiwiki.twitter.com/HTTP-Response-Codes-and-Errors
tweepy_error = {"OK":200,
"Not Modified":304,
"Bad Request": 400,
"Unauthorized": 401,
"Forbidden": 403,
"Not Found": 404,
"Not Acceptable": 406,
"Enhance Your Calm": 420,
"Internal Server Error": 500,
"Bad Gateway": 502,
"Service Unavailable": 503}
#authentication
try:
    auth = tweepy.OAuthHandler(credential['CONSUMER_KEY'], credential['CONSUMER_SECRET'])
    auth.set_access_token(credential['ACCESS_KEY'], credential['ACCESS_SECRET'])
    api = tweepy.API(auth)
except:
    print "Authentication Error."
    exit()
#getting remaining api hit count
def print_rate_limit ():
    api_limit = api.rate_limit_status()
    remain=api_limit['remaining_hits']
    print "Api limit to: " + str(remain)
#tweet = api.search(argvs[6])
#print tweet[0].text
#print tweet[1].text
#exit;
#getting remaining api hit count
def print_rate_limit ():
    api_limit = api.rate_limit_status()
    remain=api_limit['remaining_hits']
    print "Api limit to: " + str(remain)
#create a database if not exists
conn = sqlite3.connect(sqlite3file)
cur = conn.cursor() 
cur.execute("CREATE TABLE IF NOT EXISTS mystatus (userid long, screenname text, username text, statusid long, postdate text, text text, replyto text, replyto_id long, reply_status_id long, favorite integer, primary key (statusid))")
#to save tweets of myself
print "Getting your tweets..."
try:
    print "try"
    cur.execute("select max(statusid) from mystatus")
    maxsaved=cur.fetchone()[0]
    if not maxsaved:
        print "notmaxsaved"
        maxsaved=1
    q = argvs[6]
    for p in tweepy.Cursor(api.search, q, show_user = True, since_id=maxsaved).items(maxcount):
        print "in for"
        #if ( not p.author ) and ( not p.in_replay_to_user_id ):
        #    cur.execute("INSERT INTO mystatus (userid, screenname, username, statusid, postdate, text, replyto, replyto_id, reply_status_id) values (?,?,?,?,?,?,?,?,?)",  (p.author.id, p.author.screen_name, p.author.name, p.id, p.created_at, p.text, p.in_reply_to_screen_name, p.in_reply_to_user_id, p.in_reply_to_status_id) )
        #else:
        #    cur.execute("INSERT INTO mystatus (userid, screenname, username, statusid, postdate, text, replyto, replyto_id, reply_status_id) values (?,?,?,?,?,?,?,?,?)",  ("", "", "", p.id, p.created_at, p.text, "", "", "") )
        cur.execute("select count(statusid) from mystatus where statusid = " + str(p.id))
        now_id=cur.fetchone()[0]
        if now_id <= 0:
            cur.execute("INSERT INTO mystatus (userid, screenname, username, statusid, postdate, text, replyto, replyto_id, reply_status_id) values (?,?,?,?,?,?,?,?,?)",  ("", "", "", p.id, p.created_at, p.text, "", "", "") )
        print  str(p.id)+ " "
except tweepy.error.TweepError, e:
    if e.response.status == tweepy_error['Bad Request']:
        print 'Rate limit exceeded. Try later and get the rest.'
        conn.commit()
        conn.close()
        print_rate_limit()
        exit()
    elif e.response.status == tweepy_error['Forbidden']: #ブロックコメントの処理追加 20110314
        print 'probubry you are blocked.'
    else:
        raise

conn.commit()

conn.close()
print_rate_limit ()
