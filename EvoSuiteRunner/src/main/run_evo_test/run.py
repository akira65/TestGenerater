import os
import sys

from .compile import compile_evo_tests
from main.utils.utils import del_result_csv, method_pair_info_file_postfix
from .evo_test_runner import run_evo_tests
from main.utils.utils import check_directory_exists, find_project_cp, install_openjdk, set_java_home
from main.path.paths import EVO_TEST_DIR, PROJECT_DIR, TEST_GEN_DIR
from main.run_evosuite.method_searcher import get_class_with_method_list

def run(JAVA_HOME: str):
    # Evosuiteに対応するJava８の環境設定
    set_java_home(JAVA_HOME)
    
    # プロジェクト情報の取得
    project_infos = {name: os.path.join(PROJECT_DIR, name) for name in os.listdir(PROJECT_DIR) if os.path.isdir(os.path.join(PROJECT_DIR, name))}

    for project_name, project_path in project_infos.items():
        project_class_path = find_project_cp(project_path)

        if project_class_path == "":
            continue

        csv_file = os.path.join(EVO_TEST_DIR, project_name, "caller", "result.csv")
        del_result_csv(csv_file)
        csv_file = os.path.join(EVO_TEST_DIR, project_name, "callee", "result.csv")
        del_result_csv(csv_file)
        
        total_project_test_num = 0
        method_pair_file_name = project_name + method_pair_info_file_postfix
        filePath = os.path.join(TEST_GEN_DIR, method_pair_file_name)
        caller_methods = []
        callee_methods = []

        for method_ref in get_class_with_method_list(filePath):
            caller_method = method_ref.caller_method
            if not caller_method in caller_methods:
                caller_methods.append(caller_method)

                caller_tests_path = f"{EVO_TEST_DIR}/{project_name}/caller/src/{caller_method}"
                if check_directory_exists(caller_tests_path):
                    # EvosuiteのCallerテストをコンパイル
                    compile_evo_tests(project_name, project_class_path, caller_tests_path, method_ref.caller_method)
                    # EvosuiteのCallerテストを実行
                    test_num = run_evo_tests(project_name, project_class_path, method_ref)
                    if test_num:
                        total_project_test_num = total_project_test_num + test_num


            callee_method = method_ref.caller_method
            if not caller_method in callee_methods:
                callee_methods.append(caller_method)

                callee_method = method_ref.callee_method
                callee_tests_path = f"{EVO_TEST_DIR}/{project_name}/callee/src/{callee_method}"
                if check_directory_exists(callee_tests_path):
                     # EvosuiteのCalleeテストをコンパイル
                    compile_evo_tests(project_name, project_class_path, callee_tests_path, method_ref.callee_method)
                     # EvosuiteのCalleeテストを実行
                    run_evo_tests(project_name, project_class_path, callee_tests_path, method_ref)
        
        # 書き込むCSVファイルのパス
        csv_file = os.path.join(EVO_TEST_DIR, project_name, "total_test_num.csv")

        with open(csv_file, 'w', newline='') as file:
            file.write(f"total_test_num: {total_project_test_num}")
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("JAVA_HOMEを設定してください")
        sys.exit(1)
    run(sys.argv[1])
