
import os
import sys
from main.utils.utils import check_directory_exists
from main.path.paths import EVO_TEST_DIR, LIB_PATH


def compile_evo_tests(project_name: str, project_class_path: str, test_dirs: list):
    for test_dir in test_dirs:
        output_dir =  f"{EVO_TEST_DIR}/{project_name}/classes"

        if not check_directory_exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
                print(f"Directory '{output_dir}' created successfully.")
            except OSError as e:
                print(f"Failed to create directory '{output_dir}': {e}", file=sys.stderr)


        command = (
            f"javac -d {output_dir} "
            f"-cp .:{LIB_PATH}/junit-4.13.2.jar:{LIB_PATH}/evosuite-standalone-runtime-1.0.6.jar:{project_class_path} "
            f"{test_dir}/*.java"
        )
        
        # コンパイルを実行
        os.system(command)