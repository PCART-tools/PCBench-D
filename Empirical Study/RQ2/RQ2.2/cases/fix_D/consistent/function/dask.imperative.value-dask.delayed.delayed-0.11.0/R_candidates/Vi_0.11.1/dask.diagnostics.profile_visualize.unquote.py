def unquote(expr):
    if istask(expr):
        if expr[0] in (tuple, list, set):
            return expr[0](map(unquote, expr[1]))
        elif (expr[0] == dict and
              isinstance(expr[1], list) and
              isinstance(expr[1][0], list)):
            return dict(map(unquote, expr[1]))
    return expr
