def dump(filename):
    schemas = torch._C._jit_get_all_schemas()
    schemas += torch._C._jit_get_custom_class_schemas()
    with open(filename, 'w') as f:
        for s in schemas:
            f.write(str(s))
            f.write('\n')
