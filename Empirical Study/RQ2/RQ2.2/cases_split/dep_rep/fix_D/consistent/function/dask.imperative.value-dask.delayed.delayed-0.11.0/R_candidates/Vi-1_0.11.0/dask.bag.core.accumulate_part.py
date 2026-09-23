def accumulate_part(binop, seq, initial, is_first=False):
    if initial == no_default:
        res = list(accumulate(binop, seq))
    else:
        res = list(accumulate(binop, seq, initial=initial))
    if is_first:
        return res, res[-1] if res else [], initial
    return res[1:], res[-1]
