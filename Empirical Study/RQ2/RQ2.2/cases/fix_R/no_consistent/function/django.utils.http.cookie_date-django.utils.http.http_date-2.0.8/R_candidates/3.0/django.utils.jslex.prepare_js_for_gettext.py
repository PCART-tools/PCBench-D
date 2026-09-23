def prepare_js_for_gettext(js):
    """
    Convert the Javascript source `js` into something resembling C for
    xgettext.

    What actually happens is that all the regex literals are replaced with
    "REGEX".
    """
    def escape_quotes(m):
        """Used in a regex to properly escape double quotes."""
        s = m.group(0)
        if s == '"':
            return r'\"'
        else:
            return s

    lexer = JsLexer()
    c = []
    for name, tok in lexer.lex(js):
        if name == 'regex':
            # C doesn't grok regexes, and they aren't needed for gettext,
            # so just output a string instead.
            tok = '"REGEX"'
        elif name == 'string':
            # C doesn't have single-quoted strings, so make all strings
            # double-quoted.
            if tok.startswith("'"):
                guts = re.sub(r"\\.|.", escape_quotes, tok[1:-1])
                tok = '"' + guts + '"'
        elif name == 'id':
            # C can't deal with Unicode escapes in identifiers.  We don't
            # need them for gettext anyway, so replace them with something
            # innocuous
            tok = tok.replace("\\", "U")
        c.append(tok)
    return ''.join(c)
