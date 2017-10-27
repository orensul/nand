import SymbolTable
import Code


class Parser:

    SOURCEFILE = ".asm"
    DEST_FILE = ".hack"
    COMMENT = "//"
    A_TAG = '@'
    LABEL_BEGIN = '('
    LABEL_END = ')'
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2

    def __init__(self, file_path):
        self.instructions_list = {}

        self.symbol_table = SymbolTable.SymbolTable()
        self.file_path = file_path
        self.curr_instruction = ""
        self.curr_instruction_num = -1
        self.lines = []
        self.read_file(file_path)
        self.first_pass()




    def command_type(self):
        if self.curr_instruction.startswith(self.A_TAG):
            return self.A_COMMAND
        if self.curr_instruction.startswith(self.LABEL_BEGIN) and self.curr_instruction.endswith(self.LABEL_END):
            return self.L_COMMAND

        return self.C_COMMAND

    def read_file(self, file_path):

        self.file = open(file_path, 'r').read().splitlines()

        for line in self.file:
            line = line.rstrip()
            if not line.startswith("//") and line:
                self.lines.append(line)

        print(self.lines)

    def first_pass(self):
        for line in self.lines:
            if
            self.symbol_table.add_entry(line, 1)

        self.symbol_table.print_symbols_table()


    #def comp(self):

    #def dest(self):

    #def jump(self):

    #def symbol(self):

    #def command_type(self):

    #def advance(self):

    #def has_more_command(self):

