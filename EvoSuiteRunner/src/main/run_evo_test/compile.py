
import os

from main.utils.utils import check_directory_exists, find_java_file_dirs
from main.path.paths import EVO_TEST_DIR, LIB_PATH

def compile_evo_tests(project_name: str, project_class_path: str, method_list: list):
    i = 0
    for method_name in method_list:
        print(i)
        i  =  i + 1
        output_dir =  f"{EVO_TEST_DIR}/{project_name}/classes/{method_name}"

        if not check_directory_exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        test_dirs = find_java_file_dirs(f"{EVO_TEST_DIR}/{project_name}/src/{method_name}")
        for test_dir in test_dirs:
            
            command = (
                f"javac -d {output_dir} "
                f"-cp .:{LIB_PATH}/junit-4.13.2.jar:{LIB_PATH}/evosuite-standalone-runtime-1.0.6.jar:{project_class_path} "
                f"{test_dir}/*.java"
            )
            
            # コンパイルを実行
            os.system(command)