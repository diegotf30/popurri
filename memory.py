from popurri_tokens import *
from error_tokens import *
from copy import deepcopy
import math


class MemoryHandler():
    snapshot = None
    context_offset = None
    type_offset = None

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

        self.contexts = {}
        for i, ctx in enumerate([GLOBAL, LOCAL, TEMPORAL, CONSTANT]):
            self.contexts[ctx] = Memory(
                start=context_offset * i, max_size=self.type_offset)
            if ctx == TEMPORAL:
                self.contexts[ctx] = Memory(
                    start=context_offset * i, max_size=self.type_offset, is_temp=True)
                continue

            self.contexts[ctx] = Memory(
                start=context_offset * i, max_size=self.type_offset)

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

        dtype -= INT
        return ctxMemory.start + reserved_address + (self.type_offset * dtype)

    def update(self, address, value):
        '''
        Updates a particular mem stack size/value
        this functions should be used only by PopurriListener.py
        '''

        address, context = self.getContextAddress(address)
        dtype = self.getAddressType(address)

        if tokenizeByValue(value) != dtype:
            msg = EXPECTED_TYPE.format(stringifyToken(
                dtype), stringifyToken(tokenizeByValue(value)))
            raise Exception(f'ERROR: {msg}')

        # obtains the relative address within context address stack [1 -> TYPE_OFFSET]
        address -= ((dtype - INT) * self.type_offset)
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

    def getAddressType(self, address):
        'obtains the data type from address [INT, FLOAT, BOOL, STRING]'
        return math.floor(address / self.type_offset % 4) + INT

    def getValue(self, address):
        address, context = self.getContextAddress(address)
        dtype = self.getAddressType(address)
        address -= ((dtype - INT) * self.type_offset)

        return self.contexts[context].getValue(address, dtype + 33)

    def saveSnapshot(self, context=LOCAL):
        self.snapshot = deepcopy(self.contexts[context])

    def restoreSnapshot(self, context=LOCAL):
        self.contexts[context] = deepcopy(self.snapshot)

    def flush(self, context=LOCAL):
        start_offset = context - GLOBAL
        self.contexts[context] = Memory(
            start=self.context_offset * start_offset, max_size=self.type_offset)

    def count(self, context=LOCAL):
        'Returns a tuple with the amount of items allocated in each section'
        memCtx = self.contexts[context].sections
        return tuple([len(v) for v in memCtx.values()])


class Memory():
    def __init__(self, start, max_size, is_temp=False):
        self.start = start
        self.sections = {
            INT: [],
            FLOAT: [],
            BOOL: [],
            STRING: []
        }
        if is_temp:
            self.sections[POINTER] = []
        self.max_size = max_size

    def reserveAddress(self, dtype):
        '''
        Increase the list size of the given type (INT, FLOAT, BOOL, STRING).
        returns the local address of the reserved space
        '''
        if len(self.sections[dtype]) == self.max_size:
            raise Exception(
                f'ERROR: Cannot allocate any more values of type "{stringifyToken(dtype)}", limit is {self.max_size}')

        default_val_map = {
            INT: 0,
            FLOAT: 0.0,
            BOOL: False,
            STRING: '',
            POINTER: ''
        }
        self.sections[dtype].append(default_val_map[dtype])
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
