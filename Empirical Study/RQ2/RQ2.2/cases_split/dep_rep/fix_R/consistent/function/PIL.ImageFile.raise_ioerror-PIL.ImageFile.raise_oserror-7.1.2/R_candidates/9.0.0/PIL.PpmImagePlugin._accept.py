def _accept(prefix):
    return prefix[0:1] == b"P" and prefix[1] in b"0456y"
