import SymbolTable
import Code
import Parser
import sys

class Assembler:
    def __init__(self, file_path):
        self.code = Code.Code()
        self.parser = Parser.Parser(file_path)




def main():
    asm = Assembler(sys.argv[1])

if __name__ == "__main__":
    main()

