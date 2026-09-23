class fake_stderr(object):
    """
    Wx does strange things with stderr, as it makes the assumption that
    there is probably no console. This redirects stderr to the console, since
    we know that there is one!
    """

    def write(self, msg):
        print("Stderr: %s\n\r" % msg)
