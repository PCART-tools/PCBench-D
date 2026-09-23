def check_freetype_version(ver):
    if ver is None:
        return True

    if isinstance(ver, str):
        ver = (ver, ver)
    ver = [StrictVersion(x) for x in ver]
    found = StrictVersion(ft2font.__freetype_version__)

    return ver[0] <= found <= ver[1]
