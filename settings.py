# -*- coding: utf-8 -*-

DB_NAME = "VNLaw_development"
USER_NAME = "anhtt"
HOST_NAME = "localhost"
HOST_PASS = "12345678"

INPUT_DATA_FILE_NAME = "./input/articles.tsv"
PROCESSED_INPUT_DATA_FILE_NAME = "./topmine/input/data.txt"
INPUT_STOPWORDS_FILE_NAME = "./input/vietnamese-stopwords.txt"
PROCESSED_INPUT_STOPWORDS_FILE_NAME = "./topmine/topmine_src/stopwords.txt"

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
  INSERT INTO articles(article_id) VALUES(%s);
"""
QUERY_INSERT_INTO_ARTICLE_TOPICS = """
  INSERT INTO article_topics(topic_id, article_id) VALUES(%s, %s);
"""
QUERY_INSERT_TO_TOPICS = """
  INSERT INTO topics(id, value) VALUES(%s, %s);
"""
QUERY_SELECT_ARTICLE_ID = """
  SELECT article_id FROM articles;
"""
