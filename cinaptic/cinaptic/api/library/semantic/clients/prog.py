import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("keys", type=str,
                    help="the keys to make the Knowledged Graph")
args = parser.parse_args()
answer = str(args.keys).strip()
patron = re.compile('^([a-zA-Z ]+)+$')
if patron.match(answer):
    print('exito')    
else:
    print('fail')