def has_blob(proto, needle):
    for op in proto.op:
        for inp in op.input:
            if inp == needle:
                return True
        for outp in op.output:
            if outp == needle:
                return True
    return False
