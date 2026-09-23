def gen_classes(ops, op_list):
    f = ""
    for op in op_list:
        f += gen_class(op, ops[op])
    return f
