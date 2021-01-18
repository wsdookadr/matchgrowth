#!/usr/bin/python3
import sys, os
sys.path.append(os.getcwd() + '/..')

import numpy
from matchgrowth import *

def test_linear():
    X = np.linspace(1,100,num=100)
    Y = (lambda x: x/2)(X)
    matches = match_catalog(X,Y)
    first_matched = matches[0]["catalog_label"]
    assert first_matched == "linear"

def test_polynomial():
    X = np.linspace(1,100,num=100)
    Y = (lambda x: x**4 + 2*x**2 + 3)(X)
    matches = match_catalog(X,Y)
    first_matched = matches[0]["catalog_label"]
    assert first_matched == "polynomial"

test_polynomial()
