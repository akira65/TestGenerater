import os
import subprocess

from main.utils.utils import check_directory_exists, find_java_file_dirs
from main.path.paths import EVO_TEST_DIR, LIB_PATH

def compile_evo_tests(project_name: str, project_class_path: str, tests_path: str, method_name: str):
    print('Compiling methods in ' + tests_path)
    output_dir = ""
    if tests_path.find("/caller/") != -1:
        output_dir = f"{EVO_TEST_DIR}/{project_name}/caller/classes/{method_name}"
    
    if tests_path.find("/callee/") != -1:
        output_dir = f"{EVO_TEST_DIR}/{project_name}/callee/classes/{method_name}"
    
    if output_dir == "":
        return
    
    if not check_directory_exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    test_dirs = find_java_file_dirs(tests_path)
    for test_dir in test_dirs:
        command = (
            "javac"
            f" -d {output_dir}"
            f" -cp .:{LIB_PATH}/junit-4.13.2.jar:{LIB_PATH}/evosuite-standalone-runtime-1.0.6.jar:{project_class_path}"
            f" {test_dir}/*.java"
        )

        # コンパイルを実行
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pout, perr = p.communicate()
        
