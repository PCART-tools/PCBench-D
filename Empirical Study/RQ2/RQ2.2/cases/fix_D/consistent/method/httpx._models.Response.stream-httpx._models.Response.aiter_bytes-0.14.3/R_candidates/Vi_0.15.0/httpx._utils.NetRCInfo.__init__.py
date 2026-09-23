    def __init__(self, files: typing.Optional[typing.List[str]] = None) -> None:
        if files is None:
            files = [os.getenv("NETRC", ""), "~/.netrc", "~/_netrc"]
        self.netrc_files = files
