#!/bin/bash

cd topmine/
python topmine.py
cd ../
python dump.py

python ahctc/ahctcclust.py ./topmine/output/keyword_topics_distribution.txt
