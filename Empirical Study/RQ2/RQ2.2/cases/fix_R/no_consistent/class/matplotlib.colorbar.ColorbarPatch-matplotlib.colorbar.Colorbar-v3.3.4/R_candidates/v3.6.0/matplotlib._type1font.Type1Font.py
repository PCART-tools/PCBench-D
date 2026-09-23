class Type1Font:
    """
    A class representing a Type-1 font, for use by backends.

    Attributes
    ----------
    parts : tuple
        A 3-tuple of the cleartext part, the encrypted part, and the finale of
        zeros.

    decrypted : bytes
        The decrypted form of ``parts[1]``.

    prop : dict[str, Any]
        A dictionary of font properties. Noteworthy keys include:

        - FontName: PostScript name of the font
        - Encoding: dict from numeric codes to glyph names
        - FontMatrix: bytes object encoding a matrix
        - UniqueID: optional font identifier, dropped when modifying the font
        - CharStrings: dict from glyph names to byte code
        - Subrs: array of byte code subroutines
        - OtherSubrs: bytes object encoding some PostScript code
    """
    __slots__ = ('parts', 'decrypted', 'prop', '_pos', '_abbr')
    # the _pos dict contains (begin, end) indices to parts[0] + decrypted
    # so that they can be replaced when transforming the font;
    # but since sometimes a definition appears in both parts[0] and decrypted,
    # _pos[name] is an array of such pairs
    #
    # _abbr maps three standard abbreviations to their particular names in
    # this font (e.g. 'RD' is named '-|' in some fonts)

    def __init__(self, input):
        """
        Initialize a Type-1 font.

        Parameters
        ----------
        input : str or 3-tuple
            Either a pfb file name, or a 3-tuple of already-decoded Type-1
            font `~.Type1Font.parts`.
        """
        if isinstance(input, tuple) and len(input) == 3:
            self.parts = input
        else:
            with open(input, 'rb') as file:
                data = self._read(file)
            self.parts = self._split(data)

        self.decrypted = self._decrypt(self.parts[1], 'eexec')
        self._abbr = {'RD': 'RD', 'ND': 'ND', 'NP': 'NP'}
        self._parse()

    def _read(self, file):
        """Read the font from a file, decoding into usable parts."""
        rawdata = file.read()
        if not rawdata.startswith(b'\x80'):
            return rawdata

        data = b''
        while rawdata:
            if not rawdata.startswith(b'\x80'):
                raise RuntimeError('Broken pfb file (expected byte 128, '
                                   'got %d)' % rawdata[0])
            type = rawdata[1]
            if type in (1, 2):
                length, = struct.unpack('<i', rawdata[2:6])
                segment = rawdata[6:6 + length]
                rawdata = rawdata[6 + length:]

            if type == 1:       # ASCII text: include verbatim
                data += segment
            elif type == 2:     # binary data: encode in hexadecimal
                data += binascii.hexlify(segment)
            elif type == 3:     # end of file
                break
            else:
                raise RuntimeError('Unknown segment type %d in pfb file' %
                                   type)

        return data

    def _split(self, data):
        """
        Split the Type 1 font into its three main parts.

        The three parts are: (1) the cleartext part, which ends in a
        eexec operator; (2) the encrypted part; (3) the fixed part,
        which contains 512 ASCII zeros possibly divided on various
        lines, a cleartomark operator, and possibly something else.
        """

        # Cleartext part: just find the eexec and skip whitespace
        idx = data.index(b'eexec')
        idx += len(b'eexec')
        while data[idx] in b' \t\r\n':
            idx += 1
        len1 = idx

        # Encrypted part: find the cleartomark operator and count
        # zeros backward
        idx = data.rindex(b'cleartomark') - 1
        zeros = 512
        while zeros and data[idx] in b'0' or data[idx] in b'\r\n':
            if data[idx] in b'0':
                zeros -= 1
            idx -= 1
        if zeros:
            # this may have been a problem on old implementations that
            # used the zeros as necessary padding
            _log.info('Insufficiently many zeros in Type 1 font')

        # Convert encrypted part to binary (if we read a pfb file, we may end
        # up converting binary to hexadecimal to binary again; but if we read
        # a pfa file, this part is already in hex, and I am not quite sure if
        # even the pfb format guarantees that it will be in binary).
        idx1 = len1 + ((idx - len1 + 2) & ~1)  # ensure an even number of bytes
        binary = binascii.unhexlify(data[len1:idx1])

        return data[:len1], binary, data[idx+1:]

    @staticmethod
    def _decrypt(ciphertext, key, ndiscard=4):
        """
        Decrypt ciphertext using the Type-1 font algorithm.

        The algorithm is described in Adobe's "Adobe Type 1 Font Format".
        The key argument can be an integer, or one of the strings
        'eexec' and 'charstring', which map to the key specified for the
        corresponding part of Type-1 fonts.

        The ndiscard argument should be an integer, usually 4.
        That number of bytes is discarded from the beginning of plaintext.
        """

        key = _api.check_getitem({'eexec': 55665, 'charstring': 4330}, key=key)
        plaintext = []
        for byte in ciphertext:
            plaintext.append(byte ^ (key >> 8))
            key = ((key+byte) * 52845 + 22719) & 0xffff

        return bytes(plaintext[ndiscard:])

    @staticmethod
    def _encrypt(plaintext, key, ndiscard=4):
        """
        Encrypt plaintext using the Type-1 font algorithm.

        The algorithm is described in Adobe's "Adobe Type 1 Font Format".
        The key argument can be an integer, or one of the strings
        'eexec' and 'charstring', which map to the key specified for the
        corresponding part of Type-1 fonts.

        The ndiscard argument should be an integer, usually 4. That
        number of bytes is prepended to the plaintext before encryption.
        This function prepends NUL bytes for reproducibility, even though
        the original algorithm uses random bytes, presumably to avoid
        cryptanalysis.
        """

        key = _api.check_getitem({'eexec': 55665, 'charstring': 4330}, key=key)
        ciphertext = []
        for byte in b'\0' * ndiscard + plaintext:
            c = byte ^ (key >> 8)
            ciphertext.append(c)
            key = ((key + c) * 52845 + 22719) & 0xffff

        return bytes(ciphertext)

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

    @staticmethod
    def _parse_encoding(tokens, _data):
        # this only works for encodings that follow the Adobe manual
        # but some old fonts include non-compliant data - we log a warning
        # and return a possibly incomplete encoding
        encoding = {}
        while True:
            token = next(t for t in tokens
                         if t.is_keyword('StandardEncoding', 'dup', 'def'))
            if token.is_keyword('StandardEncoding'):
                return _StandardEncoding, token.endpos()
            if token.is_keyword('def'):
                return encoding, token.endpos()
            index_token = next(tokens)
            if not index_token.is_number():
                _log.warning(
                    f"Parsing encoding: expected number, got {index_token}"
                )
                continue
            name_token = next(tokens)
            if not name_token.is_slash_name():
                _log.warning(
                    f"Parsing encoding: expected slash-name, got {name_token}"
                )
                continue
            encoding[index_token.value()] = name_token.value()

    @staticmethod
    def _parse_othersubrs(tokens, data):
        init_pos = None
        while True:
            token = next(tokens)
            if init_pos is None:
                init_pos = token.pos
            if token.is_delim():
                _expression(token, tokens, data)
            elif token.is_keyword('def', 'ND', '|-'):
                return data[init_pos:token.endpos()], token.endpos()

    def transform(self, effects):
        """
        Return a new font that is slanted and/or extended.

        Parameters
        ----------
        effects : dict
            A dict with optional entries:

            - 'slant' : float, default: 0
                Tangent of the angle that the font is to be slanted to the
                right. Negative values slant to the left.
            - 'extend' : float, default: 1
                Scaling factor for the font width. Values less than 1 condense
                the glyphs.

        Returns
        -------
        `Type1Font`
        """
        fontname = self.prop['FontName']
        italicangle = self.prop['ItalicAngle']

        array = [
            float(x) for x in (self.prop['FontMatrix']
                               .lstrip('[').rstrip(']').split())
        ]
        oldmatrix = np.eye(3, 3)
        oldmatrix[0:3, 0] = array[::2]
        oldmatrix[0:3, 1] = array[1::2]
        modifier = np.eye(3, 3)

        if 'slant' in effects:
            slant = effects['slant']
            fontname += '_Slant_%d' % int(1000 * slant)
            italicangle = round(
                float(italicangle) - np.arctan(slant) / np.pi * 180,
                5
            )
            modifier[1, 0] = slant

        if 'extend' in effects:
            extend = effects['extend']
            fontname += '_Extend_%d' % int(1000 * extend)
            modifier[0, 0] = extend

        newmatrix = np.dot(modifier, oldmatrix)
        array[::2] = newmatrix[0:3, 0]
        array[1::2] = newmatrix[0:3, 1]
        fontmatrix = (
            '[%s]' % ' '.join(_format_approx(x, 6) for x in array)
        )
        replacements = (
            [(x, '/FontName/%s def' % fontname)
             for x in self._pos['FontName']]
            + [(x, '/ItalicAngle %a def' % italicangle)
               for x in self._pos['ItalicAngle']]
            + [(x, '/FontMatrix %s readonly def' % fontmatrix)
               for x in self._pos['FontMatrix']]
            + [(x, '') for x in self._pos.get('UniqueID', [])]
        )

        data = bytearray(self.parts[0])
        data.extend(self.decrypted)
        len0 = len(self.parts[0])
        for (pos0, pos1), value in sorted(replacements, reverse=True):
            data[pos0:pos1] = value.encode('ascii', 'replace')
            if pos0 < len(self.parts[0]):
                if pos1 >= len(self.parts[0]):
                    raise RuntimeError(
                        f"text to be replaced with {value} spans "
                        "the eexec boundary"
                    )
                len0 += len(value) - pos1 + pos0

        data = bytes(data)
        return Type1Font((
            data[:len0],
            self._encrypt(data[len0:], 'eexec'),
            self.parts[2]
        ))
