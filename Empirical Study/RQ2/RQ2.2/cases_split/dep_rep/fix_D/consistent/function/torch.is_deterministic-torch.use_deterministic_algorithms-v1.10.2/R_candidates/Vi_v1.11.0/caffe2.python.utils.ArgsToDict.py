def ArgsToDict(args):
    """
    Convert a list of arguments to a name, value dictionary. Assumes that
    each argument has a name. Otherwise, the argument is skipped.
    """
    ans = {}
    for arg in args:
        if not arg.HasField("name"):
            continue
        for d in arg.DESCRIPTOR.fields:
            if d.name == "name":
                continue
            if d.label == d.LABEL_OPTIONAL and arg.HasField(d.name):
                ans[arg.name] = getattr(arg, d.name)
                break
            elif d.label == d.LABEL_REPEATED:
                list_ = getattr(arg, d.name)
                if len(list_) > 0:
                    ans[arg.name] = list_
                    break
        else:
            ans[arg.name] = None
    return ans
