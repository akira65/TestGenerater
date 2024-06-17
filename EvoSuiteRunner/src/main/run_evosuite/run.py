import os
from main.utils.utils import install_openjdk, set_java_home
from .method_searcher import execute_method_searcher, ensure_method_searcher_exists, get_class_with_method_list
from .evosuite_runner import call_evosuite

from main.path.paths import EVO_JAR, EVO_TEST_DIR, PROJECT_DIR, TEST_GEN_DIR

def run():

# 0から1の間のランダムな浮動小数点数を生成
    # MethodSearcherのJARファイルを確認
    PARSER_JAR_PATH = ensure_method_searcher_exists(TEST_GEN_DIR)
    
    # # TargetProjectディレクトリ内のサブディレクトリの名前とパスを取得
    project_infos = {name: os.path.join(PROJECT_DIR, name) for name in os.listdir(PROJECT_DIR) if os.path.isdir(os.path.join(PROJECT_DIR, name))}

    for project_name, project_path in project_infos.items():
        execute_method_searcher(project_name, project_path, PARSER_JAR_PATH)

    method_ref_lists = {}

    # メソッド解析によって生成されたファイルを取得
    method_files = [f for f in os.listdir(TEST_GEN_DIR) if f.endswith('_methods.txt')]
    if method_files:
        for file in method_files:
            filePath = os.path.join(TEST_GEN_DIR, file)
            # key: メソッドリストのファイル名　value: {caller_class, caller_method, callee_class, callee_method}
            method_ref_lists[file]=get_class_with_method_list(filePath)
    else:
        print("メソッド解析に失敗しました")


    # # Evosuiteに対応するJava８の環境設定
    install_openjdk()
    set_java_home()

    # # EvoSuite 実行
    if method_ref_lists:
        project_infos_copy = project_infos.copy()

        for project_name, project_path in project_infos_copy.items():
            method_ref_lists_key = project_name + '_methods.txt'
            
            if method_ref_lists_key in method_ref_lists:
                call_evosuite(project_name, project_path, method_ref_lists[method_ref_lists_key], EVO_JAR, f"{EVO_TEST_DIR}/{project_name}/src")
                del project_infos[project_name]

        if project_infos:
            for project_name in project_infos:
                print(f"{project_name}のメソッドファイルに異常があります")
    else:
        print("メソッドファイルに異常があります")

if __name__ == '__main__':
    run()
