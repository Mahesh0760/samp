from pytrends.request import TrendReq
from newsapi import NewsApiClient
import pandas as pd
import datetime
import sqlite3
import os


def users_db_fetch():
    nw_db = sqlite3.connect("users.db")
    db_cur = nw_db.cursor()
    db_cur.execute("SELECT * FROM users")
    nw = db_cur.fetchall()

    for n in nw:
        print('\n\nUsername:     ', n[0], '\nFullname:      ', n[1],'\nemail:         ', n[2], '\nPassword:        ', n[3])
        print('Location:   ', n[4], '\nCat1:    ', n[5], '\nCat2:    ', n[6], '\nCat3:    ', n[7])

    nw_db.commit()
    nw_db.close()


def news_fetch1(cat, loc, key):
    nw_dt = datetime.datetime.now()
    nw_dt = nw_dt.date()

    newsapi = NewsApiClient(api_key=key)

    nw_db = sqlite3.connect("new_db.db")
    db_cur = nw_db.cursor()
    db_cur.execute("SELECT * FROM news_data")
    dt = db_cur.fetchall()
    id = len(dt) + 1

    pytrend = TrendReq()
    tr_keys = pytrend.trending_searches(loc)
    x1 = len(tr_keys)

    for x in range(x1):
        kw4 = tr_keys.iloc[x, 0]
        print(kw4)
        nw_key = newsapi.get_top_headlines(q=kw4, category=cat, language='en', page_size=3)
        nw_art = nw_key['articles']
        nw_art_sz = len(nw_art)
        if nw_art_sz != 0:
            for i in range(nw_art_sz):
                nw_t = nw_art[i]['title']
                nw_desc = nw_art[i]['description']
                nw_link = nw_art[i]['url']
                print(nw_t)
                print(nw_desc)
                print(nw_link)
                db_cur.execute("INSERT INTO news_data VALUES (?,?,?,?,?,?,?)", (id, cat, loc, nw_dt, nw_t, nw_desc, nw_link))
                id = id+1

    nw_db.commit()
    nw_db.close()

    print('Successfully updated NEWS database with country: ', loc, ' and category: ', cat)


def news_fetch2(cat1, cat2, loc1, loc2, key):
    nw_dt = datetime.datetime.now()
    nw_dt = nw_dt.date()
    temp = pd.DataFrame()
    tp2 = type(temp)

    newsapi = NewsApiClient(api_key=key)

    nw_db = sqlite3.connect("new_db.db")
    db_cur = nw_db.cursor()
    db_cur.execute("SELECT * FROM news_data")
    dt = db_cur.fetchall()
    id = len(dt) + 1

    os.system('cls')
    pytrend = TrendReq()
    tr_keys = pytrend.realtime_trending_searches(loc2)
    x1 = len(tr_keys)

    if x1 > 30:
        x1 = 30

    for x in range(x1):
        kw3 = tr_keys.iloc[x, 0]
        kw4 = kw3.rsplit(",")
        kw5 = kw4[1:5]
        print(kw5)
        pytrend.build_payload(kw5, timeframe='now 1-d')
        rel_keys = pytrend.related_queries()
        rel_res1 = list(rel_keys.values())[0]['top']
        tp = type(rel_res1)
        if tp == tp2:
            rel_res2 = rel_res1['query'].iloc[0]
            print(rel_res2)
            nw_key = newsapi.get_top_headlines(q=rel_res2, language='en', page_size=3, category=cat1)
            nw_art = nw_key['articles']
            nw_art_sz = len(nw_art)
            if nw_art_sz != 0:
                for i in range(nw_art_sz):
                    nw_t = nw_art[i]['title']
                    nw_desc = nw_art[i]['description']
                    nw_link = nw_art[i]['url']
                    print(nw_t)
                    print(nw_desc)
                    print(nw_link)
                    db_cur.execute("INSERT INTO news_data VALUES (?,?,?,?,?,?,?)",
                                   (id, cat2, loc2, nw_dt, nw_t, nw_desc, nw_link))
                    id = id + 1

    nw_db.commit()
    nw_db.close()

    print('Successfully updated NEWS database with country: ', loc1, ' and category: ', cat1)