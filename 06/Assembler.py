import Parser
import sys
import os

SOURCE_FILE_EXTENSION = ".asm"

class Assembler:
    def __init__(self, path, is_folder):
        if is_folder:
            for file_name in os.listdir(path):
                print(file_name)
                print(path)
                if file_name.endswith(SOURCE_FILE_EXTENSION):
                    Parser.Parser(path, "/" + file_name)
        else:
            file_name = os.path.split(path)[1]
            path = os.path.split(path)[0] + "/"
            Parser.Parser(path, file_name)

def main():
    abs_path = os.path.abspath(sys.argv[1])
    if abs_path.endswith(SOURCE_FILE_EXTENSION):
        Assembler(abs_path, False)
    else:
        Assembler(abs_path, True)



if __name__ == "__main__":
    main()

