from compiler import *
import os
from os.path import isfile, join, realpath, dirname, basename

if __name__ == '__main__':
    compiler = Compiler()

    dir_path = dirname(realpath(__file__))
    valid_dir = join(dir_path, "test/valid/")
    test_files = [join(valid_dir, f) for f in os.listdir(valid_dir) if isfile(join(valid_dir, f))]
    for test in test_files:
        print("--------TESTING VALID INPUT", basename(test))
        errors = compiler.compile(test)
        if errors > 0:
            break
        else:
            print("Compiled successfully!")
    
    malformed_dir = join(dir_path, "test/malformed/")
    test_files = [join(malformed_dir, f) for f in os.listdir(malformed_dir) if isfile(join(malformed_dir, f))]
    for test in test_files:
        print("--------TESTING MALFORMED INPUT", basename(test))
        errors = compiler.compile(test)
        if errors == 0:
            break
        else:
            print("Detected errors!")