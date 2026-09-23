def _reduce(binop, sequence, initial=no_default):
    if initial is not no_default:
        return reduce(binop, sequence, initial)
    else:
        return reduce(binop, sequence)
