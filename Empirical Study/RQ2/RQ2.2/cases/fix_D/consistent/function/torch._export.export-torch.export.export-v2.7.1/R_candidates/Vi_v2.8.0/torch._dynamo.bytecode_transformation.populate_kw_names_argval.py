def populate_kw_names_argval(instructions, consts):
    for inst in instructions:
        if inst.opname == "KW_NAMES":
            inst.argval = consts[inst.arg]
