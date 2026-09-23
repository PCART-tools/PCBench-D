def parse_lines(lines):
    # States
    EMPTY = 0
    OP = 1
    MACRO = 2
    parse_state = EMPTY

    # Preprocess the macros
    curr_macro = ""
    macros = {}

    index = 0
    while index < len(lines):
        line = lines[index]
        if line.lower().startswith("macro"):
            assert parse_state == EMPTY
            macro_line = line.split(" ")
            # Support macros that look like attributes
            # e.g. macro - CONV_LIKE
            curr_macro = " ".join(macro_line[1:])
            assert curr_macro not in macros, 'Macro "{}" defined twice.'.format(
                curr_macro
            )
            macros[curr_macro] = []
            parse_state = MACRO
            lines = lines[:index] + lines[index + 1 :]
            continue
        elif line.lower().startswith("endmacro"):
            assert parse_state == MACRO
            parse_state = EMPTY
            lines = lines[:index] + lines[index + 1 :]
            continue
        elif parse_state == MACRO:
            macros[curr_macro].append(line)
            lines = lines[:index] + lines[index + 1 :]
            continue
        index += 1

    index = 0
    while index < len(lines):
        line = lines[index]
        if line in macros:
            lines = lines[:index] + macros[line] + lines[index + 1 :]
            index += len(macros[line]) - 1
        index += 1

    # Now parse the file
    curr_op = ""
    # dict of the form
    #  opName : { attributes: [], ... }
    ops = {}
    # To preserve parsing order for dependencies (for things like init_from)
    op_list = []

    for line in lines:
        if not len(line):
            continue
        if line[0] == "-":
            assert parse_state is OP
            attr = [_.strip() for _ in line[1:].split(":")]
            assert attr[0][0].isupper()
            if len(attr) == 2:  # attribute : type
                ops[curr_op]["attributes"].append((attr[0], attr[1]))
            elif len(attr) == 3:  # attribute : type
                ops[curr_op]["attributes"].append((attr[0], attr[1], attr[2]))
        else:
            op = [l.strip() for l in line.split(":")]
            assert len(op[0].split(" ")) == 1
            parse_state = OP
            curr_op = op[0]
            assert curr_op not in ops
            ops[curr_op] = {}
            op_list.append(curr_op)
            if len(op) > 1:
                ops[curr_op]["init_from"] = [op[1]]
            ops[curr_op]["attributes"] = []
    return ops, op_list
