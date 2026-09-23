def basichandlers(extension, data):

    if extension in "txt text transcript":
        return data.decode("utf-8")

    if extension in "cls cls2 class count index inx id".split():
        try:
            return int(data)
        except ValueError:
            return None

    if extension in "json jsn":
        return json.loads(data)

    if extension in "pyd pickle".split():
        return pickle.loads(data)

    if extension in "pt".split():
        stream = io.BytesIO(data)
        return torch.load(stream)

    # if extension in "ten tb".split():
    #     from . import tenbin
    #     return tenbin.decode_buffer(data)

    # if extension in "mp msgpack msg".split():
    #     import msgpack
    #     return msgpack.unpackb(data)

    return None
