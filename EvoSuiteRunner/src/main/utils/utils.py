import os
import sys

method_pair_info_file_postfix = '_methods.txt'

    # ディレクトリが存在するか確認し、存在しなければエラーメッセージを表示
def check_directory_exists(path):
    return os.path.isdir(path)

    # OpenJDKをインストール
def install_openjdk():
    if os.system("brew list openjdk@8 &>/dev/null"):
        print("openjdk@8 is not installed. Installing now...")
        os.system("brew install openjdk@8")
    set_java_home()

    # JAVA_HOME環境変数を設定し、パスを更新
def set_java_home(JAVA_HOME: str):
    if not JAVA_HOME or not check_directory_exists(JAVA_HOME):
        print("適切なJAVA_HOMEを設定してください", file=sys.stderr)
        sys.exit(1)
    else:
        os.environ["JAVA_HOME"] = JAVA_HOME
        java_bin_path = os.path.join(os.environ["JAVA_HOME"], 'bin')
        os.environ["PATH"] = java_bin_path + ':' + os.environ['PATH']

def find_java_file_dirs(base_dir: str):
    test_dirs = []
    
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".java") and root not in test_dirs:
                test_dirs.append(root)
                
    return test_dirs

def find_project_cp(project_path: str):
    project_cp = os.path.join(project_path, 'target', 'classes')
    if check_directory_exists(project_cp):
        return project_cp
        
    project_cp = os.path.join(project_path, 'build', 'classes', 'java', 'main')
    if check_directory_exists(project_cp):
        return project_cp

    project_cp = os.path.join(project_path, 'build', 'classes')
    if check_directory_exists(project_cp):
        return project_cp
    
    print(f"{project_path}プロジェクトクラスパスが見つかりませんでした。")
    return ""

def get_method_name(test_dir):
    src_index = test_dir.find("/src/")

    if src_index != -1:
        after_src = test_dir[src_index + 12:]
        method_name = after_src.split("/")[0]
        
        return method_name
    else:
        print("srcディレクトリが見つかりませんでした")

# ファイルが存在するか確認し、存在する場合は削除する
def del_result_csv(file_path: str):

    if os.path.exists(file_path):
        os.remove(file_path)