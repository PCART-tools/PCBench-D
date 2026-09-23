def shapelist(a):
    """ Get the shape of nested list """
    if type(a) is list:
        return tuple([len(a)] + list(shapelist(a[0])))
    else:
        return ()
