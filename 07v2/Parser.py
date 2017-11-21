import VMtranslator
import CodeWriter

COMMENT = "//"


class Parser:
    """ Handles the parsing of a single .vm file, and encapsulates access to the input
        code. It reads VM commands, parses them, and provides convenient access to their
        components. In addition, it removes all white space and comments. """

    def __init__(self, folder_path, vm_file_name):
        self.vm_trans = VMtranslator.VMtranslator()
        self.vm_file_path = folder_path + vm_file_name
        self.output_file_path = folder_path + vm_file_name.replace \
            (VMtranslator.SOURCE_FILE_EXTENSION, VMtranslator.DEST_FILE_EXTENSION)

        self.code_writer = CodeWriter.CodeWriter(self.output_file_path)
        self.code_writer.set_file_name(vm_file_name)
        self.curr_command = ""
        self.vm_lines = []
        self.read_file(self.vm_file_path)
        self.parse()
        # self.code_writer.print_asm_lines()
        self.code_writer.write_output_asm_file()

    def advance(self, command):
        """
        advance the correct command to be the next command in the list of vm lines
        :param command: command to set
        """
        self.curr_command = command

    def arg1(self):
        """ Returns the first argument of the current command.
        In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is returned.
        """
        command_list = self.curr_command.split(" ")
        if self.command_type() == CodeWriter.C_ARITHMETIC:
            return command_list[0]
        return command_list[1]

    def arg2(self):
        """ Returns the second argument of the current command.
        """
        command_list = self.curr_command.split(" ")
        # return the numeric value
        return command_list[2]

    def parse(self):
        """
        The principle method of the Parser class, according to the current command type
        writes the correct asm line by CodeWriter suitable write method.
        """

        for command in self.vm_lines:
            self.advance(command)
            if self.command_type() == CodeWriter.C_ARITHMETIC:
                self.code_writer.write_arithmetic(self.curr_command)
            elif self.command_type() == CodeWriter.C_PUSH:
                 self.code_writer.write_push_pop(CodeWriter.C_PUSH, self.arg1(),
                                                 self.arg2())
            elif self.command_type() == CodeWriter.C_POP:
                self.code_writer.write_push_pop(CodeWriter.C_POP, self.arg1(),
                                                self.arg2())
            else:
                print("Invalid command")

    def read_file(self, vm_file):
        """
        This method opens the vm_file which is the input and extracts his data into
        vm_lines list
        :param vm_file: the path of the vm_file
        """
        # open the input vm file for reading
        file = open(vm_file, 'r').read().splitlines()

        for line in file:
            # remove spaces from the line (leading and trailing)
            line = line.strip()
            # if there is a comment in the line we will take the string from
            # the beginning of the line to the comment (without the comment)
            if COMMENT in line:
                line = line.split(COMMENT)[0].strip()
            # if the line is not empty and is not a comment line we will add
            # this line to our vm_lines list
            if not line.startswith(COMMENT) and line:
                self.vm_lines.append(line)

    def command_type(self):
        """
        Returns the type of the current VM command.
        C_ARITHMETIC is returned for all the arithmetic commands.
        """
        for key, value in self.code_writer.get_command_mapping_dict().items():
            if key in self.curr_command:
                return self.code_writer.get_command_type_dict().get(value)

    def print_vm_lines(self):
        """ Method to the convenience of the programmer which prints the lines of the
        VM file"""
        for line in self.vm_lines:
            print(line)