    @classmethod
    def bin_path(cls):
        '''
        Returns the binary path to the commandline tool used by a specific
        subclass. This is a class method so that the tool can be looked for
        before making a particular MovieWriter subclass available.
        '''
        return str(rcParams[cls.exec_key])
