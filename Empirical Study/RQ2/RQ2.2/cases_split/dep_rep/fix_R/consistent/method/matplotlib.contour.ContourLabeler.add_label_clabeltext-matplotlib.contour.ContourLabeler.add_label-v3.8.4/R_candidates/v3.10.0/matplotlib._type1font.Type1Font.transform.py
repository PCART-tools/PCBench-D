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
            fontname += f'_Slant_{int(1000 * slant)}'
            italicangle = round(
                float(italicangle) - np.arctan(slant) / np.pi * 180,
                5
            )
            modifier[1, 0] = slant

        if 'extend' in effects:
            extend = effects['extend']
            fontname += f'_Extend_{int(1000 * extend)}'
            modifier[0, 0] = extend

        newmatrix = np.dot(modifier, oldmatrix)
        array[::2] = newmatrix[0:3, 0]
        array[1::2] = newmatrix[0:3, 1]
        fontmatrix = (
            f"[{' '.join(_format_approx(x, 6) for x in array)}]"
        )
        replacements = (
            [(x, f'/FontName/{fontname} def')
             for x in self._pos['FontName']]
            + [(x, f'/ItalicAngle {italicangle} def')
               for x in self._pos['ItalicAngle']]
            + [(x, f'/FontMatrix {fontmatrix} readonly def')
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
