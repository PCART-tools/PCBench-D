    def setfd(self, fd):
        """
        Called from ImageFile to set the Python file-like object

        :param fd: A Python file-like object
        :returns: None
        """
        self.fd = fd
