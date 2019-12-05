#!/usr/bin/env python3
import os
import logging
import logging.handlers
import argparse
from QueryExpansion import QueryExpansion
from utils import cleanString

# argparse
parser = argparse.ArgumentParser(description="Cinaptic Query Expansion")
parser.add_argument("sk", type=cleanString, help="Search key for the query expansion")
args = parser.parse_args()

qe = QueryExpansion()
qe.execute(args.sk)