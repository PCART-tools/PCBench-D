    def __init__(self, scale, tfm, texname, vf):
        if not isinstance(texname, bytes):
            raise ValueError("texname must be a bytestring, got %s"
                             % type(texname))
        self._scale = scale
        self._tfm = tfm
        self.texname = texname
        self._vf = vf
        self.size = scale * (72.0 / (72.27 * 2**16))
        try:
            nchars = max(tfm.width) + 1
        except ValueError:
            nchars = 0
        self.widths = [(1000*tfm.width.get(char, 0)) >> 20
                       for char in range(nchars)]
