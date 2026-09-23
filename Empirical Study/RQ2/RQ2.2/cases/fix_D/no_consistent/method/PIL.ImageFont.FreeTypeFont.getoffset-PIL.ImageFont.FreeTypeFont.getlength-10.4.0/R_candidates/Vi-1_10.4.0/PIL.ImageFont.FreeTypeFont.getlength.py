    def getlength(
        self, text: str | bytes, mode="", direction=None, features=None, language=None
    ) -> float:
        """
        Returns length (in pixels with 1/64 precision) of given text when rendered
        in font with provided direction, features, and language.

        This is the amount by which following text should be offset.
        Text bounding box may extend past the length in some fonts,
        e.g. when using italics or accents.

        The result is returned as a float; it is a whole number if using basic layout.

        Note that the sum of two lengths may not equal the length of a concatenated
        string due to kerning. If you need to adjust for kerning, include the following
        character and subtract its length.

        For example, instead of ::

          hello = font.getlength("Hello")
          world = font.getlength("World")
          hello_world = hello + world  # not adjusted for kerning
          assert hello_world == font.getlength("HelloWorld")  # may fail

        use ::

          hello = font.getlength("HelloW") - font.getlength("W")  # adjusted for kerning
          world = font.getlength("World")
          hello_world = hello + world  # adjusted for kerning
          assert hello_world == font.getlength("HelloWorld")  # True

        or disable kerning with (requires libraqm) ::

          hello = draw.textlength("Hello", font, features=["-kern"])
          world = draw.textlength("World", font, features=["-kern"])
          hello_world = hello + world  # kerning is disabled, no need to adjust
          assert hello_world == draw.textlength("HelloWorld", font, features=["-kern"])

        .. versionadded:: 8.0.0

        :param text: Text to measure.
        :param mode: Used by some graphics drivers to indicate what mode the
                     driver prefers; if empty, the renderer may return either
                     mode. Note that the mode is always a string, to simplify
                     C-level implementations.

        :param direction: Direction of the text. It can be 'rtl' (right to
                          left), 'ltr' (left to right) or 'ttb' (top to bottom).
                          Requires libraqm.

        :param features: A list of OpenType font features to be used during text
                         layout. This is usually used to turn on optional
                         font features that are not enabled by default,
                         for example 'dlig' or 'ss01', but can be also
                         used to turn off default font features for
                         example '-liga' to disable ligatures or '-kern'
                         to disable kerning.  To get all supported
                         features, see
                         https://learn.microsoft.com/en-us/typography/opentype/spec/featurelist
                         Requires libraqm.

        :param language: Language of the text. Different languages may use
                         different glyph shapes or ligatures. This parameter tells
                         the font which language the text is in, and to apply the
                         correct substitutions as appropriate, if available.
                         It should be a `BCP 47 language code
                         <https://www.w3.org/International/articles/language-tags/>`_
                         Requires libraqm.

        :return: Either width for horizontal text, or height for vertical text.
        """
        _string_length_check(text)
        return self.font.getlength(text, mode, direction, features, language) / 64
