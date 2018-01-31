AND = 'AND'; OR = "OR"; NOT = "NOT"
L_BKT = '('; R_BKT = ')'; QUOTE = '"'

def get_operands(opds):
    operands = []
    n_lbkt = 0; in_opd = False
    opds = opds.strip()
    for i in range(len(opds)):
        if opds[i] == L_BKT:
            if n_lbkt == 0: start_i = i
            n_lbkt += 1
        elif opds[i] == R_BKT:
            n_lbkt -= 1
            if n_lbkt == 0: operands.append(opds[start_i:i+1])
        elif not in_opd and n_lbkt == 0 and opds[i] != ' ':
            start_i = i
            in_opd = True
        elif in_opd and n_lbkt == 0 and opds[i] == ' ':
            operands.append(opds[start_i:i])
            in_opd = False

    if in_opd:
        operands.append(opds[start_i:])
    # check unbalanced bracket
    assert(n_lbkt == 0)
    return operands

# TEST CASE:
print(get_operands('dictionary love'))                                              # ['dictionary', 'love']
print(get_operands('(NOT harry_potter) azkaban'))                                   # ['(NOT harry_potter)', 'azkaban']
print(get_operands('azkaban (NOT harry_potter)'))                                   # ['azkaban', '(NOT harry_potter)']
print(get_operands('(AND (NOT dictionary) (NOT love)) (AND harrypotter azkaban)'))  # ['(AND (NOT dictionary) (NOT love))', '(AND harrypotter azkaban)']
