def read_mk(fobj, start_length, size):
    # Alpha masks seem to be uncompressed
    start = start_length[0]
    fobj.seek(start)
    pixel_size = (size[0] * size[2], size[1] * size[2])
    sizesq = pixel_size[0] * pixel_size[1]
    band = Image.frombuffer("L", pixel_size, fobj.read(sizesq), "raw", "L", 0, 1)
    return {"A": band}
