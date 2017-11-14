
# Constants which are relevant to the CodeWriter class
LABEL_BEGIN = '('
LABEL_END = ')'
SP_START_ADDRESS = '256'
C_ARITHMETIC = 0
C_PUSH = 1
C_POP = 2
C_LABEL = 3
C_GO_TO = 4
C_IF = 5
C_FUNCTION = 6
C_RETURN = 7
C_CALL = 8
C_ERROR = 9
LCL = 'local'
ARG = 'argument'
THIS = 'this'
THAT = 'that'
PTR = 'pointer'
TEMP = 'temp'
CONST = 'constant'
STATIC = 'static'
REG = 'reg'


class CodeWriter:

    """The CodeWriter class Translates VM commands into Hack assembly code. """

    def __init__(self, asm_file):

        # first, initialization of dictionaries which will be used by this class
        # arithmetic operations:
        self._arithmetic_name = dict()
        self._arithmetic_name.update({'add': '+', 'sub': '-', 'or': '|', 'and': '&',
                                      'neg': '-', 'not': '!', 'eq': 'JEQ', 'gt': 'JGT',
                                      'lt': 'JLT'})
        # commands:
        self._command_type = dict()
        self._command_type.update({'C_ARITHMETIC': 0, 'C_PUSH': 1, 'C_POP': 2,
                                   'C_LABEL': 3, 'C_GO_TO': 4, 'C_IF': 5})

        # command type-name mapping:
        self._command_mapping = dict()
        self._command_mapping.update({'add': 'C_ARITHMETIC', 'sub': 'C_ARITHMETIC',
                                      'neg': 'C_ARITHMETIC', 'eq': 'C_ARITHMETIC',
                                      'gt': 'C_ARITHMETIC', 'lt': 'C_ARITHMETIC',
                                      'and': 'C_ARITHMETIC', 'or': 'C_ARITHMETIC',
                                      'not': 'C_ARITHMETIC', 'push': 'C_PUSH',
                                      'pop': 'C_POP', 'label': 'C_LABEL',
                                      'if-goto': 'C_IF', 'goto': 'C_GO_TO'})
        # segments
        self._segment = dict()
        self._segment.update({'local': 'LCL', 'argument': 'ARG', 'this': 'THIS',
                              'that': 'THAT', 'pointer': 'PTR', 'temp': 'TEMP',
                              'constant': 'CONST', 'static': 'STATIC', 'reg': 'REG'})

        # registers
        self._register = dict()
        self._register.update({'SP': 'R0', 'local': 'R1', 'argument': 'R2',
                               'this': 'R3', 'that': 'R4', 'temp': 'R5',
                               'pointer': 'R3', 'REG_COPY': 'R13'})

        # prepare the output asm file to be ready to be written
        self._asm_file = open(asm_file, 'w')

        # list which will hold the lines in the output asm file
        self._asm_lines = []

        # we save the number of the label we will generate so it will makes the labels
        # with different names.
        self._label_num = 0

        self._file_name = ""

        self.curr_func_name = "Main.main"

        # initialize the Stack pointer to start from 256
        self.write_init()

    def get_command_mapping_dict(self):
        """
        Getter method for the command mapping dict
        """
        return self._command_mapping

    def get_command_type_dict(self):
        """
        Getter method for the command type dict
        """
        return self._command_type

    def write_init(self):
        """
        Writes assembly code that effects the VM initialization, also called
        bootstrap code. This code must be placed at the beginning of the output file.
        """
        # initialize the SP to points to 256 by RAM[0] = 256
        self.append_address(SP_START_ADDRESS)
        self.change('D', 'A')
        self.append_address(self._register.get('SP'))
        self.change('M', 'D')

        # call Sys.init
        self.write_call('Sys.init', '0');

    def write_call(self, function_name, num_of_args):
        """
        Writes assembly code that effects the call command
        :param function_name: name of the function
        :param num_of_args: number of arguments to the function we call
        """
        # Each VM function call should generate and insert into the translated
        # code stream a unique symbol that serves as a return address, namely
        # the memory location of the command following the function call.

        label_name = self.curr_func_name + '$Ret' + str(self._label_num)
        print(label_name)
        # push return-address using the label declared below
        self.append_address(label_name)
        self.change('D', 'A')
        self.push('D')

        # saves LCL, ARG, THIS, THAT of the calling function
        self.push_register_or_memory_segment('LCL', 0, 'M')
        self.push_register_or_memory_segment('ARG', 0, 'M')
        self.push_register_or_memory_segment('THIS', 0, 'M')
        self.push_register_or_memory_segment('THAT', 0, 'M')

        # Reposition ARG: ARG = SP - numOfArgs - 5
        self.append_address('SP')
        self.change('D', 'M')
        self.append_address(num_of_args)
        self.change('D', 'D-A')
        self.append_address(5)
        self.change('D', 'D-A')
        self.append_address('ARG')
        self.change('M', 'D')

        # Reposition LCL: LCL = SP
        self.append_address('SP')
        self.change('D', 'M')
        self.append_address('LCL')
        self.change('M', 'D')

        # the goto code to the function: function_name
        self.write_goto(function_name)

        # declare the label for the return address (return address)
        self.append_label(label_name)


    def write_arithmetic(self, command):
        """
        This Method is responsible to translate given arithmetic command to the asm
        suitable command.
        :param command: command
        """
        # extract the correct operation according to the arithmetic from the dictionary
        # (for example add is "+")
        operation = self._arithmetic_name.get(command)

        if command == 'add' or command == 'sub' or command == 'or' or command == 'and':
            self.dec_sp()
            self.pop('D')
            self.peek('A')
            self.change('D', 'A' + operation + 'D')
            self.push('D')
        elif command == 'neg' or command == 'not':
            self.dec_sp()
            self.peek('D')
            self.change('D', operation + 'D')
            self.push('D')
        elif command == 'lt' or command == 'gt' or command == 'eq':
            self.dec_sp()
            self.pop('D')
            self.peek('A')
            self.change('D', 'A-D')

            # it's important to add the _label_num to the label name, otherwise, if we
            # have several eq_label for example, it will jump to the last of them which
            # will be a bug!
            label = "_label" + str(self._label_num)

            # vm represents true as -1 (minus one, 0xFFFF) and false as  0 (zero, 0x0000)
            self.append_jump_to_label(command + label, operation)
            self.push('0')
            self.append_jump("n_" + command + label)
            self.append_label(command + label)
            self.push('-1')
            self.append_label("n_" + command + label)
        else:
            print("Invalid Arithmetic command")

    def append_label(self, label_name):
        """ Adds to the asm_lines list a line of label declaration (Label_name)
            :param label_name: the name of the label
        """
        self._asm_lines.append(LABEL_BEGIN + label_name + LABEL_END)
        self._label_num += 1

    def append_conditional_jump(self, input_to_jump_command, condition):

        """ Adds to the asm_lines list a line of jump to label
            :param input_to_jump_command:
            :param condition: condition of the jump for example JEQ
        """
        self._asm_lines.append(input_to_jump_command + ";" + condition)

    def append_jump(self, label_name):
        """ Adds to the asm_lines list the two lines of jump without condition to label
            :param label_name: name of the label we enforce jump to
        """
        self.append_address(label_name)
        self._asm_lines.append('0;JMP')

    def append_jump_to_label(self, label_name, condition):
        """ Adds to the asm_lines list the two lines of jump with a condition
            :param label_name: name of the label we want to jump to
            :param condition: condition of the jump for example JEQ
        """
        self.append_address(label_name)
        self.append_conditional_jump('D', condition)

    def calc_segment_pointer_plus_offset_address(self, segment, index, register):
        """
        This method puts in A the address of segmentPointer + index
        :param segment: the name of the segment from the line in the vm file
        :param index: the numerical part of the command
        :param register: A or D (address or data)
        """
        # A = address = segmentPointer + i
        self.append_address(index)
        self.change('D', 'A')
        self.append_address(segment)
        self.change('A', '' + register + '+D')

    def push_constant_segment(self, index):
        """
        This method do the following: *SP=index
        :param index: the numerical part of constant command
        """
        self.append_address(index)
        self.change('D', 'A')
        self.push('D')

    def push_register_or_memory_segment(self, segment, index, register):
        """
        This method is responsible to translate push segment i
        segment can be one of the following: LCL,AEG,THIS,THAT,TEMP,PTR
        :param segment: the name of the segment from the line in vm file
        :param index: the numerical part of the command
        :param register: A or D
        """
        self.calc_segment_pointer_plus_offset_address(segment, index, register)
        self.change('D', 'M')
        # D = *(segmentPointer + i) = *addr
        # *SP = *addr, SP++
        self.push('D')

    def pop_register_or_memory_segment(self, segment, index, register):
        """
        This method is responsible to translate pop segment i
        segment can be one of the following:  LCL,AEG,THIS,THAT,TEMP,PTR
        :param segment: the name of the segment from the line in vm file
        :param index: the numerical part of the command
        :param register: A or D
        """
        # *R13=addr=segmentPointer+i
        self.calc_segment_pointer_plus_offset_address(segment, index, register)
        self.change('D', 'A')
        self.append_address(self._register.get('REG_COPY'))
        self.change('M', 'D')
        # D=*SP, SP--
        self.dec_sp()
        self.peek('D')
        # A=addr
        self.append_address(self._register.get('REG_COPY'))
        self.change('A', 'M')
        # *addr = D = *SP
        self.change('M', 'D')

    def pop_static_segment(self, label):
        """
         This method is responsible to translate pop segment i
        segment of static
        :param label: the label of the static variable
        """
        # D=*SP
        self.dec_sp()
        self.peek('D')

        self.append_address(label)
        self.change('M', 'D')

    def push_static_segment(self,label):
        """
        This method is responsible to translate push segment i
        segment of static
        :param label: the label of the static variable
        """
        self.append_address(label)
        self.change('D', 'M')
        self.push('D')

    def set_file_name(self, file_name):
        """
        set the file name
        :param file_name: tha name of the file we need to translate
        :return: the name of the file
        """
        self._file_name = file_name

    def create_static_label(self, index):
        """
        This method creates the label of the static variable.
        the label consists of the file name (without it's type) dot the index of the
        static variable.
        :param index: the static number at the vm command
        :return: the label we create
        """
        file_name = self._file_name.split(".")[0]
        return str(file_name) + "." + str(index)

    def write_push_pop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given command, where
        command is either C_PUSH or C_POP.
        """
        if command == C_PUSH:
            # it's a PUSH command,
            # check if the segment is memory segment(LCL,ARG,THIS,THAT) or
            # register segment(TEMP,POINTER) or
            # CONSTANT segment
            # STATIC
            if segment == CONST:
                self.push_constant_segment(index)
            elif segment in (LCL, ARG, THIS, THAT):
                self.push_register_or_memory_segment(self._segment.get(segment), index,
                                                     'M')
            elif segment in (TEMP, PTR):
                self.push_register_or_memory_segment(self._register.get(segment), index,
                                                     'A')
            elif segment == STATIC:
                self.push_static_segment(self.create_static_label(index))
            else:
                print("Unsuitable segment")
        elif command == C_POP:
            # it's a POP command,
            # check if the segment is memory segment(LCL,ARG,THIS,THAT) or
            # register segment(TEMP,POINTER) or
            # CONSTANT segment
            # STATIC
            if segment in (LCL, ARG, THIS, THAT):
                self.pop_register_or_memory_segment(self._segment.get(segment), index,
                                                    'M')
            elif segment in (TEMP, PTR):
                self._register.get(segment)
                self.pop_register_or_memory_segment(self._register.get(segment), index,'A')
            elif segment == STATIC:
                self.pop_static_segment(self.create_static_label(index))
            else:
                print("Unsuitable segment")

        else:
            print("Invalid command")

    def append_address(self, address):
        """
        Writes into the output asm file A command (@+address)
        :param address: the address to point to
        """
        address = '@' + str(address)
        self._asm_lines.append(address)

    def change(self, dest, comp):
        """ Writes into the asm_lines list the comp command(dest=comp)
        :param dest:
        :param comp:
        """
        self._asm_lines.append(dest + '=' + comp)

    def write_output_asm_file(self):
        """ This method is responsible to write the asm_list into the output file
        """
        for item in self._asm_lines:
            self._asm_file.write("{}\n".format(item))
        # close the output file
        self.close()

    def close(self):
        """ close the output file """
        self._asm_file.close()

    def inc_sp(self):
        """ Increase the SP in order to access the item in top of the stack by the
        following asm command: @SP M=M+1
        """
        self.append_address('SP')
        self.change('M', 'M+1')

    def dec_sp(self):
        """ Decrease the SP in order to access the item in top of the stack by the
        following asm command: @SP M=M-1
        """
        self.append_address('SP')
        self.change('M', 'M-1')

    def peek(self, dest):
        """ This method implements the peek from stack functionality(in peek we dont
        decrease the SP like in pop). peek will do the following: dest=*SP, by the
        following asm commands:
        @SP
        A=M
        dest=M
        :param dest: dest part(D for example)
        """
        self.append_address('SP')
        self.change('A', 'M')
        self.change(dest, 'M')

    def pop(self, dest):
        """ Pop is like peek but also remove the item in the top of the stack by decrease
        the SP
        :param dest: the dest part
        """
        self.peek(dest)
        self.dec_sp()

    def push(self, comp):
        """ This method implements the push into stack functionality. push will do the
        following: *SP=comp @SP++
        by the following rows of asm:
        @SP
        A=M
        M=comp(for example D)
        @SP
        M=M+1
        :param comp: the comp part
        """
        self.append_address('SP')
        self.change('A', 'M')
        self.change('M', comp)
        self.inc_sp()

    def print_asm_lines(self):
        """
        Method for the convenience of the programmer - to print the asm lines so far.
        """
        for line in self._asm_lines:
            print(line)

    def write_goto(self, label):
        """
        This method writes the assembly commands that effects the goto command
        :param label: the name of the label
        """
        self.append_jump(self.curr_func_name + '$' + label)

    def write_if(self, label):
        """
        This method writes the assembly commands that effects the if-goto command
        :param label: the name of the label
        """
        # D=*SP
        self.dec_sp()
        self.peek('D')
        # A=functionName$label
        # D;JNE
        self.append_jump_to_label(self.curr_func_name + '$' + label, 'JNE')

    def write_label(self, label):
        """
        This method writes the assemble commands that effects the label command
        :param label: the name of the label to write
        """
        self.append_label(self.curr_func_name + '$' + label)

    def write_function(self, function_name, num_locals):
        """
        Writes assembly code that effects the function command
        :param function_name: name of the function
        :param num_locals: number of local variables of the function
        """
        self.append_label(function_name)
        for i in range(num_locals):
            self.push(0)


