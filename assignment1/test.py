AND = 'AND'; OR = "OR"; NOT = "NOT"
L_BKT = '('; R_BKT = ')'; QUOTE = '"'

# TEST CASE:
# get_operands('dictionary love')
# get_operands('(NOT harry_potter) azkaban')
# get_operands('(AND (NOT dictionary) (NOT love)) (AND harrypotter azkaban)')
def get_operands(opds):
    operands = []
    if opds[0] == L_BKT:
        n_lbkt = 0
        for i in range(len(opds)):
            if opds[i] == L_BKT:
                if n_lbkt == 0: start_i = i
                n_lbkt += 1
            elif opds[i] == R_BKT:
                n_lbkt -= 1
                if n_lbkt == 0: operands.append(opds[start_i:i+1])
        # check unbalanced bracket
        assert(n_lbkt == 0)
    else:
        operands = opds.split()
    return operands

# ['dictionary', 'love']
print(get_operands('dictionary love'))

# ['(NOT harry_potter)', 'azkaban']
print(get_operands('(NOT harry_potter) azkaban'))

# ['(AND (NOT dictionary) (NOT love))', '(AND harrypotter azkaban)']
print(get_operands('(AND (NOT dictionary) (NOT love)) (AND harrypotter azkaban)'))
