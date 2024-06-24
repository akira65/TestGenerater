import os
import sys
from main.utils.utils import set_java_home, method_pair_info_file_postfix
from .method_searcher import execute_method_searcher, ensure_method_searcher_exists, get_class_with_method_list
from .evosuite_runner import run_evosuite
from main.path.paths import EVO_TEST_DIR, PROJECT_DIR, TEST_GEN_DIR

def tests_already_generated(project_name: str):
    return os.path.isdir(f"{EVO_TEST_DIR}/{project_name}")

def run(JAVA_HOME: str):
    
    # MethodSearcherのJARファイルを確認
    PARSER_JAR_PATH = ensure_method_searcher_exists(TEST_GEN_DIR)
    
    # # TargetProjectディレクトリ内のサブディレクトリの名前とパスを取得
    project_infos = {name: os.path.join(PROJECT_DIR, name) for name in os.listdir(PROJECT_DIR) if os.path.isdir(os.path.join(PROJECT_DIR, name))}
    
    # ループ用のバッファ
    project_infos_copy = project_infos.copy()


    for project_name, project_path in project_infos_copy.items():
        if tests_already_generated(project_name):
            del project_infos[project_name]
            print(f"{project_name}は，テストケースの生成が終了しています")
            continue
        method_pair_info_file = os.path.join(TEST_GEN_DIR, project_name + method_pair_info_file_postfix)
        if not os.path.isfile(method_pair_info_file):
            execute_method_searcher(project_name, project_path, PARSER_JAR_PATH)

    # メソッド解析によって生成されたファイルを取得
    method_ref_lists = {}
    # ループ用のバッファ再代入
    project_infos_copy = project_infos.copy()

    for project_name in project_infos_copy.keys():
        file_name = project_name + method_pair_info_file_postfix
        file_path = os.path.join(TEST_GEN_DIR, file_name)
        if os.path.isfile(file_path):
            # key: プロジェクト名　value: {caller_class, caller_method, callee_class, callee_method}
            method_ref_lists[project_name]=get_class_with_method_list(file_path)
        else:
            print("メソッド解析に失敗しました")
            sys.exit(1)
    
    # # # Evosuiteに対応するJava８の環境設定
    set_java_home(JAVA_HOME)
    
    # # # EvoSuite 実行
    if method_ref_lists:
        for project_name, project_path in project_infos_copy.items():
            
            if project_name in method_ref_lists:
                method_ref_list = method_ref_lists[project_name]
                run_evosuite(project_name, project_path, method_ref_list, f"{EVO_TEST_DIR}/{project_name}")
                del project_infos[project_name]

        if project_infos:
            for project_name in project_infos:
                print(f"{project_name}のメソッドファイルに異常があります")
    else:
        print("メソッドファイルに異常があります")

    print("テストケースの生成が終了しました")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("JAVA_HOMEを設定してください")
        sys.exit(1)
    run(sys.argv[1])
