    def _repr_png_(self):
        """Generate a PNG representation of the BivarColormap."""
        if not self._isinit:
            self._init()
        pixels = self.lut
        if pixels.shape[0] < _BIVAR_REPR_PNG_SIZE:
            pixels = np.repeat(pixels,
                               repeats=_BIVAR_REPR_PNG_SIZE//pixels.shape[0],
                               axis=0)[:256, :]
        if pixels.shape[1] < _BIVAR_REPR_PNG_SIZE:
            pixels = np.repeat(pixels,
                               repeats=_BIVAR_REPR_PNG_SIZE//pixels.shape[1],
                               axis=1)[:, :256]
        pixels = (pixels[::-1, :, :] * 255).astype(np.uint8)
        png_bytes = io.BytesIO()
        title = self.name + ' BivarColormap'
        author = f'Matplotlib v{mpl.__version__}, https://matplotlib.org'
        pnginfo = PngInfo()
        pnginfo.add_text('Title', title)
        pnginfo.add_text('Description', title)
        pnginfo.add_text('Author', author)
        pnginfo.add_text('Software', author)
        Image.fromarray(pixels).save(png_bytes, format='png', pnginfo=pnginfo)
        return png_bytes.getvalue()
