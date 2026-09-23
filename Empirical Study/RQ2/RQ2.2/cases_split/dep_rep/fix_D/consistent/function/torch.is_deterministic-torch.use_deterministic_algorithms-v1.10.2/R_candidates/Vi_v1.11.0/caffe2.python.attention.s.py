def s(scope, name):
    # We have to manually scope due to our internal/external blob
    # relationships.
    return "{}/{}".format(str(scope), str(name))
