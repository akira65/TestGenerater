import os

from .compile import compile_evo_tests
from .evo_test_runner import run_evo_tests
from main.utils.utils import check_directory_exists, find_project_cp, install_openjdk, set_java_home
from main.path.paths import EVO_TEST_DIR, PROJECT_DIR

def run():
    # Evosuiteに対応するJava８の環境設定
    install_openjdk()
    set_java_home()
    
    # プロジェクト情報の取得
    project_infos = {name: os.path.join(PROJECT_DIR, name) for name in os.listdir(PROJECT_DIR) if os.path.isdir(os.path.join(PROJECT_DIR, name))}

    for project_name, project_path in project_infos.items():
        project_class_path = find_project_cp(project_path)

        if project_class_path == "":
            continue
        tests_path = f"{EVO_TEST_DIR}/{project_name}/src"

        method_list = []
        if check_directory_exists(tests_path):
            for name in os.listdir(tests_path):
                method_list.append(name)

        # Evosuiteのテストをコンパイル
        compile_evo_tests(project_name, project_class_path, method_list)
        
        # Evosuiteのテストを実行
        for method_name in method_list:
            run_evo_tests(project_name, project_class_path, method_name)

if __name__ == '__main__':
    run()
