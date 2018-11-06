
# constants:
STATIC = 'static'
FIELD = 'field'
ARG = 'argument'
VAR = 'var'
TYPE = 0
KIND = 1
KIND_INDEX = 2

"""
A symbol table that associates names with information needed for Jack compilation:
type, kind, and running index. The symbol table has 2 nested scopes (class/subroutine).
"""


class SymbolTable:

    def __init__(self):
        # according to the implementation tip, implemented using two separate hash tables
        # one for the class scope and another one for the sub- routine scope.
        # (in python dictionaries are implemented internally by hash tables)
        self.class_scope_symbols = {}
        self.subroutine_scope_symbols = {}

        # initialize counters for the different kinds of vars of class and subroutine
        self.kind_indexes = {STATIC: 0, FIELD: 0, ARG: 0, VAR: 0}

    def reset_subroutine(self):
        """
        Clears the subroutine symbol table and
        Resets the counters of ARG and VAR in kind_indexes dictionary
        """
        self.subroutine_scope_symbols.clear()
        self.kind_indexes[ARG] = 0
        self.kind_indexes[VAR] = 0

    def start_subroutine(self):
        """
        Starts a new subroutine scope.
        """
        self.reset_subroutine()

    def define(self, name, type, kind):
        """
        Defines a new identifier of a given name, type, and kind and assigns it a
        running index. STATIC and FIELD identifiers have a class scope, while ARG and
        VAR identifiers have a subroutine scope.
        :param name: name of identifier
        :param type: type of identifier
        :param kind: kind of identifier
        """
        # I assume the input kind is correct(Static, Field, Argument, Var)
        if kind in [STATIC, FIELD]:
            self.class_scope_symbols[name] = (type, kind, self.kind_indexes[kind])
        elif kind in [ARG, VAR]:
            self.subroutine_scope_symbols[name] = (type, kind, self.kind_indexes[kind])
        self.kind_indexes[kind] += 1

    def var_count(self, kind):
        """
        Returns the number of variables of the given kind already defined in the current
        scope.
        :param kind: The name of the kind
        :return: the counter for this kind according to kind_indexes dictionary
        """
        return self.kind_indexes[kind]

    # This method replaces the methods: kind_of, type_of, index_of in the API suggestion
    def property_of_named_identifier(self, name, prop):
        """
        Returns the property(kind or type or kind index) of the named identifier
        in the current scope.
        Returns NONE if the identifier is unknown in the current scope.
        :param name: name of the identifier
        :param prop: 0 for TYPE, 1 for KIND, 2 for KIND_INDEX
        :return: the suitable property for this identifier in the current scope
        """
        if name in self.subroutine_scope_symbols:
            return self.subroutine_scope_symbols[name][prop]
        elif name in self.class_scope_symbols:
            return self.class_scope_symbols[name][prop]
        else:
            return None
