#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 13:48:08 2021

@author: pierre
"""

from argparse import ArgumentParser

parser = ArgumentParser(description="check compressed sequence")
parser.add_argument("idx_file", help="path to index file")

args = parser.parse_args()

with open(args.idx_file, "rb") as f:
    f.readline()
    f.readline()
    seq = f.read()

for s in seq:
    print(s)