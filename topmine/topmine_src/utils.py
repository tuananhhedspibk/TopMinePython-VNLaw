# -*- coding: utf-8 -*-

from sklearn.metrics.pairwise import euclidean_distances

import sys
sys.path.insert(0, "/home/mylaptop/Program/GR/LDA/TopMine")
from settings import *

import re
import numpy as np

def store_partitioned_docs(partitioned_docs, path=PARTITION_DOCS_FILE_NAME):
  f = open(path, "w")
  for document in partitioned_docs:
    f.write(", ".join(" ".join(str(word) for word in phrase) for phrase in document))
    f.write("\n")

def load_partitioned_docs(path=PARTITION_DOCS_FILE_NAME):
  f = open(path, "r")
  partitioned_docs = []
  document_index = 0
  for line in f:
    line = line.strip()
    if len(line) < 1:
      continue
    phrases = line.split(", ")
    partitioned_doc = []
    for phrase in phrases:
      phrase_of_words = map(int,phrase.split(" "))
      partitioned_doc.append(phrase_of_words)
    partitioned_docs.append(partitioned_doc)
  return partitioned_docs

def store_vocab(index_vocab, path=VOCAB_FILE_NAME):
  """
  Stores vocabulary into a file.
  """
  f = open(VOCAB_FILE_NAME, "w")
  for word in index_vocab:
    f.write(word + "\n")
  f.close()

def load_vocab(path=VOCAB_FILE_NAME):
  """
  Loads vocabulary from a file.
  """
  f = open(path, "r")
  index_vocab = []
  index = 0
  for line in f:
      index_vocab.append(line.replace("\n", ""))
  return index_vocab

def store_frequent_phrases(frequent_phrases, path=FREQUENT_PHRASES_FILE_NAME):
  f = open(path, "w")
  for phrase, val in enumerate(frequent_phrases):
    f.write(str.format("{0} {1}\n",phrase, val))
  f.close()

def store_phrase_topics(document_phrase_topics, path=PHRASE_TOPICS_FILE_NAME):
  """
  Stores topic for each phrase in the document.
  """
  f = open(path, "w")
  for document in document_phrase_topics:
    f.write(",".join(str(phrase) for phrase in document))
    f.write("\n")

def store_most_frequent_topics(most_frequent_topics, prefix_path="output/topic"):
  for topic_index, topic in enumerate(most_frequent_topics):
    file_name = str.format("{0}{1}.txt", prefix_path, topic_index)
    f = open(file_name, "w")
    for phrase, val in topic:
      f.write(str.format("{0}\t{1}\n",phrase, val))
    f.close()

def handle_string(input):
  forbiden_symbol = ["%", ":", "_", "“", "/"]
  if input != None:
    input = input.decode("utf-8").lower()
    input = input.encode("utf-8")
    for symbol in forbiden_symbol:
      input = input.replace(symbol, " ")
    return input.strip()
  return None

def filter_most_important_topics(docs_topic_info, standard_lize):
  for doc in docs_topic_info:
    _sum = sum(doc)
    topics_filter_thres = float(sum(doc)) / float(len(doc))
    for idx, topic_count in enumerate(doc):
      if float(topic_count) / float(topics_filter_thres) < 1:
        doc[idx] = 0
      if standard_lize:
        doc[idx] = float(doc[idx]) / float(_sum)
  return docs_topic_info

def get_string_phrase(documents, doc_idx, phrase_idx, index_vocab):
  return _get_string_phrase(" ".join(str(word) for word in documents[doc_idx][phrase_idx]), index_vocab)

def extract_most_frequent_phrase(topics, documents, doc_idx, phrase_index, index_vocab, ph_tp, forceAll):
  ex_phrase = get_string_phrase(documents, doc_idx, phrase_index, index_vocab)
  topic_index = 0
  for topic in topics:
    if topic_index == ph_tp:
      if forceAll:
        for phrase, val in topic.most_common():
          if len(phrase.split(" ")) > 1:
            phrase_core_string = _get_string_phrase(phrase, index_vocab)
            if ex_phrase.decode("utf-8") == phrase_core_string.decode("utf-8"):
              return handle_string(ex_phrase)
      else:
        top_ct = 0
        for phrase, val in topic.most_common():
          if top_ct < 3:
            if len(phrase.split(" ")) > 1:
              phrase_core_string = _get_string_phrase(phrase, index_vocab)
              if ex_phrase.decode("utf-8") == phrase_core_string.decode("utf-8"):
                return handle_string(ex_phrase)
              top_ct += 1
      return ""
    topic_index += 1

def write_phrase_topics(documents_tp_ph_repre, document, doc_idx, docs_topic_info, topics, documents, index_vocab, ph_extracted_ct, f, forceAll):
  for phrase_idx, topic_index in enumerate(document):
    if docs_topic_info[doc_idx][topic_index] > 0:
      phrase_extracted = extract_most_frequent_phrase(topics, documents, doc_idx, phrase_idx, index_vocab, topic_index, forceAll)
      if phrase_extracted != "":
        already_had_phrase = False
        for topic, phrases_list in documents_tp_ph_repre[doc_idx].items():
          if phrase_extracted in phrases_list:
            already_had_phrase = True
            break
        if not already_had_phrase:
          ph_extracted_ct += 1
          documents_tp_ph_repre[doc_idx][topic_index].append(phrase_extracted)
          f.write(phrase_extracted + ",")
  return ph_extracted_ct

def store_phrase_topics_pro(documents, docs_topic_info, document_phrase_topics, index_vocab, num_topics, topics):
  output_file_name = PHRASE_TOPICS_PRO_FILE_NAME
  f = open(output_file_name, "w")
  docs_topic_info_standard = docs_topic_info
  filter_most_important_topics(docs_topic_info_standard, True)
  filter_most_important_topics(docs_topic_info, False)
  documents_tp_ph_repre = {}
  for doc_idx, document in enumerate(document_phrase_topics):
    ph_extracted_ct = 0
    documents_tp_ph_repre[doc_idx] = {}
    for i in range(num_topics):
      if docs_topic_info[doc_idx][i] > 0:
        documents_tp_ph_repre[doc_idx][i] = []
    ph_extracted_ct = write_phrase_topics(documents_tp_ph_repre, document, doc_idx, docs_topic_info, topics, documents, index_vocab, ph_extracted_ct, f, False)
    if ph_extracted_ct == 0:
      write_phrase_topics(documents_tp_ph_repre, document, doc_idx, docs_topic_info, topics, documents, index_vocab, ph_extracted_ct, f, True)
    f.write("\n")
  f.close()
  return docs_topic_info_standard

def compute_distance_between_articles(docs_topic_info):
  dis_array = np.array(euclidean_distances(docs_topic_info))
  recommend_results = np.argsort(dis_array)
  _store_neighbor_article(recommend_results)

def _store_neighbor_article(data):
  f = open(NEIGHBOR_ARTICLES_FILE_NAME, "w")
  for item in data:
    for article_idx in item:
      f.write(str(article_idx) + " ")
    f.write("\n")
  f.close()

def _get_string_phrase(phrase, index_vocab):
  """
  Returns the string representation of the phrase.
  """
  res = ""
  for vocab_id in phrase.split():
    if res == "":
      res += index_vocab[int(vocab_id)]
    else:
      res += " " + index_vocab[int(vocab_id)]
  return res
