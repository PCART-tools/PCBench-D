    def _writeImg(self, data, id, smask=None):
        """
        Write the image *data*, of shape ``(height, width, 1)`` (grayscale) or
        ``(height, width, 3)`` (RGB), as pdf object *id* and with the soft mask
        (alpha channel) *smask*, which should be either None or a ``(height,
        width, 1)`` array.
        """
        height, width, color_channels = data.shape
        obj = {'Type': Name('XObject'),
               'Subtype': Name('Image'),
               'Width': width,
               'Height': height,
               'ColorSpace': Name({1: 'DeviceGray',
                                   3: 'DeviceRGB'}[color_channels]),
               'BitsPerComponent': 8}
        if smask:
            obj['SMask'] = smask
        if mpl.rcParams['pdf.compression']:
            if data.shape[-1] == 1:
                data = data.squeeze(axis=-1)
            img = Image.fromarray(data)
            img_colors = img.getcolors(maxcolors=256)
            if color_channels == 3 and img_colors is not None:
                # Convert to indexed color if there are 256 colors or fewer
                # This can significantly reduce the file size
                num_colors = len(img_colors)
                img = img.convert(mode='P', dither=Image.NONE,
                                  palette=Image.ADAPTIVE, colors=num_colors)
                png_data, bit_depth, palette = self._writePng(img)
                if bit_depth is None or palette is None:
                    raise RuntimeError("invalid PNG header")
                palette = palette[:num_colors * 3]  # Trim padding
                palette = pdfRepr(palette)
                obj['ColorSpace'] = Verbatim(b'[/Indexed /DeviceRGB '
                                             + str(num_colors - 1).encode()
                                             + b' ' + palette + b']')
                obj['BitsPerComponent'] = bit_depth
                color_channels = 1
            else:
                png_data, _, _ = self._writePng(img)
            png = {'Predictor': 10, 'Colors': color_channels, 'Columns': width}
        else:
            png = None
        self.beginStream(
            id,
            self.reserveObject('length of image stream'),
            obj,
            png=png
            )
        if png:
            self.currentstream.write(png_data)
        else:
            self.currentstream.write(data.tobytes())
        self.endStream()
