import popurri_tokens as p_t  # probablemente ni usemos esto
import error_tokens as e  # probablemente si usemos esto
import popurriRuleHandler as prh
# import _ as popurri_parser
# import _ as popurri_listener
# import _ as popurri_lexer
from antlr4 import ParseTreeWalker

# 10000 direcciones para cada tipo [INT, FLOAT, STRING, BOOL]
MEM_DEFAULT = 10000


class Compiler(object):

    def __init__(self, file_stream=None, mem_size=MEM_DEFAULT):
        self.file_stream = file_stream
        self.pListener = prh.PopurriRuleHandler(mem_size=mem_size)
        self.int_mem_counter = self.float_mem_counter = self.string_mem_counter = self.bool_mem_counter = 0
        self.int_mem_slots = self.float_mem_slots = self.string_mem_slots = self.bool_mem_slots = [] * mem_size

    def compile(self):
        lexer = PopurriLexer()
        stream = CommonTokenStream()
        parser = PopurriParser()

        tree = parser.module()

        walker = ParseTreeWalker()
        walker.walk(self.pListener, tree)


# Testing purposes
if __name__ == '__main__':
    compiler = Compiler()
    compiler.compile()
