def normalize_not_implemented(arg, parm):
    if arg != parm.default:
        raise NotImplementedError(f"'{parm.name}' parameter is not supported.")
