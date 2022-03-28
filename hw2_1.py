

""" Grammar G1 """

"""
E -> E+T | T 
T -> T*F | F
F -> *F | B
B -> id | B.id | (F)


First(E) = {'*', '(', 'id'}
First(T) = First(F) = {'*', '(', 'id'}
First(F) = {'*'} U First(B) = {'*', '(', 'id'} 
First(B) = {'id', '('}

if its a star I know its B, otherwise I have no idea

remove left recursion

E  -> TE'
E' -> +TE' | e
T  -> FT'
T' -> *FT' | e
F  -> *F | B
B  -> idB' | (F)B'
B' -> .idB' | e

Now first looks better (hopefully)
First(E) = {'*', 'id', '('}
First(E') = {'+'}
First(T) = {'*', 'id', '('}
First(T') = {'*'}
First(F) = {'*', 'id', '('}
First(B) = {'id', '('}
First(B') = {'.'}

still terrible! (but better?)

In implementation we can deal with most left recursion by iteration, instead of factoring it out
"""

from common import *

PLUS = '+'
STAR = '*'
ID = 'id'
DOT = '.'
LPAREN = "("
RPAREN = ")"


# done by iteration
def E(t: TokenStream, lnode=None):
    if lnode == None:
        lnode = Node("E").add_child(T(t))
    while t.cur() == PLUS:
        newNode = Node("E")
        newNode.add_child(lnode)
        newNode.add_child(match(t, PLUS))
        newNode.add_child(T(t))
        lnode = newNode
    return lnode

# done by iteration
def T(t: TokenStream, lnode=None):
    if lnode == None:
        lnode = F(t)
    while t.cur() == STAR:
        newNode = Node("T")
        newNode.add_child(lnode)
        newNode.add_child(match(t, STAR))
        newNode.add_child(F(t))
        lnode = newNode
    return Node("T").add_child(lnode)

def F(t: TokenStream):
    result = Node("F")
    if t.cur() == STAR:
        result.add_child(match(t, STAR))
        result.add_child(F(t))
    elif t.cur() in [ID, LPAREN]:
        result.add_child(B(t))
    else:
        error(t, "Expected '*', 'id' or '(' before ")
    return result


# factor B into B, B'
# B  -> idB' | (F)B'
# B' -> .idB' | e
def B(t: TokenStream):
    result = Node("B")
    if t.cur() == ID:
        result.add_child(match(t, ID))
        result.add_child(BPrime(t))
    elif t.cur() == LPAREN:
        result.add_child(match(t, LPAREN))
        result.add_child(F(t))
        result.add_child(match(t, RPAREN))
        result.add_child(BPrime(t))
    else:
        error(t, "Expected , 'id' or '(' before ")
    return result

# this one was able to be done iteratively
def BPrime(t: TokenStream):
    result = Node("B'")
    rnode = result
    while t.cur() == DOT:
        rnode.add_child(match(t, DOT))
        rnode.add_child(match(t, ID))
        new_rnode = Node("B'")
        rnode.add_child(new_rnode)
        rnode = new_rnode
    return result

"""
E -> E+T | T 
T -> T*F | F
F -> *F | B
B -> id | B.id | (F)
"""

def main():
    test = " id * id * id * id "
    print(test)
    t = TokenStream(test)
    print(E(t))


if __name__ == "__main__":
    main()
