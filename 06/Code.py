class Code:
    """
    This class Translates Hack assembly language mnemonics into binary codes.
    """
    def __init__(self):
        """
        Initialize the _dest_table, _comp_table and _jump_table dictionaries.
        :return:
        """
        self._dest_table = {'null': '000', 'M' : '001', 'D' : '010', 'MD' : '011',
                       'A': '100','AM': '101', 'AD': '110', 'AMD': '111'}

        self._comp_table = {'0': '1110101010', '1': '1110111111', '-1': '1110111010',
                       'D': '1110001100', 'A': '1110110000', 'M':'1111110000',
                       '!D': '1110001101', '!A': '1110110001','!M':'1111110001',
                       '-D': '1110001111', '-A': '1110110011', '-M':'1111110011',
                        'D+1': '1110011111', 'A+1': '1110110111', 'M+1': '1111110111',
                        'A-1': '1110110010', 'M-1': '1111110010', 'D+A': '1110000010',
                        'D+M': '1111000010', 'D-A': '1110010011', 'D-M': '1111010011',
                       'D-1': '1110001110', 'M-D': '1111000111', 'A-D': '1110000111',
                        'D&A': '1110000000', 'D&M': '1111000000',  'D|A': '1110010101',
                        'D|M': '1111010101', 'D*A': '110000000', 'D*M': '1101000000',
                        'D>>': '1010010000', 'D<<': '1010110000',
                        'A>>': '1010000000', 'A<<': '1010100000', 'M>>': '1011000000',
                        'M<<': '1011100000'}

        self._jump_table = {'null' : '000', 'JGT': '001', 'JEQ' : '010', 'JGE': '011'
         , 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

    def dest(self, mnemonic):
        """
        This method gets the mnemonic(string) of dest and returns the value in the
        dest dictionary.
        """
        return self._dest_table.get(mnemonic)

    def comp(self, mnemonic):
        """
        This method gets the mnemonic(string) of comp and returns the value in the
        comp dictionary.
        """
        return self._comp_table.get(mnemonic)

    def jump(self, mnemonic):
        """
        This method gets the mnemonic(string) of jump and returns the value in the
        jump dictionary.
        """
        return self._jump_table.get(mnemonic)


