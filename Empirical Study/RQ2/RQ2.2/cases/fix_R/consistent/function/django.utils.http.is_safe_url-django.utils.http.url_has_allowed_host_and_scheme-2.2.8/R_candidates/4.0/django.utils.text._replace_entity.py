def _replace_entity(match):
    text = match[1]
    if text[0] == '#':
        text = text[1:]
        try:
            if text[0] in 'xX':
                c = int(text[1:], 16)
            else:
                c = int(text)
            return chr(c)
        except ValueError:
            return match[0]
    else:
        try:
            return chr(html.entities.name2codepoint[text])
        except KeyError:
            return match[0]
