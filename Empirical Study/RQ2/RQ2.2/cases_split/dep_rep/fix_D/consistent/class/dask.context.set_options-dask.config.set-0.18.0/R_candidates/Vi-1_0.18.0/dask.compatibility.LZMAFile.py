class LZMAFile:
    def __init__(self, *args, **kwargs):
        raise ValueError("xz files requires the lzma module. "
                            "To use, install lzmaffi or backports.lzma.")
