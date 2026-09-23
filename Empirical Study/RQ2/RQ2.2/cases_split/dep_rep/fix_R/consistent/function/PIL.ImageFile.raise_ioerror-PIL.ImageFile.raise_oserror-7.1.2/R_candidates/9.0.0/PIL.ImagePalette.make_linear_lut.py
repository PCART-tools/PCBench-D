def make_linear_lut(black, white):
    lut = []
    if black == 0:
        for i in range(256):
            lut.append(white * i // 255)
    else:
        raise NotImplementedError  # FIXME
    return lut
