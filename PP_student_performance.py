#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 11:41:58 2018

@author: max
"""
import pandas as pd

#Import datasets
mat = pd.read_csv('student-mat.csv',sep=";")
por = pd.read_csv('student-por.csv',sep=";")

#Merge subjects
matpor = pd.merge(mat, por, on=["school","sex","age","address","famsize","Pstatus","Medu","Fedu","Mjob","Fjob","reason","nursery","internet"])
matpor.to_csv('matpor.csv', sep=',')

#Bin into categories
# not necessary for our dataset
