def get_bom(fn, compression=None):
    """
    Get the Byte Order Mark (BOM) if it exists.
    """
    boms = set((codecs.BOM_UTF16, codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE))
    with open(fn, mode='rb', compression=compression) as f:
        f.seek(0)
        bom = f.read(2)
        f.seek(0)
    if bom in boms:
        return bom
    else:
        return b''
