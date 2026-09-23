def GetArgumentByName(net_def, arg_name):
    for arg in net_def.arg:
        if arg.name == arg_name:
            return arg
    return None
