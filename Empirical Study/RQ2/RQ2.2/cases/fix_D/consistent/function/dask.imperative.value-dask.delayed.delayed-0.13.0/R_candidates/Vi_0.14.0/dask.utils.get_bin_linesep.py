def get_bin_linesep(encoding, linesep):
    """
    Simply doing `linesep.encode(encoding)` does not always give you
    *just* the linesep bytes, for some encodings this prefix's the
    linesep bytes with the BOM. This function ensures we just get the
    linesep bytes.
    """
    if encoding == 'utf-16':
        return linesep.encode('utf-16')[2:]  # [2:] strips bom
    else:
        return linesep.encode(encoding)
