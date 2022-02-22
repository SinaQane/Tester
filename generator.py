import os
import subprocess
import random

INPUTS = 100

def get_code():
    cwd = os.getcwd()
    files = os.listdir(cwd)
    for file in files:
        if file[-5:] == '.java':
            return file
 

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

def generate_input(file ,low, high):
    # write your input generating function here using low and high as parameters
    file.write('hello ' + str(random.randint(low, high)) + '\n')

def generate_tests():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    code = get_code()
    
    # the init value of the input range of the tests
    low = -10
    high = 10

    for i in range(0, INPUTS + 1):
        file = open('tests/in/input' + str(i) + '.txt', 'w')
        generate_input(file, low, high)
        file.close()
        
        file = open('tests/in/input' + str(i) + '.txt', 'r')
        input = list(
                filter(
                    lambda s : len(s) != 0,
                    map(
                        lambda s: s.rstrip(),
                        file.read().split('\n')
                    )
                )
            )
        file.close()
        
        error, output = get_output(code, "\n".join(input))
        
        if (error == None):
            file = open('tests/out/output' + str(i) + '.txt', 'w')
            file.write(output)
            file.close()
            print("*** test no. " + str(i) + " generated ***\n")
        else:
            i = i - 1
        
        # for changing the input range of the tests in a while
        if (i > 24):
            low = -100
            high = 100
        if (i > 49):
            low = -10000
            high = 10000 
        if (i > 74):
            low = -1000000
            high = 1000000
            
def main():
    generate_tests()

if __name__ == "__main__":
    main()