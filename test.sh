#! /bin/bash
clear

PYTHONPATH=src python3 -m unittest discover -s tests -v
