    def _repr_png_(self):
        """Generate a PNG representation of the Colormap."""
        X = np.tile(np.linspace(0, 1, _REPR_PNG_SIZE[0]),
                                (_REPR_PNG_SIZE[1], 1))
        pixels = np.zeros((_REPR_PNG_SIZE[1]*len(self), _REPR_PNG_SIZE[0], 4),
                          dtype=np.uint8)
        for i, c in enumerate(self):
            pixels[i*_REPR_PNG_SIZE[1]:(i+1)*_REPR_PNG_SIZE[1], :] = c(X, bytes=True)
        png_bytes = io.BytesIO()
        title = self.name + ' multivariate colormap'
        author = f'Matplotlib v{mpl.__version__}, https://matplotlib.org'
        pnginfo = PngInfo()
        pnginfo.add_text('Title', title)
        pnginfo.add_text('Description', title)
        pnginfo.add_text('Author', author)
        pnginfo.add_text('Software', author)
        Image.fromarray(pixels).save(png_bytes, format='png', pnginfo=pnginfo)
        return png_bytes.getvalue()
