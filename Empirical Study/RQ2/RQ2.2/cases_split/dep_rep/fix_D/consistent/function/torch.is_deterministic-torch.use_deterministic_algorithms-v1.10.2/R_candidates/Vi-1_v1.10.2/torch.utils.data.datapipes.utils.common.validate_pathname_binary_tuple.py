def validate_pathname_binary_tuple(data):
    if not isinstance(data, tuple):
        raise TypeError("pathname binary data should be tuple type, but got {}".format(type(data)))
    if len(data) != 2:
        raise TypeError("pathname binary tuple length should be 2, but got {}".format(str(len(data))))
    if not isinstance(data[0], str):
        raise TypeError("pathname binary tuple should have string type pathname, but got {}".format(type(data[0])))
    if not isinstance(data[1], BufferedIOBase):
        raise TypeError("pathname binary tuple should have BufferedIOBase based binary type, but got {}".format(type(data[1])))
