import Parser
import sys
import os

SOURCE_FILE_EXTENSION = ".vm"
DEST_FILE_EXTENSION = ".asm"
WRONG_NUMBER_OF_ARGS = "Wrong number of arguments"
WRONG_EXTENSION = "The program supports only .vm extension"
PATH_DOESNT_EXIST = "The input path to the program does not exist"


class VMtranslator:

    def main():
        num_of_args = len(sys.argv)
        input = sys.argv[1]

        # check if path is given as argument or too much arguments
        if num_of_args == 1 or num_of_args > 2:
            print(WRONG_NUMBER_OF_ARGS)
        else:
            # make it absolute path anyway
            abs_path = os.path.abspath(input)

            # check if path exists and it's a directory
            if os.path.isdir(os.path.join(input)):
                for file_name in os.listdir(abs_path):
                    if file_name.endswith(SOURCE_FILE_EXTENSION):
                        Parser.Parser(abs_path, "/" + file_name)
            # check if there is a regular file with that name
            elif os.path.exists(os.path.join(input)):
                file_name = os.path.split(abs_path)[1]
                path = os.path.split(abs_path)[0] + "/"
                if file_name.endswith(SOURCE_FILE_EXTENSION):
                    Parser.Parser(path, file_name)
                else:
                    print(WRONG_EXTENSION)

            # otherwise, the input path to the program does not exist
            else:
                print(PATH_DOESNT_EXIST)

    if __name__ == "__main__":
        main()
