#!/usr/bin/env python3
from cinaptic.cinaptic.api.library.semantic.GraphBuilder import GraphBuilder
from cinaptic.cinaptic.api.library.semantic.Config import Config
import argparse
import re
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description="Cinaptic Semantic Analizer")
parser.add_argument("keys", type=str,
                    help="Search keys for the knowledge graph")

class App:
    def run(self):
        config = Config().getParameters()
        args = parser.parse_args()
        key = args.keys.strip()
        regex = re.compile('^([a-zA-Z ]+)+$')
        if regex.match(key):
            config["keys"] = key
            print(config["keys"])
            builder = GraphBuilder()
            builder.build(config)
        else:
            print('Invalid string')
        

app = App()
app.run()