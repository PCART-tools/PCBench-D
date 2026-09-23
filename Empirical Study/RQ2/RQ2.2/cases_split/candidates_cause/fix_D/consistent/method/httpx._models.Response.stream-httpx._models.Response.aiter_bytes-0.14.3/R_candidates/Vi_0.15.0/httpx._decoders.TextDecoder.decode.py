    def decode(self, data: bytes) -> str:
        """
        If an encoding is explicitly specified, then we use that.
        Otherwise our strategy is to attempt UTF-8, and fallback to Windows 1252.

        Note that UTF-8 is a strict superset of ascii, and Windows 1252 is a
        superset of the non-control characters in iso-8859-1, so we essentially
        end up supporting any of ascii, utf-8, iso-8859-1, cp1252.

        Given that UTF-8 is now by *far* the most widely used encoding, this
        should be a pretty robust strategy for cases where a charset has
        not been explicitly included.

        Useful stats on the prevalence of different charsets in the wild...

        * https://w3techs.com/technologies/overview/character_encoding
        * https://w3techs.com/technologies/history_overview/character_encoding

        The HTML5 spec also has some useful guidelines, suggesting defaults of
        either UTF-8 or Windows 1252 in most cases...

        * https://dev.w3.org/html5/spec-LC/Overview.html
        """
        if self.decoder is None:
            # If this is the first decode pass then we need to determine which
            # encoding to use by attempting UTF-8 and raising any decode errors.
            attempt_utf_8 = codecs.getincrementaldecoder("utf-8")(errors="strict")
            try:
                attempt_utf_8.decode(data)
            except UnicodeDecodeError:
                # Could not decode as UTF-8. Use Windows 1252.
                self.decoder = codecs.getincrementaldecoder("cp1252")(errors="replace")
            else:
                # Can decode as UTF-8. Use UTF-8 with lenient error settings.
                self.decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")

        return self.decoder.decode(data)
