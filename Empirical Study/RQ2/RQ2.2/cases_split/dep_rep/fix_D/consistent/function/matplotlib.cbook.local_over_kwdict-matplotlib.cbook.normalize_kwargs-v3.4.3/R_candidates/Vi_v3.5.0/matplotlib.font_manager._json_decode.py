def _json_decode(o):
    cls = o.pop('__class__', None)
    if cls is None:
        return o
    elif cls == 'FontManager':
        r = FontManager.__new__(FontManager)
        r.__dict__.update(o)
        return r
    elif cls == 'FontEntry':
        r = FontEntry.__new__(FontEntry)
        r.__dict__.update(o)
        if not os.path.isabs(r.fname):
            r.fname = os.path.join(mpl.get_data_path(), r.fname)
        return r
    else:
        raise ValueError("Don't know how to deserialize __class__=%s" % cls)
