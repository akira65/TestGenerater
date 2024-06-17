import os
from subprocess import run, PIPE, STDOUT
from main.path.paths import EVO_TEST_DIR, LIB_PATH, PROJECT_DIR

def get_test_classes(project_name: str):
    test_classes = []
    test_dir = f"{EVO_TEST_DIR}/{project_name}/classes"

    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith("ESTest.class"):
                # クラスファイルのパスを相対パスに変換
                relative_path = os.path.relpath(os.path.join(root, file), test_dir)
                # パッケージ名とクラス名を抽出
                test_class = relative_path.replace(os.sep, ".")[:-6]  # ".class"を除くために[:-6]を使用
                test_classes.append(test_class)
    return test_classes

def run_evo_tests(project_name: str, project_class_path: str):
    test_classes = get_test_classes(project_name)

    if not test_classes:
        print("テストクラスファイルの取得に失敗しました。")
        return
    else:
        print(test_classes)

    for test_class in test_classes:
        command = (
            f"java -javaagent:{LIB_PATH}/org.jacoco.agent-0.8.10-runtime.jar=destfile=jacoco.exec "
            f"-cp .:{LIB_PATH}/junit-4.13.2.jar:{LIB_PATH}/evosuite-standalone-runtime-1.0.6.jar:{project_class_path}:"
            f"{EVO_TEST_DIR}/{project_name}/classes:{LIB_PATH}/hamcrest-2.2.jar org.junit.runner.JUnitCore {test_class}"
        )
        
        # テストの実行
        os.system(command)
        generate_coverage_report(project_name, project_class_path, test_class)


def generate_coverage_report(project_name: str, project_class_path: str, test_class: str):
    project_src_path = os.path.join(PROJECT_DIR, project_name, "src", "main", "java")
    command = (
        f"java -jar {LIB_PATH}/org.jacoco.cli-0.8.10-nodeps.jar report jacoco.exec --classfiles "
        f"{project_class_path} --sourcefiles {project_src_path} --html {EVO_TEST_DIR}/{project_name}/report/{test_class}"
    )
    # カバレッジレポート生成の実行
    result = run(command, shell=True, stdout=PIPE, stderr=STDOUT, encoding="utf-8")
    if result.returncode != 0:
        print(f"カバレッジレポート生成エラー: {result.stdout}")

