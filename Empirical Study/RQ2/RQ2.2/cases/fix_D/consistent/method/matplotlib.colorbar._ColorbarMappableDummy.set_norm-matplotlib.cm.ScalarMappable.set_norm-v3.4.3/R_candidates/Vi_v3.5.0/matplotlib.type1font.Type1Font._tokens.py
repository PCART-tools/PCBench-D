    @classmethod
    def _tokens(cls, text):
        """
        A PostScript tokenizer. Yield (token, value) pairs such as
        (_TokenType.whitespace, '   ') or (_TokenType.name, '/Foobar').
        """
        # Preload enum members for speed.
        tok_whitespace = _TokenType.whitespace
        tok_name = _TokenType.name
        tok_string = _TokenType.string
        tok_delimiter = _TokenType.delimiter
        tok_number = _TokenType.number
        pos = 0
        while pos < len(text):
            match = cls._whitespace_or_comment_re.match(text, pos)
            if match:
                yield (tok_whitespace, match.group())
                pos = match.end()
            elif text[pos:pos+1] == b'(':
                start = pos
                pos += 1
                depth = 1
                while depth:
                    match = cls._instring_re.search(text, pos)
                    if match is None:
                        return
                    pos = match.end()
                    if match.group() == b'(':
                        depth += 1
                    elif match.group() == b')':
                        depth -= 1
                    else:  # a backslash - skip the next character
                        pos += 1
                yield (tok_string, text[start:pos])
            elif text[pos:pos + 2] in (b'<<', b'>>'):
                yield (tok_delimiter, text[pos:pos + 2])
                pos += 2
            elif text[pos:pos+1] == b'<':
                start = pos
                pos = text.index(b'>', pos)
                yield (tok_string, text[start:pos])
            else:
                match = cls._token_re.match(text, pos)
                if match:
                    try:
                        float(match.group())
                        yield (tok_number, match.group())
                    except ValueError:
                        yield (tok_name, match.group())
                    pos = match.end()
                else:
                    yield (tok_delimiter, text[pos:pos + 1])
                    pos += 1
