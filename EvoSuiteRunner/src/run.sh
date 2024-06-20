#!/bin/bash

JAVA_HOME="/usr/local/Cellar/openjdk@8/1.8.0-412"
python3 -m main.run_evosuite.run
python3 -m main.run_evo_test.run
