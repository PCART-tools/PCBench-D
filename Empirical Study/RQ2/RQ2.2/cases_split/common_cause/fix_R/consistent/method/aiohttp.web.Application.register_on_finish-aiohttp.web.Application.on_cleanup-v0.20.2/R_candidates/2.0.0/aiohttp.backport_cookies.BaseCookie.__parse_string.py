    def __parse_string(self, str, patt=_CookiePattern):
        i = 0            # Our starting point
        n = len(str)     # Length of string
        M = None         # current morsel

        while 0 <= i < n:
            # Start looking for a cookie
            match = patt.match(str, i)
            if not match:
                # No more cookies
                break

            key, value = match.group("key"), match.group("val")
            i = match.end(0)

            # Parse the key, value in case it's metainfo
            if key[0] == "$":
                # We ignore attributes which pertain to the cookie
                # mechanism as a whole.  See RFC 2109.
                # (Does anyone care?)
                if M:
                    M[key[1:]] = value
            elif key.lower() in Morsel._reserved:
                if M:
                    if value is None:
                        if key.lower() in Morsel._flags:
                            M[key] = True
                    else:
                        M[key] = _unquote(value)
            elif value is not None:
                rval, cval = self.value_decode(value)
                self.__set(key, rval, cval)
                M = self[key]
