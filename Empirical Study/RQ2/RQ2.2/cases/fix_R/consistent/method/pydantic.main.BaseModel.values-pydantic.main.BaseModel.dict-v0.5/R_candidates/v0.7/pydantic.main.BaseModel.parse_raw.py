    @classmethod
    def parse_raw(cls, b: StrBytes, *,
                  content_type: str=None,
                  encoding: str='utf8',
                  proto: Protocol=None,
                  allow_pickle: bool=False):
        try:
            obj = load_str_bytes(b, proto=proto, content_type=content_type, encoding=encoding,
                                 allow_pickle=allow_pickle)
        except (ValueError, TypeError, UnicodeDecodeError) as e:
            raise ValidationError([Error(e, None, None)])
        return cls.parse_obj(obj)
