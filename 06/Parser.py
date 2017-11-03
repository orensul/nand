import SymbolTable
import Code
import re
import Assembler


class Parser:
    """
        Encapsulates access to the input code. Reads an assembly language command,
        parses it, and provides convenient access to the commands components
        (fields and symbols). In addition, removes all white space and comments.
    """

    COMMENT = "//"
    A_TAG = '@'
    LABEL_BEGIN = '('
    LABEL_END = ')'
    A_INSTRUCTION = 0
    C_INSTRUCTION = 1
    L_INSTRUCTION = 2

    def __init__(self, folder_path, file_name):
        # construct an empty symbol table with the predefined symbols
        self.symbol_table = SymbolTable.SymbolTable()
        self.code = Code.Code()

        # initialize the class variables
        self.n = 16
        self.file_path = folder_path + file_name
        self.output_file_path = folder_path + file_name.replace \
            (Assembler.SOURCE_FILE_EXTENSION, Assembler.DEST_FILE_EXTENSION)
        self.curr_instruction = ""
        self.curr_instruction_num = -1
        self.assembly_lines = []
        self.binary_lines = []

        # read the file and saving the lines of the files in assembly_lines list
        self.read_file(self.file_path)
        # assemble the instructions in binary by scanning the assembly_lines list
        self.assemble()

    def instruction_type(self):
        """
        This method is responsible to return 0 or 1 or 2 corresponding to the current
        instruction type
        :return:
        """
        if self.curr_instruction.startswith(self.A_TAG):
            return self.A_INSTRUCTION
        if self.curr_instruction.startswith(self.LABEL_BEGIN) and \
                self.curr_instruction.endswith(self.LABEL_END):
            return self.L_INSTRUCTION

        return self.C_INSTRUCTION

    def read_file(self, file_path):
        # open the input asm file for reading
        file = open(file_path, 'r').read().splitlines()

        for line in file:
            # remove spaces from the line (leading and trailing)
            line = line.strip()
            # if there is a comment in the line we will take the string from
            # the beginning of the line to the comment (without the comment)
            if self.COMMENT in line:
                line = line.split(self.COMMENT)[0].strip()
            # if the line is not empty and is not a comment line we will add
            # this line to our assembly_lines list
            if not line.startswith(self.COMMENT) and line:
                self.assembly_lines.append(line)

    def print_binary_lines(self):
        for line in self.binary_lines:
            print(line)

    def print_assembly_lines(self):
        for line in self.assembly_lines:
            print(line)

    def handle_c_instruction(self, instruction):
        """
        This method is responsible to translate C instruction to binary and add it to
        binary_lines list
        :param instruction:
        :return:
        """
        # extracts the dest, comp and jump strings from the instruction
        if '=' in instruction and ';' in instruction:
            dest = instruction.split('=')[0]
            comp = instruction.split('=')[1]
            jump = instruction.split(';')[1]
        elif '=' in instruction and ';' not in instruction:
            dest = instruction.split('=')[0]
            comp = instruction.split('=')[1]
            jump = 'null'
        elif '=' not in instruction and ';' in instruction:
            dest = 'null'
            comp = instruction.split(';')[0]
            jump = instruction.split(';')[1]

        # using the methods of Code class we will get the corresponding binary of
        # comp, dest and jump, then after concatenation binary_value will be the result
        binary_value = self.code.comp(comp.strip()) + self.code.dest(dest.strip()) + \
                       self.code.jump(jump.strip())

        # add it to our binary_lines list
        self.binary_lines.append(binary_value)

    def handle_l_instruction(self):
        """
        This method is responsible to add L instruction into the symbol table
        :return:
        """
        # takes the label from the string the xxx from (xxx)
        label = self.curr_instruction[1:-1]
        # adding this label to the symbol table, the current instruction counter will
        # be the address value for this symbol
        self.symbol_table.add_entry(label, self.curr_instruction_num + 1)

    def handle_a_instruction(self):
        """
        This method is responsible to translates A instruction and add the binary
        translation into the binary_lines list
        :return:
        """
        # regex of a number
        num_re = re.compile(r'\d+')
        # check if the current A instruction has number or not after @
        if re.match(num_re, self.curr_instruction[1:]):
            binary_line = bin(int(self.curr_instruction[1:]))[2:].zfill(16)
        # it's not a number, so it's a symbol, it can be in the symbols table or
        # a new one
        else:
            # if the current instruction contains symbol which has already exist in the
            # symbol table we will use the symbol table to get the address and convert
            # it from decimal to binary
            if self.symbol_table.contains(self.curr_instruction[1:]):
                binary_line = bin(self.symbol_table.get_address
                                  (self.curr_instruction[1:]))[2:].zfill(16)
            # otherwise, we will add the new symbol to the table and use the property
            # self.n to be the address of the variable (starts from 16)
            else:
                self.symbol_table.add_entry(self.curr_instruction[1:], self.n)
                binary_line = bin(self.symbol_table.get_address
                                  (self.curr_instruction[1:]))[2:].zfill(16)
                self.n += 1
        # now after we finished and extracted the binary value of the instruction,
        # we will add it to the binary_lines list
        self.binary_lines.append(binary_line)

    def advance(self, instruction):
        """
        This method is responsible to saves the current instruction and increase the
        instruction's counter if it's A or C instruction
        :param instruction:
        :return:
        """
        self.curr_instruction = instruction
        if not self.instruction_type() == self.L_INSTRUCTION:
            self.curr_instruction_num += 1

    def first_pass(self):
        """
        This method is responsible to scan the instructions list and look only for labels
        the purpose is to add the labels with the address of current instruction counter
        into the symbol table, so in the second scan we will have the labels in the table
        with their corresponding line number of the following instruction of this label
        :return:
        """
        for instruction in self.assembly_lines:
            # read the next instruction makes it the current instruction and increase
            # the curr_command_num counter
            self.advance(instruction)
            # check if the instruction type if label
            if self.instruction_type() == self.L_INSTRUCTION:
                self.handle_l_instruction()

    def second_pass(self):
        """
        This method is responsible to handle A,C instructions, it will be run after we
        called the first pass which takes cares of L instructions
        :return:
        """
        # initialize the current instruction counter for the beginning of the second scan
        self.curr_instruction_num = -1
        for instruction in self.assembly_lines:
            # read the next instruction makes it the current instruction and increase
            # the curr_command_num counter
            self.advance(instruction)
            # check if the instruction is A type or C type and handle the instruction
            if self.instruction_type() == self.A_INSTRUCTION:
                self.handle_a_instruction()
            elif self.instruction_type() == self.C_INSTRUCTION:
                self.handle_c_instruction(self.curr_instruction)

    def assemble(self):
        """
        This method calls two methods for scan the instructions list twice and parse it
        :return:
        """
        # call first_pass - first we will handle the labels instructions
        self.first_pass()
        self.second_pass()

        self.write_output_hack_file()
        #self.print_assembly_binary_lines()

    def print_assembly_binary_lines(self):
        """
        This method is responsible to print the binary_lines list
        :return:
        """
        for i in range(0, len(self.binary_lines)):
            print("assembly line: " + self.assembly_lines[i] + " binary line: " +
                  self.binary_lines[i])

    def write_output_hack_file(self):
        """
        This method is responsible to write the binary_list into the output file
        :return:
        """
        with open(self.output_file_path, 'w') as file_handler:
            for item in self.binary_lines:
                file_handler.write("{}\n".format(item))
        # close the output file
        file_handler.close()
