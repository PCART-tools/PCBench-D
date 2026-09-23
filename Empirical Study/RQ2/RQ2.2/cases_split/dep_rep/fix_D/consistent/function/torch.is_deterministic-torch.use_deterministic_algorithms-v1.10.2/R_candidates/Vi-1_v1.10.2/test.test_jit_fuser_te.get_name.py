def get_name(op):
    l = [op.name]
    if op.variant_test_name != '':
        l.append(op.variant_test_name)
    return '.'.join(l)
