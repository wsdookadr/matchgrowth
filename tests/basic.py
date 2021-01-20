#!/usr/bin/python3
import sys, os
mod_path = os.getcwd() + '/'
print(mod_path)
sys.path.insert(0,mod_path)

import numpy as np
from matchgrowth import *

class MockArgs:
    def debug(self):
        return False

def test_linear():
    cli_args = MockArgs()
    X = np.linspace(1,100,num=100)
    Y = (lambda x: x/2)(X)
    matches = match_catalog(cli_args, X,Y,common_catalog)
    first_matched = matches[0]["catalog_label"]
    assert first_matched == "linear"

def test_polynomial():
    cli_args = MockArgs()
    X = np.linspace(1,100,num=100)
    Y = (lambda x: x**4 + 2*x**2 + 3)(X)
    matches = match_catalog(cli_args,X,Y,common_catalog)
    first_matched = matches[0]["catalog_label"]
    assert first_matched == "polynomial"

def test_exponential():
    cli_args = MockArgs()
    X = np.linspace(1,100,num=100)
    Y = (lambda x: 10 + np.exp(x) )(X)
    matches = match_catalog(cli_args, X,Y,common_catalog)
    first_matched = matches[0]["catalog_label"]
    assert first_matched == "exp_e"

