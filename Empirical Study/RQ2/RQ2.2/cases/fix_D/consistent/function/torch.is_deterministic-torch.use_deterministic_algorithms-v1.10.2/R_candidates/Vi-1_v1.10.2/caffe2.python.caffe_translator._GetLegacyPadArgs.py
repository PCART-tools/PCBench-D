def _GetLegacyPadArgs(op_def, arg_map):
    pads = {}
    keys = ['pad_l', 'pad_t', 'pad_r', 'pad_b']
    is_pad = 'pad' in arg_map
    if is_pad:
        for k in keys:
            pads[k] = arg_map['pad'].i
    else:
        pads = {x: arg_map[x].i for x in keys}
    return pads
