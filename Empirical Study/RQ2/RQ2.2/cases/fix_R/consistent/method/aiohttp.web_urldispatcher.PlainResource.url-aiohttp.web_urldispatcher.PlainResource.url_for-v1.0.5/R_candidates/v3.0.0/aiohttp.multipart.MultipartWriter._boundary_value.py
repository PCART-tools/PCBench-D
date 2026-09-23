    @property
    def _boundary_value(self):
        """Wrap boundary parameter value in quotes, if necessary.

        Reads self.boundary and returns a unicode sting.
        """
        # Refer to RFCs 7231, 7230, 5234.
        #
        # parameter      = token "=" ( token / quoted-string )
        # token          = 1*tchar
        # quoted-string  = DQUOTE *( qdtext / quoted-pair ) DQUOTE
        # qdtext         = HTAB / SP / %x21 / %x23-5B / %x5D-7E / obs-text
        # obs-text       = %x80-FF
        # quoted-pair    = "\" ( HTAB / SP / VCHAR / obs-text )
        # tchar          = "!" / "#" / "$" / "%" / "&" / "'" / "*"
        #                  / "+" / "-" / "." / "^" / "_" / "`" / "|" / "~"
        #                  / DIGIT / ALPHA
        #                  ; any VCHAR, except delimiters
        # VCHAR           = %x21-7E
        value = self._boundary
        if re.match(self._valid_tchar_regex, value):
            return value.decode('ascii')  # cannot fail

        if re.search(self._invalid_qdtext_char_regex, value):
            raise ValueError("boundary value contains invalid characters")

        # escape %x5C and %x22
        quoted_value_content = value.replace(b'\\', b'\\\\')
        quoted_value_content = quoted_value_content.replace(b'"', b'\\"')

        return '"' + quoted_value_content.decode('ascii') + '"'
