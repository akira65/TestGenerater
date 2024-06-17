import os
import sys

from main.utils.utils import find_project_cp


def run_evosuite(project_name: str, project_cp: str, class_path: str, method_path: str, EVO_JAR: str, OUTPUT_DIR: str):
   
    command = f"java -jar {EVO_JAR} -class {class_path} -Dtarget_method {method_path} -projectCP {project_cp} -Dsearch_budget=200 -Dnumber_of_tests_per_target=200 -generateSuite -Dtest_dir={OUTPUT_DIR} -Dreport_dir={OUTPUT_DIR} -Dminimize=false -Duse_separate_classloader=false"

    if os.path.exists(project_cp):
        os.system(command)
    else:
        print(f"プロジェクト {project_name} の target ディレクトリが見つかりません。プロジェクトをコンパイルしてください。", file=sys.stderr)

def call_evosuite(project_name: str, project_path: str, method_ref_list: dict, EVO_JAR: str, OUTPUT_DIR: str):
    method_info_list = []
    
    project_cp = find_project_cp(project_path)

    for method_ref in method_ref_list:
        class_root = method_ref.caller_class.replace('.', '/')
        class_path = os.path.join(project_cp, class_root)

        if os.path.exists(class_path + ".class"):
            replaced_class_root = class_root.replace('/', '.')
            replaced_method_root = f"{replaced_class_root}.{method_ref.caller_method}"
            method_info_list.append({
                'replaced_class_root': replaced_class_root,
                'replaced_method_root': replaced_method_root,
                'method_name' : method_ref.caller_method
            })

    for exist_class_path in method_info_list:
        run_evosuite(project_name, project_cp, exist_class_path['replaced_class_root'], exist_class_path['replaced_method_root'], EVO_JAR, f"{OUTPUT_DIR}/{exist_class_path['method_name']}")

