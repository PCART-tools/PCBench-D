class HTTPFileSystem(core.FileSystem):
    """
    Simple File-System for fetching data via HTTP(S)

    Unlike other file-systems, HTTP is limited in that it does not provide glob
    or write capability.
    """
    sep = '/'

    def __init__(self, **storage_options):
        """
        Parameters
        ----------
        storage_options: key-value
            May be credentials, e.g., `{'auth': ('username', 'pword')}` or any
            other parameters for requests
        """
        self.block_size = storage_options.pop('block_size', DEFAULT_BLOCK_SIZE)
        self.kwargs = storage_options
        self.session = requests.Session()

    def glob(self, url):
        """For a template path, return matching files"""
        raise NotImplementedError

    def mkdirs(self, url):
        """Make any intermediate directories to make path writable"""
        raise NotImplementedError

    def open(self, url, mode='rb', block_size=None, **kwargs):
        """Make a file-like object

        Parameters
        ----------
        url: str
            Full URL with protocol
        mode: string
            must be "rb"
        kwargs: key-value
            Any other parameters, passed to requests calls
        """
        if mode != 'rb':
            raise NotImplementedError
        block_size = block_size if block_size is not None else self.block_size
        return HTTPFile(url, self.session, block_size, **self.kwargs)

    def ukey(self, url):
        """Unique identifier, implied file might have changed every time"""
        return uuid.uuid1().hex

    def size(self, url):
        """Size in bytes of the file at path"""
        return file_size(url, session=self.session, **self.kwargs)
