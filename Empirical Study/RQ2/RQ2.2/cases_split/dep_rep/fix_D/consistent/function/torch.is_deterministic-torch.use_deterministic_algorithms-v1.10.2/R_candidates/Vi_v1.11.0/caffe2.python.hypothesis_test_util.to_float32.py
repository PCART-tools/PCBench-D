def to_float32(x):
    return struct.unpack("f", struct.pack("f", float(x)))[0]
