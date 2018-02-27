# -*- coding: utf-8 -*-

DB_NAME = "VNLaw_development"
USER_NAME = "anhtt"
HOST_NAME = "localhost"
HOST_PASS = "12345678"

INPUT_DATA_FILE_NAME = "./input/articles.tsv"
PROCESSED_INPUT_DATA_FILE_NAME = "./topmine/input/data.txt"
INPUT_STOPWORDS_FILE_NAME = "./input/vietnamese-stopwords.txt"
PROCESSED_INPUT_STOPWORDS_FILE_NAME = "./topmine/topmine_src/stopwords.txt"

PARTITION_DOCS_FILE_NAME = "intermediate_output/partitioneddocs.txt"
VOCAB_FILE_NAME = "intermediate_output/vocab.txt"
PHRASE_TOPICS_FILE_NAME = "intermediate_output/phrase_topics.txt"
FREQUENT_PHRASES_FILE_NAME = "output/frequent_phrases.txt"
NEIGHBOR_ARTICLES_FILE_NAME = "output/neighbor_articles.txt"
PHRASE_TOPICS_PRO_FILE_NAME = "output/phrase_topics_pro.txt"
KEYWORD_TOPICS_DIS_FILE_NAME = "output/keyword_topics_distribution.txt"

PARAM_BUILD_DATA = "build_data"
PARAM_BUILD_SW = "build_stopwords"

REDUNDANT_SYMBOL = ["\\t", "\\r", "\\n", "##", "\\", "”",
  "**___________________**", "**", "---", "_", "|", "…",
  "---|---|---|---|---"]

REDUNDANT_PATTERN = ["[a-z]\)", "đ\)", "&amp",
  "(\d+\/)*([A-Z\d\%\-a-z]+)+(\&[a-z]+\;([a-z]+\=[A-Za-z\d]+)+)+\"",
  "([a-z]+\=\"[a-z_]+\"\&[a-z;]+)+",
  "((\)\;)+[a-z\-\:\;\"]+)+", "([a-z]+\=\".*\-)+",
  "(right:[a-z\d]+\;)(color\:[a-z\(\d\,\s]+)"]

REDUNDANT_STRING_PATTERN = ["điều \d{1,2}", "khoản \d{1,2}",
  "chương [ivxlcdm]+", "điểm \d{1,2}",
  "phần thứ [a-zâấưăáảáíờộơ ]+", "mục \d{1,2}",
  "cộng hoà xã hội chủ nghĩa việt nam", "độc lập - tự do - hạnh phúc",
  "\d{1,2}\\\.", "[\w]\)", "đ\)"]

FORBIDEN_SYMBOL_TOPICS = ["_", "%", "|", "\\", ":"]

QUERY_INSERT_AI_TO_ARTICLES = """
  INSERT INTO articles(article_id, created_at, updated_at)
    VALUES(%s, %s, %s);
"""

QUERY_INSERT_INTO_ARTICLE_TOPICS = """
  INSERT INTO articles_topics(article_id, topics, created_at, updated_at)
    VALUES(%s, %s, %s, %s);
"""

QUERY_INSERT_INTO_ARTICLE_NEIGHBORS = """
  INSERT INTO article_neighbors(source_id, neighbor_id, level, created_at, updated_at)
    VALUES(%s, %s, %s, %s, %s);
"""

QUERY_SELECT_ARTICLES_ID = """
  SELECT article_id FROM articles;
"""
