    def __init__(self, fps=5, metadata=None, codec=None, bitrate=None):
        self.fps = fps
        self.metadata = metadata if metadata is not None else {}
        self.codec = (
            mpl.rcParams['animation.codec'] if codec is None else codec)
        self.bitrate = (
            mpl.rcParams['animation.bitrate'] if bitrate is None else bitrate)
