
class Node:
    def __init__(self, name: str):
        self.name = name
        self.children: list = []

    def add_child(self, child):
        self.children.append(child)
        return self

    def __str__(self) -> str:
        return self.stringify(0)

    def stringify(self, indent):
        s = '   '*indent + self.name + " =>"
        for child in self.children:
            s += '\n'
            s += child.stringify(indent + 1)
        return s + '\n'

class TokenStream:
    def __init__(self, string: str):
        self.tokens = string.split() + ['$']
        self.index = 0

    def cur(self):
        if self.index >= len(self.tokens):
            raise Exception("end of token stream")
        return self.tokens[self.index]

    def has_next(self):
        return self.index < len(self.tokens)

    def next(self):
        self.index += 1

def match(t: TokenStream, token: str):
    if t.cur() == token:
        t.next()
        return Node(token)
    else:
        error(t, f"Expected token {token} before ")
        return Node("ERROR")

def error(t: TokenStream, s: str):
    print(f"ERROR: {s} {t.cur()}")

def verify(t: TokenStream, s: str):
    if t.cur() != s:
        error(t, "expected " + s)

