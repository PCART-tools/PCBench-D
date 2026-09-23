    def __init__(self, mode, *args):
        self.im = None
        self.state = PyCodecState()
        self.fd = None
        self.mode = mode
        self.init(args)
