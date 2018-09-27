#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 11:41:58 2018

@author: max
"""
import pandas as pd

#Import datasets, add subjects variable
mat = pd.read_csv('student-mat.csv',sep=";")
mat['subject'] = ["M" for x in range(mat.shape[0])]
por = pd.read_csv('student-por.csv',sep=";")
por['subject'] = ["P" for x in range(por.shape[0])]

#Merge/concat subjects
#matpor = pd.merge(mat, por, on=["school","sex","age","address","famsize","Pstatus","Medu","Fedu","Mjob","Fjob","reason","nursery","internet"], suffixes=('_mat', '_por'))
matpor = pd.concat([mat,por])
matpor.to_csv('matpor_concat.csv', sep=',')

#Bin into categories
# not necessary for our dataset
