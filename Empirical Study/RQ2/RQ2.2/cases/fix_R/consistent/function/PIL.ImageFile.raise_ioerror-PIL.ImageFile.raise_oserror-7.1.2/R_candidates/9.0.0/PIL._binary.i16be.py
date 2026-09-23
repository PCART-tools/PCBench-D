def i16be(c, o=0):
    return unpack_from(">H", c, o)[0]
