def eval(expression, _dict={}, **kw):
    """
    Evaluates an image expression.

    :param expression: A string containing a Python-style expression.
    :param options: Values to add to the evaluation context.  You
                    can either use a dictionary, or one or more keyword
                    arguments.
    :return: The evaluated expression. This is usually an image object, but can
             also be an integer, a floating point value, or a pixel tuple,
             depending on the expression.
    """

    # build execution namespace
    args = ops.copy()
    args.update(_dict)
    args.update(kw)
    for k, v in list(args.items()):
        if hasattr(v, "im"):
            args[k] = _Operand(v)

    code = compile(expression, "<string>", "eval")
    for name in code.co_names:
        if name not in args and name != "abs":
            raise ValueError(f"'{name}' not allowed")

    out = builtins.eval(expression, {"__builtins": {"abs": abs}}, args)
    try:
        return out.im
    except AttributeError:
        return out
