    @classmethod
    def parse_file(cls, path: Union[str, Path], *,
                   content_type: str=None,
                   encoding: str='utf8',
                   proto: Protocol=None,
                   allow_pickle: bool=False):
        obj = load_file(path, proto=proto, content_type=content_type, encoding=encoding, allow_pickle=allow_pickle)
        return cls.parse_obj(obj)
