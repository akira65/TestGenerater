import csv
import os
import subprocess
import xml.etree.ElementTree as ET
from main.utils.utils import get_method_name
from main.path.paths import EVO_TEST_DIR, LIB_PATH, PROJECT_DIR
from main.run_evosuite.method_searcher import Call


# 生成したテストケースをパッケージ名込みで取得
def get_test_classes(project_name: str, method_name: str, class_position: str):
    test_dir =  f"{EVO_TEST_DIR}/{project_name}/{class_position}/classes/{method_name}"
    
    test_classes = []
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith("ESTest.class"):
                
                # クラスファイルのパスを相対パスに変換
                relative_path = os.path.relpath(os.path.join(root, file), test_dir)
                # パッケージ名とクラス名を抽出
                test_class = relative_path.replace(os.sep, ".")[:-6]  # ".class"を除くために[:-6]を使用
                test_classes.append(test_class)
    return test_classes
        
# テストケースを一つずつJUnitで実行、Jacocoでjacoco.execを生成
def run_evo_tests(project_name: str, project_class_path: str, method_ref: Call):
    caller_method_name = method_ref.caller_method
    caller_test_classes = get_test_classes(project_name, caller_method_name, "caller")

    callee_method_name = method_ref.caller_method
    callee_test_classes = get_test_classes(project_name, callee_method_name, "callee")

    if not caller_test_classes and not callee_test_classes:
        print("テストクラスファイルの取得に失敗しました。")
        return
    
    methods_num = call_junit_and_jacoco(project_class_path, project_name, caller_test_classes, caller_method_name, method_ref, "caller")
    call_junit_and_jacoco(project_class_path, project_name, callee_test_classes, callee_method_name, method_ref, "callee")

    return methods_num


def call_junit_and_jacoco(project_class_path: str, project_name: str, test_classes: list, method_name: str, method_ref: Call, class_position: str):
    MAX_TEST_NUM = 20
    total_num = 0
    coverage_sum = 0

    print(f"{method_name}のテストを開始します")
    for test_class in test_classes:
        command0 = (
             "java"
            f" -javaagent:{LIB_PATH}/org.jacoco.agent-0.8.10-runtime.jar=destfile=jacoco.exec"
            f" -cp .:"
            f"{LIB_PATH}/junitmethodrunner.jar:"
            f"{LIB_PATH}/junit-4.13.2.jar:"
            f"{LIB_PATH}/evosuite-standalone-runtime-1.0.6.jar:"
            f"{project_class_path}:"
            f"{EVO_TEST_DIR}/{project_name}/{class_position}/classes/{method_name}:"
            f"{LIB_PATH}/hamcrest-2.2.jar"
        )
        
        
        test_methods = find_test_methods(command0, test_class)
        test_method_num = min(int(MAX_TEST_NUM / len(test_classes)), len(test_methods))
        # 一つのメソッドに対して最大２０個のテストまで
        limited_test_methods = test_methods[:test_method_num]

        for num, (test_class, test_method) in enumerate(limited_test_methods, 1):
            total_num = total_num + 1
            run_test_methods(command0, test_class, test_method, test_method_num, num)
            report_path = f"{EVO_TEST_DIR}/{project_name}/{class_position}/report/{method_name}"
            os.makedirs(report_path, exist_ok=True)
            report_file = f"{report_path}/{test_class}_{test_method}.xml"
            generate_coverage_report(project_name, project_class_path, report_file)
            if class_position == "caller":
                result = check_coverage_report(report_file, method_ref)
                coverage_sum = coverage_sum + result
    
    # CSVに書き込み
    if class_position == "caller" and not total_num == 0:
        write_to_csv(project_name, method_name, total_num, coverage_sum, class_position)

        print('Covered ' + method_ref.callee_class + '#' + method_ref.callee_method + ': ')
        print('  test method number = ' + str(total_num))
        print('  covered test method number = ' + str(coverage_sum / total_num))
        print('  test method number = ' + str(coverage_sum))

    return len(test_methods)
                
def find_test_methods(command0, test_class):
    # コマンドを組み立てる
    command_find = command0 + f" junitmethodrunner.MethodFinder {test_class}"
    
    # コマンドを実行して出力を取得する
    p = subprocess.Popen(command_find, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pout, perr = p.communicate()

    # 出力をデコードし、行ごとに分割する
    test_method_info = pout.decode().rstrip('\r\n').split('\n') if pout else []
    # タプルのリストを作成する
    test_methods = [tuple(m.split('#')) for m in test_method_info]
    
    return test_methods
        
def run_test_methods(command0, test_class, test_method, total_num, num):
    print('Running ' + test_class + '#' + test_method + ' (' + str(num) + '/' + str(total_num) + ')')
    command_test = command0 + f" junitmethodrunner.Runner {test_class} {test_method}"
    p = subprocess.Popen(command_test, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    pout, perr = p.communicate()

# Jacoco.execをもとにカバレッジレポートを生成
def generate_coverage_report(project_name: str, project_class_path: str, report_file: str):
    project_src_path = os.path.join(PROJECT_DIR, project_name, "src", "main", "java")
    command = (
        "java"
        f" -jar {LIB_PATH}/org.jacoco.cli-0.8.10-nodeps.jar"
         " report jacoco.exec"
        f" --classfiles {project_class_path}"
        f" --sourcefiles {project_src_path}"
        f" --xml {report_file}"
    )

    # カバレッジレポート生成の実行
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
    if result.returncode != 0:
        print(f"カバレッジレポート生成エラー: {result.stdout}")

def check_coverage_report(report_file: str, method_ref: Call):
    caller_class = method_ref.caller_class
    caller_method = method_ref.caller_method

    callee_class = method_ref.callee_class
    callee_method = method_ref.callee_method

    result = covered(report_file, callee_class, callee_method)
    return result
    
def covered(report_file, callee_class, callee_method):
    if not os.path.isfile(report_file):
        return 0
    
    tree = ET.parse(report_file)
    root = tree.getroot()
    for child in root.findall('package'):
        for child2 in child.findall('class'):
            class_name = child2.attrib['name'].replace('/', '.')
            if class_name == callee_class:
                for child3 in child2.findall('method'):
                    method_name = child3.attrib['name']
                    if method_name == callee_method:
                        for child4 in child3.findall('counter'):
                            if child4.attrib['type'] == 'LINE':
                                if int(child4.attrib['covered']) > 0:
                                    # LINEカバレッジ取得
                                    # return int(child4.attrib['covered']) / (int(child4.attrib['covered']) + int(child4.attrib['missed']))
                                    return 1
    return 0

def write_to_csv(project_name: str, method_name: str, test_method_num: int, line_coverage: int, class_position: str):
    # 書き込むCSVファイルのパス
    csv_file = os.path.join(EVO_TEST_DIR, project_name, class_position, "result2.csv")

    # ヘッダーとデータを準備します
    header = ['CalleeMethod', 'TestMethodNum', 'ValidTest']
    data = [method_name, test_method_num, line_coverage]

    # ファイルが存在しない場合は、新規作成してヘッダーを書き込む
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    # 追記
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
