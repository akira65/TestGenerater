import os
import sys

from main.path.paths import EVO_JAR
from main.utils.utils import find_project_cp


def evosuite(project_name: str, project_cp: str, class_path: str, method_path: str, EVO_JAR: str, OUTPUT_DIR: str):
   
    command = (f"java"
               f" -jar {EVO_JAR}"
               f" -class {class_path}"
               f" -Dtarget_method {method_path}"
               f" -projectCP {project_cp}"
                " -Dsearch_budget=200"
                " -Dnumber_of_tests_per_target=60"
                " -generateSuite"
               f" -Dtest_dir={OUTPUT_DIR}"
               f" -Dreport_dir={OUTPUT_DIR}"
                " -Duse_separate_classloader=false")

    if os.path.exists(project_cp):
        os.system(command)
    else:
        print(f"プロジェクト {project_name} の target ディレクトリが見つかりません。プロジェクトをコンパイルしてください。", file=sys.stderr)
    
def run_evosuite(project_name: str, project_path: str, method_ref_list: dict, OUTPUT_DIR: str):
    caller_method_info_list = []
    callee_method_info_list = []
    
    project_cp = find_project_cp(project_path)

    for method_ref in method_ref_list:
        caller_class_root = method_ref.caller_class.replace('.', '/')
        caller_class_path = os.path.join(project_cp, caller_class_root)

        if os.path.exists(caller_class_path + ".class"):
            append_method_info(caller_method_info_list, method_ref.caller_method, caller_class_root)

        callee_class_root = method_ref.callee_class.replace('.', '/')
        callee_class_path = os.path.join(project_cp, callee_class_root)

        if os.path.exists(callee_class_path + ".class"):
            append_method_info(callee_method_info_list, method_ref.callee_method, callee_class_root)
    
    call_evosuite(project_name, project_cp, caller_method_info_list, f"{OUTPUT_DIR}/caller/src")
    call_evosuite(project_name, project_cp, callee_method_info_list, f"{OUTPUT_DIR}/callee/src")
    


def append_method_info(method_info_list: list, method_name: str, class_root: str):
    replaced_class_root = class_root.replace('/', '.')
    replaced_method_root = f"{replaced_class_root}.{method_name}"
    method_info_list.append({
        'replaced_class_root': replaced_class_root,
        'replaced_method_root': replaced_method_root,
        'method_name' : method_name,
    })

def call_evosuite(project_name: str, project_cp: str, method_info_list: list, OUTPUT_DIR: str):
    for exist_class_path in method_info_list:
        evosuite(project_name, project_cp,
                     exist_class_path['replaced_class_root'],
                     exist_class_path['replaced_method_root'],
                     EVO_JAR, f"{OUTPUT_DIR}/{exist_class_path['method_name']}")
        