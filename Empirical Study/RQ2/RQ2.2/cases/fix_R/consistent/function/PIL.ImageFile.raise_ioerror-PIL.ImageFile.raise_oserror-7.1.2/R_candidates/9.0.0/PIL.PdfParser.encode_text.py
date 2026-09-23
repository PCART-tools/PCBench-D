def encode_text(s):
    return codecs.BOM_UTF16_BE + s.encode("utf_16_be")
