def _AdjustDims(op_def, arg_map, pads, dim1, dim2):
    n1, c1, h1, w1 = dim1
    n2, c2, h2, w2 = dim2
    assert(n1 == n2)
    assert(c1 == c2)
    is_pad = 'pad' in arg_map
    if h1 != h2 or w1 != w2:
        if h1 == h2 + 1:
            pads['pad_b'] += 1
        elif h1 != h2:
            raise Exception("Unexpected dimensions for height:", h1, h2)
        if w1 == w2 + 1:
            pads['pad_r'] += 1
        elif w1 != w2:
            raise Exception("Unexpected dimensions for width:", w1, w2)
        if is_pad:
            op_def.arg.remove(arg_map['pad'])
            args = []
            for name in pads.keys():
                arg = caffe2_pb2.Argument()
                arg.name = name
                arg.i = pads[name]
                args.append(arg)
            op_def.arg.extend(args)
        else:
            for name in pads.keys():
                arg_map[name].i = pads[name]
