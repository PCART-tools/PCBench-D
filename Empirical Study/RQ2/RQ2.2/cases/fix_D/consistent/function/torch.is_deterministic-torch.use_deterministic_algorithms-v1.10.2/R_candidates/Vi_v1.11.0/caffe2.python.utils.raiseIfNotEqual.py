def raiseIfNotEqual(a, b, msg):
    if a != b:
        raise Exception("{}. {} != {}".format(msg, a, b))
