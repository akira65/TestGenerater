#!/bin/bash

# スクリプトファイルの絶対パス
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# TestGeneraterディレクトリパス
TEST_GEN_DIR="$SCRIPT_DIR/../.."

if [ ! -d "$TEST_GEN_DIR" ]; then
    echo "エラー: TEST_GEN_DIRが見つかりません。ディレクトリ構成が変更された可能性があります。" >&2
    exit 1
fi

# TargetProjectディレクトリパス
PROJECT_DIR="$TEST_GEN_DIR/TargetProject"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "エラー: TargetProjectディレクトリが見つかりません。ディレクトリ構成が変更された可能性があります。" >&2
    exit 1
fi

# TargetProjectディレクトリ内のサブディレクトリの名前とパスを取得し,PROJECT＿INFOに格納
declare -a PROJECT_INFOS
i=0
while IFS= read -r -d '' PROJECT_PATH; do
    PROJECT_INFOS["$i"]="$(basename "$PROJECT_PATH")":"$PROJECT_PATH"
    ((i++))
done < <(find "$PROJECT_DIR" -maxdepth 1 -type d -not -path "$PROJECT_DIR" -print0)

# MethodSearcher実行
JARFILE_PATH=$TEST_GEN_DIR/MethodSearcher/target/method_sarcher-1.0-SNAPSHOT.jar

if [ ! -e "$JARFILE_PATH" ]; then
    echo "実行ファイルが見つかりませんでした。MAVENを実行します。"
    cd "$TEST_GEN_DIR/MethodSearcher" || exit 1
    mvn clean install || exit 1
fi 

for ((j=0; j<i; j++)); do
    echo "メソッド解析を開始します。:"
    IFS=":" read -r -a project_info <<< ${PROJECT_INFOS[$j]}
    java -jar $JARFILE_PATH ${project_info[0]} ${project_info[1]}
done
