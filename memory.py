from popurri_tokens import *
import math

class MemoryHandler():
    contexts = {}
    context_offset = 10000
    type_offset = int(context_offset / 4)

    def __init__(self, context_offset=10000):
        '''
        Creates 4 memory contexts (GLOBAL, LOCAL, TEMPORAL, CONSTANT) with default size of 10k
        0     ->  9999 : GLOBAL
        10000 -> 19999 : LOCAL
        20000 -> 29999 : TEMPORAL
        30000 -> 39999 : CONSTANT
        '''
        self.context_offset = context_offset
        self.type_offset = int(context_offset / 4)

        if self.type_offset % 1 != 0:
            raise Exception('ERROR: \'context_offset\' must be divisible by 4')

        for i, ctx in enumerate([GLOBAL, LOCAL, TEMPORAL, CONSTANT]):
            self.contexts[ctx] = Memory(start=context_offset * i)

    def reserve(self, context, dtype, value=None):
        'reserves an address; assigns value if given'
        ctxMemory = self.contexts[context]
        reserved_address = ctxMemory.reserveAddress(dtype)

        if value is not None:
            ctxMemory.updateAddress(
                address=reserved_address,
                dtype=dtype,
                value=value
            )

        return ctxMemory.start + reserved_address + (self.type_offset * dtype)

    def update(self, address, value):
        '''
        Updates a particular mem stack size/value
        this functions should be used only by PopurriListener.py
        '''

        address, context = self.getContextAddress(address)

        # obtains the data type from the address [INT, FLOAT, BOOL, STRING]
        dtype = math.floor(address / self.type_offset)

        # obtains the relative address within context address stack [1 -> TYPE_OFFSET]
        address -= (dtype * self.type_offset)
        # Update value
        self.contexts[context].updateAddress(address, dtype, value)

    def getContextAddress(self, address):
        '''
        given the address return the address without offset (GLOBAL, LOCAL, TEMPORAL or CONSTANT)
        and its respective context.
        '''
        for i, ctx in enumerate([GLOBAL, LOCAL, TEMPORAL, CONSTANT]):
            start = self.context_offset * i
            end = self.context_offset * (i + 1) - 1
            if address in range(start, end):
                return (address - start, ctx)

        return (None, None)

    def getValue(self, address):
        address, context = self.getContextAddress(address)
        dtype = math.floor(address / self.type_offset)
        address -= (dtype * self.type_offset)
        print(dtype, address)

        return self.contexts[context].getAddressValue(address, dtype)


class Memory():
    start = -1
    sections = {
        INT: [],
        FLOAT: [],
        STRING: [],
        BOOL: []
    }

    def __init__(self, start):
        self.start = start

    def reserveAddress(self, dtype):
        '''
        Increase the list size of the given type (INT, FLOAT, BOOL, STRING).
        returns the local address of the reserved space
        '''
        self.sections[dtype].append(None)
        return len(self.sections[dtype]) - 1

    def updateAddress(self, address, dtype=None, value=None):
        '''
        address is the index after offset. Ej. Address:5024 -> 24.
        dtype is the on of the possible data types used by popurri
        value is the actual value to be recorded in the current address 
        '''
        if value is None:
            return

        self.sections[dtype][address] = value

    def getValue(self, address, dtype):
        '''
        list_address is the index after offset. Ej. Address:5024 -> 24.
        dtype is the on of the possible data types used by popurri
        '''

        return self.sections[dtype][address]
