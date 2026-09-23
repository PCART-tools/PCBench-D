    def _parse(self):
        """
        Find the values of various font properties. This limited kind
        of parsing is described in Chapter 10 "Adobe Type Manager
        Compatibility" of the Type-1 spec.
        """
        # Start with reasonable defaults
        prop = {'weight': 'Regular', 'ItalicAngle': 0.0, 'isFixedPitch': False,
                'UnderlinePosition': -100, 'UnderlineThickness': 50}
        filtered = ((token, value)
                    for token, value in self._tokens(self.parts[0])
                    if token is not _TokenType.whitespace)
        # The spec calls this an ASCII format; in Python 2.x we could
        # just treat the strings and names as opaque bytes but let's
        # turn them into proper Unicode, and be lenient in case of high bytes.
        convert = lambda x: x.decode('ascii', 'replace')
        for token, value in filtered:
            if token is _TokenType.name and value.startswith(b'/'):
                key = convert(value[1:])
                token, value = next(filtered)
                if token is _TokenType.name:
                    if value in (b'true', b'false'):
                        value = value == b'true'
                    else:
                        value = convert(value.lstrip(b'/'))
                elif token is _TokenType.string:
                    value = convert(value.lstrip(b'(').rstrip(b')'))
                elif token is _TokenType.number:
                    if b'.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                else:  # more complicated value such as an array
                    value = None
                if key != 'FontInfo' and value is not None:
                    prop[key] = value

        # Fill in the various *Name properties
        if 'FontName' not in prop:
            prop['FontName'] = (prop.get('FullName') or
                                prop.get('FamilyName') or
                                'Unknown')
        if 'FullName' not in prop:
            prop['FullName'] = prop['FontName']
        if 'FamilyName' not in prop:
            extras = ('(?i)([ -](regular|plain|italic|oblique|(semi)?bold|'
                      '(ultra)?light|extra|condensed))+$')
            prop['FamilyName'] = re.sub(extras, '', prop['FullName'])

        self.prop = prop
