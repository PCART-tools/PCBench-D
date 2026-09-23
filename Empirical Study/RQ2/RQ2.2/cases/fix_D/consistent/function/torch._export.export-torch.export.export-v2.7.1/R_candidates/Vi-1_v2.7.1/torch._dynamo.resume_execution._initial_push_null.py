def _initial_push_null(insts):
    if sys.version_info >= (3, 11):
        insts.append(create_instruction("PUSH_NULL"))
        if sys.version_info < (3, 13):
            insts.append(create_instruction("SWAP", arg=2))
