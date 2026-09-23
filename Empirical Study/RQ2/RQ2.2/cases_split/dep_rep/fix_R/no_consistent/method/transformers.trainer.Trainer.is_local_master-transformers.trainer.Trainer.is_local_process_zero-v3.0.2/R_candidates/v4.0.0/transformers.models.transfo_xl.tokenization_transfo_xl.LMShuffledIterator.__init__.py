    def __init__(self, data, bsz, bptt, device="cpu", ext_len=None, shuffle=False):
        """
        data -- list[LongTensor] -- there is no order among the LongTensors
        """
        self.data = data

        self.bsz = bsz
        self.bptt = bptt
        self.ext_len = ext_len if ext_len is not None else 0

        self.device = device
        self.shuffle = shuffle
