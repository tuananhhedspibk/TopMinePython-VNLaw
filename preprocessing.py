# -*- coding: utf-8 -*-

from pyvi.pyvi import ViTokenizer
import sys
import re
import os
import psycopg2
from settings import *

dir = os.path.dirname(__file__)

def handle_string(input_string):

  input_string = input_string.decode("utf-8").lower().encode("utf-8")

  for pattern in REDUNDANT_STRING_PATTERN:
    input_string = re.sub(pattern, "", input_string)

  for symbol in REDUNDANT_SYMBOL:
    if symbol == "\\n":
      input_string = input_string.replace(symbol, ". ")
    else:
      input_string = input_string.replace(symbol, "")

  return input_string

def is_forbidden_string(input_string):
  pattern_under_score = re.compile("_{2,}")
  pattern_minus = re.compile("-{2,}")
  pattern_multiple = re.compile("\*\s\*\s\\\s(\-|\s)+\*\s\*")

  if len(input_string) == 0:
    return True
  elif pattern_under_score.match(input_string):
    return True
  elif pattern_minus.match(input_string):
    return True
  elif pattern_multiple.match(input_string):
    return True
  return False

def pyviConvert(input_str):
  input_str = unicode(input_str, "utf-8")
  input_str = ViTokenizer.tokenize(input_str)
  input_str = input_str.encode("utf-8")
  return input_str

def write_file(output_file, data, delimiter):
  with open(output_file, "a") as output_file_pt:
    output_file_pt.write(data + delimiter)
  output_file_pt.close()

def handle_file(input_file_path, output_file_path, delimiter, need_to_checked):
  db_con = psycopg2.connect(dbname=DB_NAME, user=USER_NAME,
    host=HOST_NAME, password=HOST_PASS)
  cur = db_con.cursor()
  with open(input_file_path) as fp:
    for line in fp:
      if need_to_checked:
        cut_data = line.split("\t")[1]
        cut_id = line.split("\t")[0]
        cur.execute(QUERY_INSERT_AI_TO_ARTICLES, [cut_id])
        db_con.commit()
        if len(cut_data.strip()) <= 2 or "file:///" in cut_data:
          continue
        checked_line = handle_string(cut_data)
        if is_forbidden_string(checked_line):
          continue
        outputPyVi = pyviConvert(checked_line)
        if len(outputPyVi) <= 2:
          continue
      else:
        outputPyVi = pyviConvert(line)
      write_file(output_file_path, outputPyVi, delimiter)
  fp.close()
  cur.close()
  db_con.close()

def main():
  if len(sys.argv) == 2:
    if str(sys.argv[1]) == PARAM_BUILD_DATA:
      handle_file(os.path.join(dir, INPUT_DATA_FILE_NAME),
        os.path.join(dir, PROCESSED_INPUT_DATA_FILE_NAME), "\n", True)
    elif str(sys.argv[1]) == PARAM_BUILD_SW:
      handle_file(os.path.join(dir, INPUT_STOPWORDS_FILE_NAME),
        os.path.join(dir, PROCESSED_INPUT_STOPWORDS_FILE_NAME), "\n", False)

if __name__ == "__main__":
    main()
