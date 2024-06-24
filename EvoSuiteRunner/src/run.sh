#!/bin/bash

# java8をインストール後パスを設定してください
JAVA_HOME=""

python3 -m main.run_evosuite.run "$JAVA_HOME"
python3 -m main.run_evo_test.run "$JAVA_HOME"
