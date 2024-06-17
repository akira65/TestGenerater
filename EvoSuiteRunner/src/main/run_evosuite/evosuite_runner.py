import os
import sys
from main.utils.utils import run_subprocess

def run_evosuite(project_name: str, project_cp: str, class_path: str, EVO_JAR: str, OUTPUT_DIR: str):
   
    command = f"java -jar {EVO_JAR} -class {class_path} -projectCP {project_cp} -Dsearch_budget=300 -generateSuite -Dtest_dir={OUTPUT_DIR} -Dreport_dir={OUTPUT_DIR} -Dminimize=false -Duse_separate_classloader=false"


    if os.path.exists(project_cp):
        os.system(command)
    else:
        print(f"プロジェクト {project_name} の target ディレクトリが見つかりません。プロジェクトをコンパイルしてください。", file=sys.stderr)


import os

def call_evosuite(project_name: str, project_path: str, method_ref_list: dict, EVO_JAR: str, OUTPUT_DIR: str):
    class_list = []
    exist_class_path_list = []
    project_cp = os.path.join(project_path, 'target', 'classes')

    for method_ref in method_ref_list:
        if method_ref.caller_class not in class_list:
            class_list.append(method_ref.caller_class)

    for class_root in class_list:
        replaced_class_root = class_root.replace('.', '/')
        class_path = os.path.join(project_cp, replaced_class_root)
        if os.path.exists(class_path + ".class"):
            replaced_class_root = replaced_class_root.replace('/', '.')
            exist_class_path_list.append(replaced_class_root)
      
    for exist_class_path in exist_class_path_list:
        run_evosuite(project_name, project_cp, exist_class_path, EVO_JAR, OUTPUT_DIR)

