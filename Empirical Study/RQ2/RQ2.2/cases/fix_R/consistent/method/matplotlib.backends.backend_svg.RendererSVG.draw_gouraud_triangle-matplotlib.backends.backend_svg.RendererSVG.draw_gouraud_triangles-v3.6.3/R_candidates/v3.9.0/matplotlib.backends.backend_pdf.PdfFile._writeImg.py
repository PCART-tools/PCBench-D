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
               'ColorSpace': Name({1: 'DeviceGray', 3: 'DeviceRGB'}[color_channels]),
               'BitsPerComponent': 8}
        if smask:
            obj['SMask'] = smask
        if mpl.rcParams['pdf.compression']:
            if data.shape[-1] == 1:
                data = data.squeeze(axis=-1)
            png = {'Predictor': 10, 'Colors': color_channels, 'Columns': width}
            img = Image.fromarray(data)
            img_colors = img.getcolors(maxcolors=256)
            if color_channels == 3 and img_colors is not None:
                # Convert to indexed color if there are 256 colors or fewer. This can
                # significantly reduce the file size.
                num_colors = len(img_colors)
                palette = np.array([comp for _, color in img_colors for comp in color],
                                   dtype=np.uint8)
                palette24 = ((palette[0::3].astype(np.uint32) << 16) |
                             (palette[1::3].astype(np.uint32) << 8) |
                             palette[2::3])
                rgb24 = ((data[:, :, 0].astype(np.uint32) << 16) |
                         (data[:, :, 1].astype(np.uint32) << 8) |
                         data[:, :, 2])
                indices = np.argsort(palette24).astype(np.uint8)
                rgb8 = indices[np.searchsorted(palette24, rgb24, sorter=indices)]
                img = Image.fromarray(rgb8, mode='P')
                img.putpalette(palette)
                png_data, bit_depth, palette = self._writePng(img)
                if bit_depth is None or palette is None:
                    raise RuntimeError("invalid PNG header")
                palette = palette[:num_colors * 3]  # Trim padding; remove for Pillow>=9
                obj['ColorSpace'] = [Name('Indexed'), Name('DeviceRGB'),
                                     num_colors - 1, palette]
                obj['BitsPerComponent'] = bit_depth
                png['Colors'] = 1
                png['BitsPerComponent'] = bit_depth
            else:
                png_data, _, _ = self._writePng(img)
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
