from popurri_memory_tokens import *
import math

# 9999 / 4 = 2499
TYPE_OFFSET = 2499
CONTEXT_TOKEN_OFFSET = 4


class MemoryHandler():

    contextConversion = {
        'global': GLOBAL,
        'class': LOCAL,
        'function': LOCAL,
    }

    dataTypes = {
        'int': INT,
        'float': FLOAT,
        'bool': BOOL,
        'string': STRING,
    }

    memoryContextStartingPoint = {
        GLOBAL: 10000,
        LOCAL: 20000,
        TEMPORAL: 30000,
        CONSTANT: 40000,
    }

    def __init__(self):
        '''
        mem_context_list : [GLOBAL, LOCAL, TEMPORAL]
        '''
        self.mem_context_list = []
        for _ in range(0, 5):
            self.mem_context_list.append(Memory())

    def getTypeFromValue(self, value=None):
        value_type = None

        if type(value) is int:
            value_type = 'int'
        elif type(value) is float:
            value_type = 'float'
        if type(value) is bool:
            value_type = 'bool'
        if type(value) is str:
            value_type = 'string'

        return self.dataTypes[value_type]

    def getTypeFromRawString(self, raw_type=None):
        return self.dataTypes[raw_type]

    def reserveMemoryAddress(self, context=None, dtype=None, value=None):
        '''
        this function will reserve an address for the corresponding source call.

        '''

        quadrant_memory = self.memoryContextStartingPoint[context]

        context -= CONTEXT_TOKEN_OFFSET

        relative_memory = self.mem_context_list[context].updateTypeStackSize(
            dtype)

        address = quadrant_memory + (TYPE_OFFSET * dtype) + relative_memory

        if value is not None:
            self.mem_context_list[context].updateAddress(
                address=relative_memory, dtype=dtype, value=value)

        return address

    def updateMemory(self, address=None, value=None):
        '''
        Updates a particular mem stack size/value
        this functions should be used only by PopurriListener.py
        '''

        context, address = self.getAddressContext(address)

        # obtains the data type from the address [INT, FLOAT, BOOL, STRING]
        dtype = math.floor(address / TYPE_OFFSET)

        # obtains the relative address within context address stack [1 -> TYPE_OFFSET]
        address -= (dtype * TYPE_OFFSET)

        # updates the corresponding type list
        # self.mem_context_list[context].updateTypeStackSize(dtype)

        if value is not None:
            # inserts value in the corresponding type list
            self.mem_context_list[context - CONTEXT_TOKEN_OFFSET].updateAddress(
                address=address, dtype=dtype, value=value)

    def getAddressContext(self, address):
        '''
        given the address return the context [GLOBAL, LOCAL, TEMPORAL] 
        and removes the offset from the address [this new address is returned too]
        10000 -> 19999 : GLOBAL
        20000 -> 29999 : LOCAL
        30000 -> 39999 : TEMPORAL
        40000 -> 49999 : CONSTANT
        '''
        if address >= 10000 and address <= 19999:
            return (GLOBAL, address - 10000)
        elif address >= 20000 and address <= 29999:
            return (LOCAL, address - 20000)
        elif address >= 30000 and address <= 39999:
            return (TEMPORAL, address - 30000)
        elif address >= 40000 and address <= 49999:
            return (CONSTANT, address - 40000)
        else:
            return (None, None)

    def getAddressValue(self, address):
        context, address = self.getAddressContext(address)

        dtype = math.floor(address / 2499)

        address -= (dtype * 2499)
        print(dtype, address)
        return self.mem_context_list[context - CONTEXT_TOKEN_OFFSET].getAddressValue(address, dtype)

    def getAdressStack(self, context):
        return self.mem_context_list[context - CONTEXT_TOKEN_OFFSET].list_types

    def copyAddressType(self, address):
        _, address = self.getAddressContext(address)

        dtype = (address / TYPE_OFFSET)

        return dtype

    def getContextByRawString(self, context=None):
        if context[:5] == 'class':
            context = 'class'
        elif context[:4] == 'func':
            context = 'function'
        return self.contextConversion[context]


class Memory():

    def __init__(self):
        '''
        Lists size can be redefined after creating a Memory object.
        '''
        self.list_types = [None] * 4

        for dtype in range(0, 4):
            self.list_types[dtype] = []

    def updateTypeStackSize(self, dtype=None):
        '''
        Increase the list size of a certain type[INT, FLOAT, BOOL, STRING]
        this function simulates the addition of another slot of a certain type
        '''
        if dtype is None:
            return False

        self.list_types[dtype].append(None)

        return len(self.list_types[dtype])

    def getContextStack(self):
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

        self.list_types[dtype][address-1] = value

        return True

    def getAddressValue(self, address=None, dtype=None):
        '''
        list_address is the index after offset. Ej. Address:5024 -> 24.
        dtype is the on of the possible data types used by popurri
        '''

        print(self.list_types[dtype][address - 1], dtype, address - 1)
        return self.list_types[dtype][address - 1]
