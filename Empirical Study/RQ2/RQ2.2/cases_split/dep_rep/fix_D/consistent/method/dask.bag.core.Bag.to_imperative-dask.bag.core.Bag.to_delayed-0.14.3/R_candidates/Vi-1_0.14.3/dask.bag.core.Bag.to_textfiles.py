    @wraps(to_textfiles)
    def to_textfiles(self, path, name_function=None, compression='infer',
                     encoding=system_encoding, compute=True, get=None):
        return to_textfiles(self, path, name_function, compression, encoding,
                            compute, get=get)
