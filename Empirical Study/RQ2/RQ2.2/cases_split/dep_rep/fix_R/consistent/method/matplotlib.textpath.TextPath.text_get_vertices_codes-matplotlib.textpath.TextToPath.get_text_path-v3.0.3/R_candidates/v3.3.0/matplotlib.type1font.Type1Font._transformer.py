    @classmethod
    def _transformer(cls, tokens, slant, extend):
        def fontname(name):
            result = name
            if slant:
                result += b'_Slant_%d' % int(1000 * slant)
            if extend != 1.0:
                result += b'_Extend_%d' % int(1000 * extend)
            return result

        def italicangle(angle):
            return b'%a' % (float(angle) - np.arctan(slant) / np.pi * 180)

        def fontmatrix(array):
            array = array.lstrip(b'[').rstrip(b']').split()
            array = [float(x) for x in array]
            oldmatrix = np.eye(3, 3)
            oldmatrix[0:3, 0] = array[::2]
            oldmatrix[0:3, 1] = array[1::2]
            modifier = np.array([[extend, 0, 0],
                                 [slant, 1, 0],
                                 [0, 0, 1]])
            newmatrix = np.dot(modifier, oldmatrix)
            array[::2] = newmatrix[0:3, 0]
            array[1::2] = newmatrix[0:3, 1]
            # Not directly using `b'%a' % x for x in array` for now as that
            # produces longer reprs on numpy<1.14, causing test failures.
            as_string = '[' + ' '.join(str(x) for x in array) + ']'
            return as_string.encode('latin-1')

        def replace(fun):
            def replacer(tokens):
                token, value = next(tokens)      # name, e.g., /FontMatrix
                yield value
                token, value = next(tokens)      # possible whitespace
                while token is _TokenType.whitespace:
                    yield value
                    token, value = next(tokens)
                if value != b'[':                # name/number/etc.
                    yield fun(value)
                else:                            # array, e.g., [1 2 3]
                    result = b''
                    while value != b']':
                        result += value
                        token, value = next(tokens)
                    result += value
                    yield fun(result)
            return replacer

        def suppress(tokens):
            for _ in itertools.takewhile(lambda x: x[1] != b'def', tokens):
                pass
            yield b''

        table = {b'/FontName': replace(fontname),
                 b'/ItalicAngle': replace(italicangle),
                 b'/FontMatrix': replace(fontmatrix),
                 b'/UniqueID': suppress}

        for token, value in tokens:
            if token is _TokenType.name and value in table:
                yield from table[value](
                    itertools.chain([(token, value)], tokens))
            else:
                yield value
