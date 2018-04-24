#!/bin/bash

cd topmine/
python topmine.py

cd ../
python ahctc/ahctcclust.py ./topmine/output/keyword_topics_distribution.txt

python visualized3j/converter.py
