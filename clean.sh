#!/bin/bash

# PARAMS:
#   (1) DEL_IP: delete input/data.txt file
#   (2) NONE: keep input/data.txt file

cd topmine
rm -rf intermediate_output/*
rm -rf output/*

if [ "$1" == "DEL_IP" ]; then
  rm input/data.txt
fi
