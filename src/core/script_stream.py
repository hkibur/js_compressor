from . import regex, huffman
from ..components import object_proxy

def sub_callback(reg, protect_comments = True, protect_quotes = True):
    def call(func):
        def dispatch(*args):
            fixed_func = (lambda minfo, *args, this=args[0]: func(this, minfo, *args)) \
                         if len(args) == 2 else func
            args[-1].do_substitution(reg, fixed_func, protect_comments, protect_quotes)
        dispatch.undecorated = func
        return dispatch
    return call

def proc_return(args):
    if args is None:
        return "", tuple()
    if isinstance(args, tuple):
        return args[0], tuple(args[1:])
    return args, (len(args),)

class ScriptStream(object):
    def __init__(self, raw):
        self.raw = raw
        self.symbols = {}

        self.quote_intervals = []
        self.calc_quote_intervals()

        self.comment_intervals = []
        self.calc_comment_intervals()

        print(self.comment_intervals)

    def calc_quote_intervals(self):
        cur_type = None
        cur_start = None
        for i, char in enumerate(self.raw):
            if char == "\"" or char == "'":
                if self.raw[i - 1] == "\\":
                    continue
                if cur_start is None:
                    cur_type = char
                    cur_start = i
                elif char == cur_type:
                    self.quote_intervals.append([cur_start, i])
                    cur_type = None
                    cur_start = None

    def calc_comment_intervals(self):
        cur_start = None
        for i in range(len(self.raw)):
            if self.in_quotes(i):
                continue
            if cur_start is None and self.raw[i:i + 2] == "//":
                cur_start = i
            elif cur_start is not None and self.raw[i] == "\n":
                self.comment_intervals.append([cur_start, i])
                cur_start = None

    def in_interval(self, intervals, index):
        for interval in intervals:
            if interval[0] <= index <= interval[1]:
                return True
        return False

    def in_quotes(self, index):
        return self.in_interval(self.quote_intervals, index)

    def in_comment(self, index):
        return self.in_interval(self.comment_intervals, index)

    def add_symbol(self, symbol, *script_indecies):
        if symbol not in self.symbols.keys():
            self.symbols[symbol] = []
        self.symbols[symbol].extend(script_indecies)

    def apply_offset_at(self, index, offset):
        for _, indecies in self.symbols.items():
            for i in range(len(indecies)):
                if indecies[i] > index:
                    indecies[i] += offset
        for interval in (self.quote_intervals + self.comment_intervals):
            if interval[1] > index:
                interval[0] += index
                interval[1] += index
            elif interval[0] < index <= interval[1]:
                interval[1] += index

    def insert_at(self, index, string):
        self.raw = self.raw[:index] + string + self.raw[index:]
        self.apply_offset_at(index, len(string))

    def add_header(self, header_raw):
        self.apply_offset_at(0, len(header_raw))
        self.raw = header_raw + self.raw

    def do_substitution(self, reg, callback, protect_comments, protect_quotes):
        minfo = regex.MatchInfo()

        def call(match, minfo):
            minfo.set_match(match)
            if (protect_comments and self.in_comment(minfo.start)) or (protect_quotes and self.in_quotes(minfo.start)):
                return minfo.matched
            thing = proc_return(callback(minfo, *match.groups()))
            replace, symbol_indecies = thing
            minfo.apply_offset(len(replace) - len(minfo.matched))
            for symbol_index in symbol_indecies:
                self.apply_offset_at(minfo.start + symbol_index, symbol_index - len(minfo.matched))
            return replace
            
        self.raw = reg.sub(lambda match, minfo=minfo: call(match, minfo), self.raw)

    def test_symbols(self):
        for i, item in enumerate(self.symbols.items()):
            symbol, indecies = item
            for index in indecies:
                self.insert_at(index, "<{}>".format(i))
        return self.raw

    def resolve_symbols(self):
        huff = huffman.ScopedHuffman()
        for symbol, indecies in self.symbols.items():
            huff.record_symbol(symbol, num=len(indecies))
        huff.build()
        for symbol, indecies in self.symbols.items():
            for index in indecies:
                self.insert_at(index, huff.get_code_from_symbol(symbol))
        return self.raw