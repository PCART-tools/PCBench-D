@_api.deprecated("3.3")
def DEBUG_MSG(string, lvl=3, o=None):
    if lvl >= _DEBUG:
        print(f"{_DEBUG_lvls[lvl]}- {string} in {type(o)}")
