class SymbolTable:
    def __init__(self):
        # Predefined symbols
        self._symbols_table = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4,
                               'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9,
                               'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13,
                               'R14': 14, 'R15': 15, 'SP': 0, 'LCL': 1,
                               'ARG': 2, 'THIS': 3, 'THAT': 4, 'SCREEN': 16384,
                               'KBD': 24576}

    def add_entry(self, symbol, address):
        """
        Adds tuple of symbol and value(=address) into the symbolTable
        dictionary
        :param symbol:
        :param address:
        :return:
        """
        self._symbols_table[symbol] = address

    def contains(self, symbol):
        """
        :param symbol:
        :return: True if symbol exists in the dictionary symbols_table,
        otherwise, returns false.
        """
        return symbol in self._symbols_table

    def get_address(self, symbol):
        """
        :param symbol:
        :return: The value of the symbol in the symbolTable dictionary
        """
        return self._symbols_table[symbol]

    def print_symbols_table(self):
        for symbol, value in self._symbols_table.items():
            print("Key: " + symbol +"\n" + "Value: " + str(value) + "\n")

