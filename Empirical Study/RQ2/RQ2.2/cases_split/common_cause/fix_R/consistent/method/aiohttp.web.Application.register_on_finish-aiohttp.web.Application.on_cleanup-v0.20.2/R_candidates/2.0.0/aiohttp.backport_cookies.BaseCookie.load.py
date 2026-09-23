    def load(self, rawdata):
        """Load cookies from a string (presumably HTTP_COOKIE) or
        from a dictionary.  Loading cookies from a dictionary 'd'
        is equivalent to calling:
            map(Cookie.__setitem__, d.keys(), d.values())
        """
        if isinstance(rawdata, str):
            self.__parse_string(rawdata)
        else:
            # self.update() wouldn't call our custom __setitem__
            for key, value in rawdata.items():
                self[key] = value
        return
