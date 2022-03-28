
"""
F -> foreach var (L) | foreach var (R)
L -> L,I | I
I -> list | var
R -> var..var

First(F) = { foreach }
First(L) = {list, var}
First(I) = {list, var}
First(R) = { var }

L is left recursive, we can rewrite it like:

L  -> IL' | 
L' -> ,IL' | e

but it will be better to just write this rule iteratively
"""

from common import *

FOREACH = 'foreach'
VAR = 'var'
LIST = 'list'
RANGE = '..'
COMMA = ','
LPAREN = '('
RPAREN = ')'
END_OF_STREAM = '$'


def F(t: TokenStream):
    result = Node("F")
    result.add_child(match(t, FOREACH))
    result.add_child(match(t, VAR))
    result.add_child(match(t, LPAREN))
    if t.cur() == LIST:
        result.add_child(L(t))
    elif t.cur() == VAR:
        lnode = match(t, VAR)
        if t.cur() == RANGE:
            result.add_child(R(t, lnode=lnode))
        elif t.cur() == COMMA:
            result.add_child(L(t, lnode=lnode))
        else:
            error(t, "Expected 'range' or 'comma' before ")
    else:
        error(t, "Expected 'var' or 'list' before ")
    result.add_child(match(t, RPAREN))
    result.add_child(match(t, END_OF_STREAM))
    return result

# F -> foreach var (L) | foreach var (R)
# L -> L,I | I
# I -> list | var
# R -> var..var

def L(t: TokenStream, lnode=None):
    if lnode == None:
        lnode = I(t)
    while t.cur() == COMMA:
        new_node = Node("L")
        new_node.add_child(lnode)
        new_node.add_child(match(t, COMMA) )
        new_node.add_child(I(t))
        lnode = new_node
    result = Node("L")
    result.add_child(lnode)
    return result

def I(t: TokenStream, lnode=None):
    result = Node("I")
    if lnode == None:
        if t.cur() == LIST:
            result.add_child(match(t, LIST))
        elif t.cur() == VAR:
            result.add_child(match(t, VAR))
        else:
            error(t, "Expected 'LIST' or 'VAR' before ")
    else:
        result.add_child(lnode)
    return result

def R(t: TokenStream, lnode=None):
    result = Node("R")
    if lnode == None:
        if t.cur() == VAR:
            lnode = match(t, VAR)
        else:
            error(t, "Expected 'VAR' before ")
    result.add_child(lnode)
    result.add_child(match(t, RANGE))
    result.add_child(match(t, VAR))
    return result


"""
F -> foreach var (L) | foreach var (R)
L -> L,I | I
I -> list | var
R -> var..var
"""

def main():
    test = " foreach var ( var .. var ) "
    print(test)
    t = TokenStream(test)
    print(F(t))


if __name__ == "__main__":
    main()

