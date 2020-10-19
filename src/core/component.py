from . import regex, script_stream

class CompressionComponent(object):
    def __init__(self, stream):
        self.stream = stream
        self.referenced_symbols = []

    @script_stream.sub_callback(regex.DEFINED_VARIABLE_REGEX)
    def get_symbol_refs(self, minfo, prefix, symbol):
        if symbol not in self.referenced_symbols:
            return minfo.matched
        self.stream.add_symbol(symbol, minfo.start + len(prefix))
        return prefix, len(prefix)

    def run(self):
        raise NotImplementedError()