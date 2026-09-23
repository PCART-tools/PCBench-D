def _accept(prefix):
    return prefix[0:4] == b"GRIB" and prefix[7] == 1
