from os.path import isfile, join, realpath, dirname, basename
from compiler import Compiler
import sys
import os

def test_valid(compiler, files):
    for test in test_files:
        print("--------TESTING VALID INPUT", basename(test))
        errors = compiler.compile(test)
        if errors > 0:
            exit(1)
        else:
            print("Compiled successfully!")

def test_malformed(compiler, files):
    for test in test_files:
        print("--------TESTING MALFORMED INPUT", basename(test))
        try:
            errors = compiler.compile(test)
            if errors == 0:
                print("Failed to detect errors :/")
                exit(1)
            else:
                print("Detected errors!")
        except Exception as e:
            print("Detected errors!", "Got error:", e)

if __name__ == '__main__':
    compiler = Compiler()
    dir_path = dirname(realpath(__file__))

    # test only inputs
    if len(sys.argv) > 1:
        test_files = [join(dir_path, f) for f in sys.argv[1:] if isfile(join(dir_path, f))]
        test_valid(compiler, test_files)
        exit()

    valid_dir = join(dir_path, "test/valid/")
    test_files = [join(valid_dir, f) for f in os.listdir(valid_dir) if isfile(join(valid_dir, f))]
    test_valid(compiler, test_files)

    malformed_dir = join(dir_path, "test/malformed/")
    test_files = [join(malformed_dir, f) for f in os.listdir(malformed_dir) if isfile(join(malformed_dir, f))]
    test_malformed(compiler, test_files)