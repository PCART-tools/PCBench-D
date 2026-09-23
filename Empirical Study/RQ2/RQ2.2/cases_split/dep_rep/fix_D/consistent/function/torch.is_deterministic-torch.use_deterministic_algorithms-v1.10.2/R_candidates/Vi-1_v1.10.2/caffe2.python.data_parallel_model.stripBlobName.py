def stripBlobName(param):
    # Format is "a/b/c/d" -> "b/c/d"
    if isinstance(param, core.GradientSlice):
        return stripBlobName(param.indices) + ":" + stripBlobName(param.values)
    else:
        name = str(param)
    return name[name.index(scope._NAMESCOPE_SEPARATOR) + 1:]
