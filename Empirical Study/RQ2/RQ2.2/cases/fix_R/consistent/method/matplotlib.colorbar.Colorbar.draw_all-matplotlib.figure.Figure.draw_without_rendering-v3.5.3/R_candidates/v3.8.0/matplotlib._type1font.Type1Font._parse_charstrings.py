    @staticmethod
    def _parse_charstrings(tokens, _data):
        count_token = next(tokens)
        if not count_token.is_number():
            raise RuntimeError(
                "Token following /CharStrings must be a number, "
                f"was {count_token}"
            )
        count = count_token.value()
        charstrings = {}
        next(t for t in tokens if t.is_keyword('begin'))
        while True:
            token = next(t for t in tokens
                         if t.is_keyword('end') or t.is_slash_name())
            if token.raw == 'end':
                return charstrings, token.endpos()
            glyphname = token.value()
            nbytes_token = next(tokens)
            if not nbytes_token.is_number():
                raise RuntimeError(
                    f"Token following /{glyphname} in CharStrings definition "
                    f"must be a number, was {nbytes_token}"
                )
            next(tokens)  # usually RD or |-
            binary_token = tokens.send(1+nbytes_token.value())
            charstrings[glyphname] = binary_token.value()
