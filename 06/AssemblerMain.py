import Parser
import sys
import os

SOURCE_FILE_EXTENSION = ".asm"

class Assembler:
    def __init__(self, path, is_folder):
        if is_folder:
            for file_name in os.listdir(path):
                if file_name.endswith(SOURCE_FILE_EXTENSION):
                    Parser.Parser(path, file_name)
        else:
            path, file_name = os.path.split(path)
            Parser.Parser(path + "/", file_name)

def main():
    if sys.argv[1].endswith(SOURCE_FILE_EXTENSION):
        Assembler(sys.argv[1], False)
    elif "." in sys.argv[1]:
        print("wrong input, you should enter full path of the asm file or a folder")
    else:
        Assembler(sys.argv[1], True)


if __name__ == "__main__":
    main()

