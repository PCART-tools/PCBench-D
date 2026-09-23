    @classmethod
    def isAvailable(cls):
        '''
        Check to see if a ImageMagickWriter is actually available.

        Done by first checking the windows registry (if applicable) and then
        running the commandline tool.
        '''
        bin_path = cls.bin_path()
        if bin_path == "convert":
            cls._init_from_registry()
        return super(ImageMagickBase, cls).isAvailable()
