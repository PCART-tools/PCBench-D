    def __init__(self, formats=None, zero_formats=None, offset_formats=None,
                 show_offset=True):
        self._formats = formats
        self._zero_formats = zero_formats
        self._offset_formats = offset_formats
        self._show_offset = show_offset
        super().__init__()
