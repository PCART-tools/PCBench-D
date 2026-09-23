    def __init__(self, prefix, directory, *, name=None,
                 expect_handler=None, chunk_size=256*1024,
                 response_factory=StreamResponse,
                 show_index=False, follow_symlinks=False):
        super().__init__(prefix, name=name)
        try:
            directory = Path(directory)
            if str(directory).startswith('~'):
                directory = Path(os.path.expanduser(str(directory)))
            directory = directory.resolve()
            if not directory.is_dir():
                raise ValueError('Not a directory')
        except (FileNotFoundError, ValueError) as error:
            raise ValueError(
                "No directory exists at '{}'".format(directory)) from error
        self._directory = directory
        self._file_sender = FileSender(resp_factory=response_factory,
                                       chunk_size=chunk_size)
        self._show_index = show_index
        self._follow_symlinks = follow_symlinks
        self._expect_handler = expect_handler

        self._routes = {'GET': ResourceRoute('GET', self._handle, self,
                                             expect_handler=expect_handler),

                        'HEAD': ResourceRoute('HEAD', self._handle, self,
                                              expect_handler=expect_handler)}
