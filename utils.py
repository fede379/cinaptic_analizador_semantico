#!/usr/bin/env python3
# utils file
import pickle
import re
import argparse


def savePickle(path=None, results=None):
    if path is not None and results is not None:
        with open(path, 'wb') as f:
            pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)
    return path


def getLexicographicTuple(entity1=None, entity2=None):
    tupla = None
    if entity1 is not None and entity2 is not None:
        if entity1 < entity2:
            tupla = tuple([entity1, entity2])
        else:
            tupla = tuple([entity2, entity1])
    return tupla


def lexicographicSort(unsortedList=[]):
    result = [(x, y) for x in unsortedList for y in unsortedList if x < y]
    return result


def loadPickle(nameGraph=None):
    if nameGraph is not None:
        path = f'graphs/{nameGraph}.pickle'
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print('No se encontro ningun grafo creado')
            return {}
    return {}

def cleanString(string = ''):
    blacklist = """!"#$%&'()*+,./:;<=>?@[\]^_`{|}~"""
    try:
        chars = re.escape(blacklist)
        result = re.sub(f"[{chars}]", '',string)
    except Exception as e:
        raise argparse.ArgumentTypeError(
            "%s is an invalid string value" %string)
    return result
