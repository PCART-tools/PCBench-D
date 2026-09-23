    def __init__(
        self,
        fp: StrOrBytesPath | IO[bytes],
        filename: str | bytes | None = None,
    ) -> None:
        self.tag_v2: ImageFileDirectory_v2
        """ Image file directory (tag dictionary) """

        self.tag: ImageFileDirectory_v1
        """ Legacy tag entries """

        super().__init__(fp, filename)
