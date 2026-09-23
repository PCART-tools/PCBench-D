def _floatconv(x):
    try:
        return float(x)  # The fastest path.
    except ValueError:
        if '0x' in x:  # Don't accidentally convert "a" ("0xa") to 10.
            try:
                return float.fromhex(x)
            except ValueError:
                pass
        raise  # Raise the original exception, which makes more sense.
