def i32be(c, o=0):
    return unpack_from(">I", c, o)[0]
