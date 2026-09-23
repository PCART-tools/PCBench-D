    @classmethod
    def _tokens(cls, text):
        """
        A PostScript tokenizer. Yield (token, value) pairs such as
        (cls._whitespace, '   ') or (cls._name, '/Foobar').
        """
        pos = 0
        while pos < len(text):
            match = (cls._comment_re.match(text[pos:]) or
                     cls._whitespace_re.match(text[pos:]))
            if match:
                yield (cls._whitespace, match.group())
                pos += match.end()
            elif text[pos] == b'(':
                start = pos
                pos += 1
                depth = 1
                while depth:
                    match = cls._instring_re.search(text[pos:])
                    if match is None:
                        return
                    pos += match.end()
                    if match.group() == b'(':
                        depth += 1
                    elif match.group() == b')':
                        depth -= 1
                    else:  # a backslash - skip the next character
                        pos += 1
                yield (cls._string, text[start:pos])
            elif text[pos:pos + 2] in (b'<<', b'>>'):
                yield (cls._delimiter, text[pos:pos + 2])
                pos += 2
            elif text[pos] == b'<':
                start = pos
                pos += text[pos:].index(b'>')
                yield (cls._string, text[start:pos])
            else:
                match = cls._token_re.match(text[pos:])
                if match:
                    try:
                        float(match.group())
                        yield (cls._number, match.group())
                    except ValueError:
                        yield (cls._name, match.group())
                    pos += match.end()
                else:
                    yield (cls._delimiter, text[pos:pos + 1])
                    pos += 1
