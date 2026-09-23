def safe_append_to_index(index, key):
    """ a safe append to an index, if incorrect type, then catch and recreate
    """
    try:
        return index.insert(len(index), key)
    except:

        # raise here as this is basically an unsafe operation and we want
        # it to be obvious that you are doing something wrong
        raise ValueError("unsafe appending to index of type {0} with a key "
                         "{1}".format(index.__class__.__name__, key))
