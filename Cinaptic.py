#!/usr/bin/env python3
import os
import daemon
import logging
import logging.handlers
import argparse
from cinaptic.cinaptic.api.library.semantic.utils.utils import check_int, check_string, check_path, parse_string, is_path_creatable
from cinaptic.cinaptic.api.library.semantic.GraphBuilder import GraphBuilder
from cinaptic.cinaptic.api.library.semantic.Config import Config
config = Config().getParameters()

# argparse
parser = argparse.ArgumentParser(description="Cinaptic Semantic Analizer")
parser.add_argument("entity", type=check_string,
                    help="Entity for the knowledge graph")
parser.add_argument("-d", "--depth", type=check_int, dest="depth",
                    help="Depth of the knowlegde graph")
parser.add_argument('-D', '--debug',
    help="Log lots of debugging statements",
    action="store_const", dest="loglevel", const=logging.DEBUG, default=config['loglevel'])
parser.add_argument('-L', '--log',
    help="Enter a path to change the default log file",
    type=check_path , dest="logfile", default=config['logfile'])
parser.add_argument('-NE', '--noemail',
    help="Send email with results flag",
    action="store_true", dest="noemail")
parser.add_argument('-O', '--onlyresults',
    help="Process only results flag",
    action="store_true", dest="onlyresults")
args = parser.parse_args()

# logger
logging.basicConfig()
file_logger = logging.FileHandler(args.logfile, "w")
logger = logging.getLogger()
logger.addHandler(file_logger)
logger.setLevel(args.loglevel)

entity = parse_string(args.entity)

# hardcodeada
# meta = [f"results/{entity}/Betweenness_idGraph_{entity}_relation_BROADER.csv",
# f"results/{entity}/Betweenness_idGraph_{entity}_relation_SUBJECT.csv",
# f"results/{entity}/Closeness_idGraph_{entity}_relation_BROADER_improved_False.csv",
# f"results/{entity}/Closeness_idGraph_{entity}_relation_BROADER_improved_True.csv",
# f"results/{entity}/Closeness_idGraph_{entity}_relation_SUBJECT_improved_False.csv",
# f"results/{entity}/Closeness_idGraph_{entity}_relation_SUBJECT_improved_True.csv",
# f"results/{entity}/Degree_idGraph_{entity}_relation_BROADER_direction_incoming.csv",
# f"results/{entity}/Degree_idGraph_{entity}_relation_BROADER_direction_outcoming.csv",
# f"results/{entity}/Degree_idGraph_{entity}_relation_SUBJECT_direction_incoming.csv",
# f"results/{entity}/Degree_idGraph_{entity}_relation_SUBJECT_direction_outcoming.csv",
# f"results/{entity}/Harmonic_Closeness_idGraph_{entity}_relation_BROADER.csv",
# f"results/{entity}/Harmonic_Closeness_idGraph_{entity}_relation_SUBJECT.csv",
# f"results/{entity}/PageRank_idGraph_{entity}_relation_BROADER_iterations_20_dampingFactor_0.85.csv",
# f"results/{entity}/PageRank_idGraph_{entity}_relation_SUBJECT_iterations_20_dampingFactor_0.85.csv"]

# main
config["entity"] = entity
if args.depth is not None:
    config["depth"] = int(args.depth)
if args.noemail is not None:
    config["noemail"] = bool(args.noemail)
if args.onlyresults is not None:
    config["onlyresults"] = bool(args.onlyresults)
if config["onlyresults"]:
    path = f"""results/{config["entity"]}"""
    if not os.path.isdir(path):
        os.mkdir(path)
with daemon.DaemonContext(files_preserve=[file_logger.stream.fileno()]):
    builder = GraphBuilder()
    builder.build(config)