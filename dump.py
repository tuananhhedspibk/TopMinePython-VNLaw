from settings import *

import psycopg2
import os, glob
import datetime

dir = os.path.dirname(__file__)

def _fetch_all_articles_id(cur):
  cur.execute(QUERY_SELECT_ARTICLES_ID)
  articles_id = []
  for article_id in cur.fetchall():
    articles_id.append(article_id)
  return articles_id

def dump_topics_for_doc(db_con, cur):
  articles_id = _fetch_all_articles_id(cur)
    
  with open(os.path.join(dir, "./topmine/" + PHRASE_TOPICS_PRO_FILE_NAME)) as fp:
    output_data = ""
    for idx, line in enumerate(fp):
      cur.execute(QUERY_INSERT_INTO_ARTICLE_TOPICS,
        (articles_id[idx], line[:-1],
          datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
          datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    db_con.commit()

def dump_neighbor_article(db_con, cur):
  articles_id = _fetch_all_articles_id(cur)

  with open(os.path.join(dir, "./topmine/" + NEIGHBOR_ARTICLES_FILE_NAME)) as fp:
    for line in fp:
      article_neighbors_idx = line.split(" ")
      for i in range(1, 4):
        cur.execute(QUERY_INSERT_INTO_ARTICLE_NEIGHBORS,
          (articles_id[int(article_neighbors_idx[0])],
          articles_id[int(article_neighbors_idx[i])], i,
          datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
          datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    db_con.commit()

def main():
  db_con = psycopg2.connect(dbname=DB_NAME, user=USER_NAME,
    host=HOST_NAME, password=HOST_PASS)
  cur = db_con.cursor()
  dump_topics_for_doc(db_con, cur)
  dump_neighbor_article(db_con, cur)
  cur.close()
  db_con.close()

if __name__ == "__main__":
    main()
