from main.run_evosuite.run import run
from main.run_evo_test.run import run as run_evo_test

def main():
    run_evo_test()
    run()


if __name__ == '__main__':
    run()
