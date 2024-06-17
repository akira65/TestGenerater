import os
import subprocess
import sys

from main.path.paths import EVO_TEST_DIR

def check_directory_exists(path):
    # ディレクトリが存在するか確認し、存在しなければエラーメッセージを表示
    if not os.path.isdir(path):
        return False
    return True

def run_subprocess(command, cwd=None, error_message=None):
    # サブプロセスを実行し、失敗した場合にエラーメッセージを表示して終了
    try:
        subprocess.run(command, cwd=cwd, check=True)
    except subprocess.CalledProcessError:
        if error_message:
            print(error_message, file=sys.stderr)
        sys.exit(1)

def install_openjdk():
    # OpenJDKをインストール
    if os.system("brew list openjdk@8 &>/dev/null"):
        print("openjdk@8 is not installed. Installing now...")
        os.system("brew install openjdk@8")
    set_java_home()

def set_java_home():
    # JAVA_HOME環境変数を設定し、パスを更新
    try:
        java_home = subprocess.check_output(["brew", "--prefix", "openjdk@8"]).decode().strip()
        os.environ["JAVA_HOME"] = java_home
        os.environ["PATH"] = f"{java_home}/bin:{os.environ['PATH']}"
        java_version = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT).decode()
        print(java_version)
    except subprocess.CalledProcessError:
        print("JAVA_HOMEの設定に失敗しました。", file=sys.stderr)
        sys.exit(1)

def find_java_file_dirs(project_name: str):
    test_dirs = []
    
    for root, _, files in os.walk(f"{EVO_TEST_DIR}/{project_name}/src"):
        for file in files:
            if file.endswith(".java"):
                test_dirs.append(root)
    return test_dirs
