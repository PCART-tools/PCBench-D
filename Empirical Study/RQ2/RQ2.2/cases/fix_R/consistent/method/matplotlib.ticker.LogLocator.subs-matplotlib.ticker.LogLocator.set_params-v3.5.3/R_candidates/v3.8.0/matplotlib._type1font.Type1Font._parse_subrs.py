    def _parse_subrs(self, tokens, _data):
        count_token = next(tokens)
        if not count_token.is_number():
            raise RuntimeError(
                f"Token following /Subrs must be a number, was {count_token}"
            )
        count = count_token.value()
        array = [None] * count
        next(t for t in tokens if t.is_keyword('array'))
        for _ in range(count):
            next(t for t in tokens if t.is_keyword('dup'))
            index_token = next(tokens)
            if not index_token.is_number():
                raise RuntimeError(
                    "Token following dup in Subrs definition must be a "
                    f"number, was {index_token}"
                )
            nbytes_token = next(tokens)
            if not nbytes_token.is_number():
                raise RuntimeError(
                    "Second token following dup in Subrs definition must "
                    f"be a number, was {nbytes_token}"
                )
            token = next(tokens)
            if not token.is_keyword(self._abbr['RD']):
                raise RuntimeError(
                    f"Token preceding subr must be {self._abbr['RD']}, "
                    f"was {token}"
                )
            binary_token = tokens.send(1+nbytes_token.value())
            array[index_token.value()] = binary_token.value()

        return array, next(tokens).endpos()
