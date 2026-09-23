    def _read_token(self) -> bytes:
        assert self.fp is not None

        token = b""
        while len(token) <= 10:  # read until next whitespace or limit of 10 characters
            c = self.fp.read(1)
            if not c:
                break
            elif c in b_whitespace:  # token ended
                if not token:
                    # skip whitespace at start
                    continue
                break
            elif c == b"#":
                # ignores rest of the line; stops at CR, LF or EOF
                while self.fp.read(1) not in b"\r\n":
                    pass
                continue
            token += c
        if not token:
            # Token was not even 1 byte
            msg = "Reached EOF while reading header"
            raise ValueError(msg)
        elif len(token) > 10:
            msg = f"Token too long in file header: {token.decode()}"
            raise ValueError(msg)
        return token
