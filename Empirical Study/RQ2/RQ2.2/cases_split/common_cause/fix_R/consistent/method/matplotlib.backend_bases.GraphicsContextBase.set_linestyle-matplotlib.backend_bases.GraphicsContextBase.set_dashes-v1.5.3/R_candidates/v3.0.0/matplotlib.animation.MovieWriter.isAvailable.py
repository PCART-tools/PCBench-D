    @classmethod
    def isAvailable(cls):
        '''
        Check to see if a MovieWriter subclass is actually available.
        '''
        return shutil.which(cls.bin_path()) is not None
