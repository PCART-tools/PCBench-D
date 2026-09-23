    def getsize_multiline(
        self,
        text,
        direction=None,
        spacing=4,
        features=None,
        language=None,
        stroke_width=0,
    ):
        """
        .. deprecated:: 9.2.0

        Use :py:meth:`.ImageDraw.multiline_textbbox` instead.

        See :ref:`deprecations <Font size and offset methods>` for more information.

        Returns width and height (in pixels) of given text if rendered in font
        with provided direction, features, and language, while respecting
        newline characters.

        :param text: Text to measure.

        :param direction: Direction of the text. It can be 'rtl' (right to
                          left), 'ltr' (left to right) or 'ttb' (top to bottom).
                          Requires libraqm.

        :param spacing: The vertical gap between lines, defaulting to 4 pixels.

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

                         .. versionadded:: 6.0.0

        :param stroke_width: The width of the text stroke.

                         .. versionadded:: 6.2.0

        :return: (width, height)
        """
        deprecate("getsize_multiline", 10, "ImageDraw.multiline_textbbox")
        max_width = 0
        lines = self._multiline_split(text)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            line_spacing = self.getsize("A", stroke_width=stroke_width)[1] + spacing
            for line in lines:
                line_width, line_height = self.getsize(
                    line, direction, features, language, stroke_width
                )
                max_width = max(max_width, line_width)

        return max_width, len(lines) * line_spacing - spacing
