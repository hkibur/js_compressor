import re

# Match things like this document.cookie.split(";");
# Capturing anything after the first period and open parenthesis for the arguments
# It also captures whatever is inside the parens but it sorts it into either of two
# capture groups depending on whether it's quoted or not.
OBJECT_ATTRIBUTE_REGEX = re.compile(r'(?<=\.)([a-zA-Z_]\w*)')
DEFINED_VARIABLE_REGEX = re.compile(r'([^\w.])([a-zA-Z_]\w*)')
ANON_FUNC_REGEX = re.compile(r'function\((.*)\)')
NAMED_FUNC_REGEX = re.compile(r'function\s+([a-zA-Z_]\w*)\s*\((.*)\)')
FUNC_PARAMS_REGEX = re.compile(r'([a-zA-Z_]\w*)(\s*=\s*)?(?=[^(]*\)=>)')
KEYWORD_MATCH = re.compile(r'\W(?:await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|false|finally|for|function|if|implements|import|in|instanceof|interface|let|new|null|package|private|protected|public|return|super|switch|static|this|throw|try|True|typeof|var|void|while|with|yield)\W')
VAR_DEFINE_REGEX = re.compile(r'(var|let|const)\s+([a-zA-Z_]\w*)')

def is_keyword(string):
    return KEYWORD_MATCH.match(string) is not None

class MatchInfo(object):
    def __init__(self):
        self.offset = 0

    def set_match(self, match):
        self.start = match.start() + self.offset
        self.end = match.end() + self.offset
        self.matched = match.string[match.start():match.end()]
        self.len = len(self.matched)

    def apply_offset(self, offset):
        self.offset += offset
