from ..core import component, regex, script_stream

class AnonFunctionComponent(component.CompressionComponent):
    def __init__(self, stream):
        super().__init__(stream)

    @script_stream.sub_callback(regex.ANON_FUNC_REGEX)
    def get_anon_funcs(self, minfo, params):
        if not params:
            return "()=>"
        elif len(params.split(",")) == 1:
            self.referenced_symbols.append(params)
            return "{}=>".format(params)
        else:
            return "({})=>".format(params)

    @script_stream.sub_callback(regex.NAMED_FUNC_REGEX)
    def get_named_funcs(self, minfo, name, params):
        var_prefix = "var "
        self.referenced_symbols.append(name)
        self.stream.add_symbol(name, minfo.start + len(var_prefix))
        return var_prefix + " = " + self.get_anon_funcs.undecorated(self, None, params)

    @script_stream.sub_callback(regex.FUNC_PARAMS_REGEX)
    def get_params(self, minfo, param_name, equals):
        self.referenced_symbols.append(param_name)
        self.stream.add_symbol(param_name, minfo.start)
        return "=" if equals else ""

    def run(self):
        self.get_anon_funcs(self.stream)
        self.get_named_funcs(self.stream)
        print(self.referenced_symbols)
        self.get_params(self.stream)
        self.get_symbol_refs(self.stream)