def supports(o, factory_methods):
    # Ignore all families (!) of functions that have TensorOptions (i.e. tensor factory methods).
    if o['name'] in factory_methods:
        if factory_methods[o['name']] == 0:
            print("Skipping {} because it is a factory method".format(o['name']))
        factory_methods[o['name']] += 1
        return False

    # skip all in-place operators for now since aten cannot Resize
    # caffe2 memory inside an operator
    if o['inplace']:
        return False

    # _out variants also work in-place on arguments taken as destinations
    # we also cannot handle these because aten cannot resize caffe2 Tensors
    if "_out" in o['name']:
        return False

    # skip if no return, previously it is 'void'
    if len(o['returns']) == 0:
        return False

    # skip return types we cannot handle
    for ret in o['returns']:
        if not value_has_tensors(ret) and ret['type'] not in RETURN_MAP:
            print("Skipping {} Because of Ret: {} ({})".format(
                  o['name'], ret['type'], ret['dynamic_type']))
            return False

    # skip arguments we cannot handle
    for arg in o['arguments']:
        if not value_has_tensors(arg) and arg['type'] not in ARGUMENT_MAP:
            print("Skipping {} Because of Arg: {} ({}) ".format(
                  o['name'], arg['type'], arg['dynamic_type']))
            return False
    return True
