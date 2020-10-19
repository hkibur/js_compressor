from ..core import component, regex, script_stream

PROXY_HEADER = """var proxy_table = {{{}}};
function make_proxy(obj){{
    return new Proxy(obj, {{get: function(target, attribute){{
        return target[proxy_table[attribute]];
    }}}});
}}"""
TABLE_OFFSET = len("var proxy_table = {")

class ObjectProxyComponent(component.CompressionComponent):
    def __init__(self, stream):
        self.obj_table = []
        self.stream = stream

    @script_stream.sub_callback(regex.OBJECT_ATTRIBUTE_REGEX)
    def get_obj_attribs(self, minfo, symbol):
        if symbol not in self.obj_table:
            self.obj_table.append(symbol)
        self.stream.add_symbol(symbol, minfo.start)

    def run(self):
        self.get_obj_attribs(self.stream)
        table_str = ""
        in_header = {}
        for symbol in self.obj_table:
            in_header[symbol] = TABLE_OFFSET + len(table_str)
            table_str += ":\"{}\",".format(symbol)
        self.stream.add_header(PROXY_HEADER.format(table_str[:-1]))
        for symbol, index in in_header.items():
            self.stream.add_symbol(symbol, index)



    