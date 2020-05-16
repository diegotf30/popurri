from popurri_memory_tokens import *


class MemoryHandler():

    def __init__(self):
        '''
        mem_context_list : [GLOBAL, LOCAL, TEMPORAL]
        '''
        self.mem_context_list = [Memory([0, 0, 0, 0])] * 3

    def updateMemory(self, address=None, value=None, dtype=None):
        '''
        Updates a particular mem stack size
        '''

        context, address = self.getAddressContext(address)

        # updates the corresponding type list
        self.mem_context_list[context].updateTypeStackSize(dtype)

        # inserts value in the corresponding type list
        self.mem_context_list[context].updateAddress(
            address=address, dtype=dtype, value=value)

    def getAddressContext(self, address):
        if address >= 10000 and address <= 19999:
            return (GLOBAL, address - 10000)
        elif address >= 20000 and address <= 29999:
            return (LOCAL, address - 20000)
        elif address >= 30000 and address <= 39999:
            return (TEMPORAL, address - 30000)
        else:
            return (None, None)


class Memory():

    def __init__(self, sizes=None):
        '''
        Lists size can be redefined after creating a Memory object.
        '''
        self.list_types = [] * 4

        for dtype in [INT, FLOAT, BOOL, STRING]:
            self.list_types[dtype] = sizes[dtype]

    def updateTypeStackSize(self, dtype=None):
        if dtype is None:
            return False

        self.list_types[dtype].append(None)

        return True

    def getAddressStack(self):
        '''
        return a tuple of list_types
        '''
        return tuple(self.list_types)

    def updateAddress(self, address=None, dtype=None, value=None):
        '''
        address is the index after offset. Ej. Address:5024 -> 24.
        dtype is the on of the possible data types used by popurri
        value is the actual value to be recorded in the current address 
        '''

        if type is None or value is None:
            return False

        self.list_types[dtype][address] = value

        return True

    def getAddressValue(self, list_address=None, dtype=None):
        '''
        list_address is the index after offset. Ej. Address:5024 -> 24.
        dtype is the on of the possible data types used by popurri
        '''
        return self.list_types[dtype][list_address]
