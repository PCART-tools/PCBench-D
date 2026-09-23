    @classmethod
    def isAvailable(cls):
        '''
        Check to see if a MovieWriter subclass is actually available by
        running the commandline tool.
        '''
        bin_path = cls.bin_path()
        if not bin_path:
            return False
        try:
            p = subprocess.Popen(
                bin_path,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess_creation_flags)
            return cls._handle_subprocess(p)
        except OSError:
            return False
