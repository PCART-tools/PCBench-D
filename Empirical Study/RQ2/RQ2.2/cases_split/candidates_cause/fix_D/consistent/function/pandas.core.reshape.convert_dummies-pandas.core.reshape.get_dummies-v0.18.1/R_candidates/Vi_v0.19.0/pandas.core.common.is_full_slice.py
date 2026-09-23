def is_full_slice(obj, l):
    """ we have a full length slice """
    return (isinstance(obj, slice) and obj.start == 0 and obj.stop == l and
            obj.step is None)
