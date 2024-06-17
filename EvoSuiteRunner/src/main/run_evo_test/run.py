import os

from .compile import compile_evo_tests
from .evo_test_runner import run_evo_tests
from main.utils.utils import find_java_file_dirs, install_openjdk, set_java_home
from main.path.paths import PROJECT_DIR

def run():
    # Evosuiteに対応するJava８の環境設定
    install_openjdk()
    set_java_home()
    
    # プロジェクト情報の取得
    project_infos = {name: os.path.join(PROJECT_DIR, name) for name in os.listdir(PROJECT_DIR) if os.path.isdir(os.path.join(PROJECT_DIR, name))}

    for project_name, project_path in project_infos.items():
        project_class_path = os.path.join(project_path, "target", "classes")
        test_dirs = find_java_file_dirs(project_name)

        # Evosuiteのテストをコンパイル
        compile_evo_tests(project_name, project_class_path, test_dirs)
        
        # Evosuiteのテストを実行
        run_evo_tests(project_name, project_class_path)

if __name__ == '__main__':
    run()
