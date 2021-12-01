import os
import re
import subprocess
import time

from colorama import Back, Fore, Style, init

init()

TIME_LIMIT = 10000

def err(string):
    print(Fore.YELLOW + string, end='')

def fail(string):
    print(Fore.RED + string, end='')

def success(string):
    print(Fore.GREEN + string, end='')

def log(string):
    print(Style.RESET_ALL + string, end='')

def beautify(string):
    return string.replace('\n', '\n               ').rstrip()

def get_code():
    cwd = os.getcwd()
    files = os.listdir(cwd)
    for file in files:
        if file[-5:] == '.java':
            return file
 
def get_tests_count():
    numbers = []
    cwd = os.getcwd()
    files = os.listdir(cwd + '/tests/in')
    for file in files:
        numbers.extend([int(x) for x in re.findall("\d+", file)])
    return max(numbers)

def get_tests(tests_count):
    tests = []
    inp = []
    out = []
    for i in range (1, tests_count + 1):
        with open('tests/in/input' + str(i) + '.txt', 'r') as file:
            inp = list(
                filter(
                    lambda s : len(s) != 0,
                    map(
                        lambda s: s.rstrip(),
                        file.read().split('\n')
                    )
                )
            )
        with open('tests/out/output' + str(i) + '.txt', 'r') as file:
            out = list(
                filter(
                    lambda s : len(s) != 0,
                    map(
                        lambda s: s.rstrip(),
                        file.read().split('\n')
                    )
                )
            )
        tests.append(["\n".join(inp), "\n".join(out)])
    return tests

def get_output(program, inp):
    try:
        result = subprocess.check_output(
            [
            'java',
            program
            ],
            input=bytes(
                inp,
                encoding='utf8'
            )
        ).decode("utf-8")
        return None, result
    except:
        return RuntimeError, None

def check_err(err, output):
    if err == None:
        return beautify(output)
    else:
        return 'RuntimeError'

def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    tests_count = get_tests_count()
    code = get_code()

    for idx, test in enumerate(get_tests(tests_count)):
        start_time = time.time()
        error, output = get_output(code, test[0])
        time_elapsed = time.time() - start_time
        
        log(f'Case #{idx + 1}\n')
        log(f'INPUT        : {beautify(test[0])}\n')
        log(f'OUTPUT       : {check_err(error, output)}\n')
        log(f'EXPECTED     : {beautify(test[1])}\n')
        log(f'TIME ELAPSED : {time_elapsed * 1000} ms\n')
        log(f'STATUS       : ')
        
        if error != None:
            err('RUNTIME ERROR\n\n')
        elif time_elapsed * 1000 > TIME_LIMIT:
            err('TIME LIMIT EXCEEDED\n\n')
        elif output.rstrip() == test[1]:
            success('PASSED\n\n')
        else:
            fail('FAILED\n\n')

if __name__ == "__main__":
    main()
