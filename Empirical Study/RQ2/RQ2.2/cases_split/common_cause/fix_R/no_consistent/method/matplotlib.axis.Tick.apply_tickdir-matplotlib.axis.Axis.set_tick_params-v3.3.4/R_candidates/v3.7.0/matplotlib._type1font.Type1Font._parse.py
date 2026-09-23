    def _parse(self):
        """
        Find the values of various font properties. This limited kind
        of parsing is described in Chapter 10 "Adobe Type Manager
        Compatibility" of the Type-1 spec.
        """
        # Start with reasonable defaults
        prop = {'Weight': 'Regular', 'ItalicAngle': 0.0, 'isFixedPitch': False,
                'UnderlinePosition': -100, 'UnderlineThickness': 50}
        pos = {}
        data = self.parts[0] + self.decrypted

        source = _tokenize(data, True)
        while True:
            # See if there is a key to be assigned a value
            # e.g. /FontName in /FontName /Helvetica def
            try:
                token = next(source)
            except StopIteration:
                break
            if token.is_delim():
                # skip over this - we want top-level keys only
                _expression(token, source, data)
            if token.is_slash_name():
                key = token.value()
                keypos = token.pos
            else:
                continue

            # Some values need special parsing
            if key in ('Subrs', 'CharStrings', 'Encoding', 'OtherSubrs'):
                prop[key], endpos = {
                    'Subrs': self._parse_subrs,
                    'CharStrings': self._parse_charstrings,
                    'Encoding': self._parse_encoding,
                    'OtherSubrs': self._parse_othersubrs
                }[key](source, data)
                pos.setdefault(key, []).append((keypos, endpos))
                continue

            try:
                token = next(source)
            except StopIteration:
                break

            if isinstance(token, _KeywordToken):
                # constructs like
                # FontDirectory /Helvetica known {...} {...} ifelse
                # mean the key was not really a key
                continue

            if token.is_delim():
                value = _expression(token, source, data).raw
            else:
                value = token.value()

            # look for a 'def' possibly preceded by access modifiers
            try:
                kw = next(
                    kw for kw in source
                    if not kw.is_keyword('readonly', 'noaccess', 'executeonly')
                )
            except StopIteration:
                break

            # sometimes noaccess def and readonly def are abbreviated
            if kw.is_keyword('def', self._abbr['ND'], self._abbr['NP']):
                prop[key] = value
                pos.setdefault(key, []).append((keypos, kw.endpos()))

            # detect the standard abbreviations
            if value == '{noaccess def}':
                self._abbr['ND'] = key
            elif value == '{noaccess put}':
                self._abbr['NP'] = key
            elif value == '{string currentfile exch readstring pop}':
                self._abbr['RD'] = key

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
        # Decrypt the encrypted parts
        ndiscard = prop.get('lenIV', 4)
        cs = prop['CharStrings']
        for key, value in cs.items():
            cs[key] = self._decrypt(value, 'charstring', ndiscard)
        if 'Subrs' in prop:
            prop['Subrs'] = [
                self._decrypt(value, 'charstring', ndiscard)
                for value in prop['Subrs']
            ]

        self.prop = prop
        self._pos = pos
