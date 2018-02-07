import psycopg2
import os, glob
from settings import *

dir = os.path.dirname(__file__)

def filter_topics(topics):
  filtered_topics = []
  number_of_all_phrases = len(topics)
  for i in range(10):
    topic_count = topics.count(i)
    if topic_count > 0:
      if float(topic_count) / float(number_of_all_phrases) >= 0.1:
        filtered_topics.append(i)
  return filtered_topics

def dump_topics_list(db_con, cur):
  for file in os.listdir("./topmine/output"):
    if file.endswith(".txt") and "topic" in file:
      topic_id = file.split(".")[0][-1:]
      with open(os.path.join(dir, "./topmine/output/topic" + topic_id + ".txt")) as fp:
        ct = 0
        topics = ""
        for line in fp:
          topic = line.split("\t")[0]
          for symbol in FORBIDEN_SYMBOL_TOPICS:
            topic = topic.replace(symbol, " ")
          if ct == 0:
            topics += topic + ","
            ct += 1
          else:
            topics += topic
            break
      cur.execute(QUERY_INSERT_TO_TOPICS, (topic_id, topics))
      db_con.commit()

def dump_topics_for_doc(db_con, cur):
  cur.execute(QUERY_SELECT_ARTICLE_ID)
  articles_id = []
  for article_id in cur.fetchall():
    articles_id.append(article_id)
    
  with open(os.path.join(dir, "./topmine/intermediate_output/phrase_topics.txt")) as fp:
    output_data = ""
    for idx, line in enumerate(fp):
      data = line.split(",")
      topics = []
      for item in data:
        topics.append(int(item.rstrip()))
      topics = filter_topics(topics)
      for topic in topics:
        cur.execute(QUERY_INSERT_INTO_ARTICLE_TOPICS, (topic, articles_id[idx]))
      db_con.commit()

def main():
  db_con = psycopg2.connect(dbname=DB_NAME, user=USER_NAME,
    host=HOST_NAME, password=HOST_PASS)
  cur = db_con.cursor()
  #dump_topics_list(db_con, cur)
  dump_topics_for_doc(db_con, cur)
  cur.close()
  db_con.close()

if __name__ == "__main__":
    main()
