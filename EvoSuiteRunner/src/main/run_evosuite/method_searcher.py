import os

def execute_method_searcher(project_name: str, project_path: str, jarfile_path: str):
    print(f"{project_name}プロジェクトのメソッド呼び出し関係の解析を始めます")
    command = f"java -jar {jarfile_path} {project_name} {project_path}"
    os.system(command)
    
# MethodSearcherのJARファイルが存在するか確認し、存在しなければMavenを実行してビルドする
def ensure_method_searcher_exists(test_gen_dir):
    jarfile_path = os.path.join(test_gen_dir, 'MethodSearcher', 'target', 'method_searcher-1.0-SNAPSHOT.jar')
    if not os.path.exists(jarfile_path):
        os.system("maven clean install")
    return jarfile_path

# caller, calleeペアを格納するオブジェクト
class Call:
    def __init__(self, caller_class, caller_method, callee_class, callee_method):
        self.caller_class = caller_class
        self.caller_method = caller_method
        self.callee_class = callee_class
        self.callee_method = callee_method
    
# オブジェクト格納  
def get_class_with_method_list(methodFile: str):
    with open(methodFile, 'r') as file:
        input_text = file.read()

    calls = []
    lines = input_text.strip().split('\n')
    for i in range(0, len(lines)):
        if lines[i].startswith("callerMethod: "):
            caller_method_info = lines[i].replace("callerMethod: ", "")
            callee_method_info = lines[i + 1].replace("calleeMethod: ", "")

            caller_class = caller_method_info.split('#')[0]
            caller_method = caller_method_info.split('#')[1].split('(')[0]
            callee_class = callee_method_info.split('#')[0]
            callee_method = callee_method_info.split('#')[1].split('(')[0]
            calls.append(Call(caller_class, caller_method, callee_class, callee_method))

    return calls
