import os
import subprocess
import sys

from main.path.paths import EVO_TEST_DIR

    # ディレクトリが存在するか確認し、存在しなければエラーメッセージを表示
def check_directory_exists(path):
    if not os.path.isdir(path):
        return False
    return True

    # OpenJDKをインストール
def install_openjdk():
    if os.system("brew list openjdk@8 &>/dev/null"):
        print("openjdk@8 is not installed. Installing now...")
        os.system("brew install openjdk@8")
    set_java_home()

    # JAVA_HOME環境変数を設定し、パスを更新
def set_java_home():
    try:
        java_home = subprocess.check_output(["brew", "--prefix", "openjdk@8"]).decode().strip()
        os.environ["JAVA_HOME"] = java_home
        os.environ["PATH"] = f"{java_home}/bin:{os.environ['PATH']}"
        java_version = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT).decode()
        print(f"javaのバージョンを変更しました。\n{java_version}")
    except subprocess.CalledProcessError:
        print("JAVA_HOMEの設定に失敗しました。", file=sys.stderr)
        sys.exit(1)

def find_java_file_dirs(base_dir: str):
    test_dirs = []
    
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".java") and root not in test_dirs:
                test_dirs.append(root)
                
    return test_dirs

def find_project_cp(project_path: str):
    project_cp = os.path.join(project_path, 'target', 'classes')
    if not check_directory_exists(project_cp):
        project_cp = os.path.join(project_path, 'build', 'classes', 'java', 'main')
    else:
        return project_cp
    
    if not check_directory_exists(project_cp):
        project_cp = os.path.join(project_path, 'build', 'classes')
    else:
        return project_cp

    if not check_directory_exists(project_cp):
        print(f"{project_path}プロジェクトクラスパスが見つかりませんでした。")
        return ""

def get_method_name(test_dir):
    src_index = test_dir.find("/src/")

    if src_index != -1:
        after_src = test_dir[src_index + 5:]
        method_name = after_src.split("/")[0]
        
        return method_name
    else:
        print("srcディレクトリが見つかりませんでした")
