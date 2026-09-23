    @classmethod
    def get_default_filetype(cls):
        """
        Get the default savefig file format as specified in rcParam
        ``savefig.format``. Returned string excludes period. Overridden
        in backends that only support a single file type.
        """
        return rcParams['savefig.format']
