# 0から1の間のランダムな浮動小数点数を生成
import os
import random
import sys


def get_absolute_path(*paths):
    # 指定された相対パスを絶対パスに変換
    return os.path.abspath(os.path.join(*paths))

i = random.random()

# スクリプトファイルの絶対パス
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# TestGeneraterディレクトリパス
TEST_GEN_DIR: str = get_absolute_path(SCRIPT_DIR, '..', '..', '..', '..')

# TargetProjectディレクトリパス
PROJECT_DIR = os.path.join(TEST_GEN_DIR, 'TargetProject')

# EvoSuiteの出力先
EVO_TEST_DIR = os.path.join(TEST_GEN_DIR, "EvoSuiteRunner", "evosuite")

LIB_PATH = os.path.join(TEST_GEN_DIR, "EvoSuiteRunner", "lib")

#Evosuiteのjarファイルパス
EVO_JAR = os.path.join(LIB_PATH, "evosuite-1.0.6.jar")
