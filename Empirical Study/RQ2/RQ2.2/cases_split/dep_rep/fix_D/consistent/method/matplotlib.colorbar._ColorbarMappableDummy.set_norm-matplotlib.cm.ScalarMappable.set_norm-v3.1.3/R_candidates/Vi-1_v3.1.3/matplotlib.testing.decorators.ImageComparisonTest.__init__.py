    def __init__(self, baseline_images, extensions, tol,
                 freetype_version, remove_text, savefig_kwargs, style):
        _ImageComparisonBase.__init__(self, tol, remove_text, savefig_kwargs)
        self.baseline_images = baseline_images
        self.extensions = extensions
        self.freetype_version = freetype_version
        self.style = style
