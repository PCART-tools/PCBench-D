def nonfunctional_tooslow(func):
    return dec.skipif(True, "    Test not yet functional (too slow), needs more work.")(func)
