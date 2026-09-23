    def _writeImg(self, data, height, width, grayscale, id, smask=None):
        """
        Write the image *data* of size *height* x *width*, as grayscale
        if *grayscale* is true and RGB otherwise, as pdf object *id*
        and with the soft mask (alpha channel) *smask*, which should be
        either None or a *height* x *width* x 1 array.
        """

        obj = {'Type':             Name('XObject'),
               'Subtype':          Name('Image'),
               'Width':            width,
               'Height':           height,
               'ColorSpace':       Name('DeviceGray' if grayscale
                                        else 'DeviceRGB'),
               'BitsPerComponent': 8}
        if smask:
            obj['SMask'] = smask
        if rcParams['pdf.compression']:
            png = {'Predictor': 10,
                   'Colors':    1 if grayscale else 3,
                   'Columns':   width}
        else:
            png = None
        self.beginStream(
            id,
            self.reserveObject('length of image stream'),
            obj,
            png=png
            )
        if png:
            self._writePng(data)
        else:
            self.currentstream.write(data.tostring())
        self.endStream()
