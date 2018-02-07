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

REDUNDANT_SYMBOL = ["\\t", "\\r", "\\n", "\\\\", "##", "\\",
  "**___________________**", "**", "---", "_", "|", "…",
  "---|---|---|---|---"]
REDUNDANT_PATTERN = ["[a-z]\)", "đ\)", "&amp",
  "(\d+\/)*([A-Z\d\%\-a-z]+)+(\&[a-z]+\;([a-z]+\=[A-Za-z\d]+)+)+\"",
  "([a-z]+\=\"[a-z_]+\"\&[a-z;]+)+",
  "((\)\;)+[a-z\-\:\;\"]+)+", "([a-z]+\=\".*\-)+",
  "(right:[a-z\d]+\;)(color\:[a-z\(\d\,\s]+)"]

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

translate_map = {
  ord(u'Á'): u'á',
  ord(u'À'): u'à',
  ord(u'Ạ'): u'ạ',
  ord(u'Ả'): u'ả',
  ord(u'Ã'): u'ã',
  ord(u'Â'): u'â',
  ord(u'Ấ'): u'ấ',
  ord(u'Ầ'): u'ầ',
  ord(u'Ậ'): u'ậ',
  ord(u'Ẩ'): u'ẩ',
  ord(u'Ẫ'): u'ẫ',
  ord(u'Ă'): u'ă',
  ord(u'Ắ'): u'ắ',
  ord(u'Ằ'): u'ằ',
  ord(u'Ặ'): u'ặ',
  ord(u'Ẳ'): u'ẳ',
  ord(u'Ẵ'): u'ẵ',
  ord(u'É'): u'é',
  ord(u'È'): u'è',
  ord(u'Ẹ'): u'ẹ',
  ord(u'Ẻ'): u'ẻ',
  ord(u'Ẽ'): u'ẽ',
  ord(u'Ê'): u'ê',
  ord(u'Ế'): u'ế',
  ord(u'Ề'): u'ề',
  ord(u'Ệ'): u'ệ',
  ord(u'Ể'): u'ể',
  ord(u'Ễ'): u'ễ',
  ord(u'Ó'): u'ó',
  ord(u'Ò'): u'ò',
  ord(u'Ọ'): u'ọ',
  ord(u'Ỏ'): u'ỏ',
  ord(u'Õ'): u'õ',
  ord(u'Ô'): u'ô',
  ord(u'Ố'): u'ố',
  ord(u'Ồ'): u'ồ',
  ord(u'Ộ'): u'ộ',
  ord(u'Ổ'): u'ổ',
  ord(u'Ỗ'): u'ỗ',
  ord(u'Ơ'): u'ơ',
  ord(u'Ớ'): u'ớ',
  ord(u'Ờ'): u'ờ',
  ord(u'Ợ'): u'ợ',
  ord(u'Ở'): u'ở',
  ord(u'Ỡ'): u'ỡ',
  ord(u'Ú'): u'ú',
  ord(u'Ù'): u'ù',
  ord(u'Ụ'): u'ụ',
  ord(u'Ủ'): u'ủ',
  ord(u'Ũ'): u'ũ',
  ord(u'Ư'): u'ư',
  ord(u'Ứ'): u'ứ',
  ord(u'Ừ'): u'ừ',
  ord(u'Ự'): u'ự',
  ord(u'Ử'): u'ử',
  ord(u'Ữ'): u'ữ',
  ord(u'Í'): u'í',
  ord(u'Ì'): u'ì',
  ord(u'Ị'): u'ị',
  ord(u'Ỉ'): u'ỉ',
  ord(u'Ĩ'): u'ĩ',
  ord(u'Đ'): u'đ',
  ord(u'Ý'): u'ý',
  ord(u'Ỳ'): u'ỳ',
  ord(u'Ỵ'): u'ỵ',
  ord(u'Ỷ'): u'ỷ',
  ord(u'Ỹ'): u'ỹ',
}
