
segments = {'var': 'local', 'field': 'this', 'static': 'static', 'argument': 'argument'}


class VMWriter:
    """
    This class writes VM commands into a file. It encapsulates the VM command syntax.
    """
    def __init__(self, vm_file):
        # list of output vm lines, in the end it will be written to the output vm file
        self.vm_lines = []
        # open the output vm file for writing
        self.vm_file = open(vm_file, 'w')

        self.file_name = ""

    def set_file_name(self, file_name):
        self.file_name = file_name

    def write_push(self, segment, index):
        """
        Writes a VM push command
        :param segment: name of the segment we push
        :param index: index
        """
        self.vm_lines.append('push ' + segment + ' ' + str(index) + "\n")

    def write_pop(self, segment, index):
        """
        Writes a VM pop command
        :param segment: name of the segment we pop
        :param index: index
        """
        self.vm_lines.append('pop ' + segment + ' ' + str(index) + "\n")

    def write_arithmetic(self, command):
        """
        Writes a VM arithmetic command
        :param command: the arithmetic command
        """
        self.vm_lines.append(command + "\n")

    def write_label(self, label):
        """
        Writes a VM label command
        :param label: the name of the label
        """
        self.vm_lines.append('label ' + label + "\n")

    def write_go_to(self, label):
        """
        Writes a VM GO-TO command
        :param label: the name of the label we should go to
        """
        self.vm_lines.append('goto ' + label + "\n")

    def write_if(self, label):
        """
        Writes a VM If-goto command
        :param label: name of the label
        """
        self.vm_lines.append('if-goto ' + label + "\n")

    def write_call(self, name, number_of_args):
        """
        Writes a VM call command
        :param name: name of the callee
        :param number_of_args: number of arguments to the callee
        """
        self.vm_lines.append('call ' + name + ' ' + str(number_of_args) + "\n")

    def write_function(self, name, number_of_locals):
        """
        Writes a VM function command
        :param name: name of the function
        :param number_of_locals: number of local variables
        """
        self.vm_lines.append('function ' + name + ' ' + str(number_of_locals) + "\n")

    def write_return(self):
        """
        Writes a VM return command
        """
        self.vm_lines.append('return' + "\n")

    def close(self):
        """ close the output file """
        self.vm_file.close()

    def print_vm_lines(self):
        for line in self.vm_lines:
            print(line)

    def write_output_vm_file(self):
        """
        Writes the lines in the vm_lines list into the output vm file
        :return:
        """
        for item in self.vm_lines:
            self.vm_file.write("{}".format(item))
        self.close()

