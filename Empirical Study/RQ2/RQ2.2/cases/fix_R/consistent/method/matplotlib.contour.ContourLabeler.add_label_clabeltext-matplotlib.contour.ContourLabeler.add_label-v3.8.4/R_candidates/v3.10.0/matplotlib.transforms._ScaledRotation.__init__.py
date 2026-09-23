    def __init__(self, theta, trans_shift):
        super().__init__()
        self._theta = theta
        self._trans_shift = trans_shift
        self._mtx = None
