from ..core import component, regex, script_stream

class DefinedVariableComponent(component.CompressionComponent):
    @script_stream.sub_callback(regex.VAR_DEFINE_REGEX)
    def get_var_defines(self, minfo, def_type, symbol):
        if regex.is_keyword(symbol):
            return minfo.matched
        self.stream.add_symbol(symbol, minfo.start + len(def_type) + 1)
        self.referenced_symbols.append(symbol)
        return def_type + " ", len(def_type) + 1

    def run(self):
        self.get_var_defines(self.stream)
        self.get_symbol_refs(self.stream)