from . import regex

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
NUMBER_ADDS = "0123456789"
ALPHA_SIZE = len(ALPHABET)
FULL_ALPHA_SIZE = ALPHA_SIZE + len(NUMBER_ADDS)

def calc_huffman_pholder(list_len, k):
    mod = list_len % (k - 1)
    if mod == 0:
        return 1
    elif mod == 1:
        return 0
    else:
        return k - mod

class ScopedHuffmanBranch(object):
    def __init__(self, node_list):
        self.table = {}
        self.num_occ = 0
        for i, char in enumerate(ALPHABET):
            if i >= len(node_list):
                break
            self.table[char] = node_list[i]
            self.num_occ += node_list[i].num_occ

class ScopedHuffmanNode(object):
    def __init__(self, symbol, num_occ):
        self.symbol = symbol
        self.num_occ = num_occ

class ScopedHuffmanPlaceholder(object):
    def __init__(self):
        self.num_occ = 0

class ScopedHuffman(object):
    def __init__(self):
        self.freq_list = {}
        self.tree = {}
    
    def record_symbol(self, symbol, num = 1):
        if symbol in self.freq_list.keys():
            self.freq_list[symbol] += num
        else:
            self.freq_list[symbol] = num

    def build(self):
        sorted_freq = sorted([ScopedHuffmanNode(symbol, num_occ) for symbol, num_occ in self.freq_list.items()],
                             key = lambda x: x.num_occ)
        sorted_freq = ([ScopedHuffmanPlaceholder()] * calc_huffman_pholder(len(sorted_freq), ALPHA_SIZE)) + sorted_freq
        while len(sorted_freq) > 1:
            first_26, sorted_freq = sorted_freq[:ALPHA_SIZE], sorted_freq[ALPHA_SIZE:]
            new_branch = ScopedHuffmanBranch(first_26)
            sorted_freq.append(new_branch)
            sorted_freq = sorted(sorted_freq, key=lambda x: x.num_occ)

        if not isinstance(sorted_freq[0], ScopedHuffmanBranch):
            sorted_freq[0] = ScopedHuffmanBranch([sorted_freq[0]])

        def recurse_flatten(branch, prefix):
            for code, elm in branch.table.items():
                new_prefix = prefix + code
                if isinstance(elm, ScopedHuffmanNode):
                    self.tree[elm.symbol] = new_prefix
                elif isinstance(elm, ScopedHuffmanBranch):
                    recurse_flatten(elm, new_prefix)

        recurse_flatten(sorted_freq[0], "")

    def get_code_from_symbol(self, symbol):
        return self.tree[symbol]