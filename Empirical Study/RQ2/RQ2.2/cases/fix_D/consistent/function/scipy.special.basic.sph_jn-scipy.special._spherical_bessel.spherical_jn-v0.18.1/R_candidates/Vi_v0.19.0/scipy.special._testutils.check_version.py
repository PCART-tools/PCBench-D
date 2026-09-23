def check_version(module, min_ver):
    if type(module) == MissingModule:
        return dec.skipif(True, "{} is not installed".format(module.name))
    return dec.skipif(LooseVersion(module.__version__) < LooseVersion(min_ver),
                      "{} version >= {} required".format(module.__name__, min_ver))
