def AddArgument(op, key, value):
    """Makes an argument based on the value type."""
    op.arg.extend([utils.MakeArgument(key, value)])
