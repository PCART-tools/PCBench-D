def _conv_type_shape(im):
    typ, extra = _MODE_CONV[im.mode]
    if extra is None:
        return (im.size[1], im.size[0]), typ
    else:
        return (im.size[1], im.size[0], extra), typ
