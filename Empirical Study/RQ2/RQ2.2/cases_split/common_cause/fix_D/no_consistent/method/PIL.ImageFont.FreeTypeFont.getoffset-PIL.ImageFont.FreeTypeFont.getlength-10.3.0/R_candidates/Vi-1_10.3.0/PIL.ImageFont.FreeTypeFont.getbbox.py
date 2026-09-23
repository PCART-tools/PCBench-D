    def getbbox(
        self,
        text,
        mode="",
        direction=None,
        features=None,
        language=None,
        stroke_width=0,
        anchor=None,
    ):
        """
        Returns bounding box (in pixels) of given text relative to given anchor
        when rendered in font with provided direction, features, and language.

        Use :py:meth:`getlength()` to get the offset of following text with
        1/64 pixel precision. The bounding box includes extra margins for
        some fonts, e.g. italics or accents.

        .. versionadded:: 8.0.0

        :param text: Text to render.
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

        :param stroke_width: The width of the text stroke.

        :param anchor:  The text anchor alignment. Determines the relative location of
                        the anchor to the text. The default alignment is top left,
                        specifically ``la`` for horizontal text and ``lt`` for
                        vertical text. See :ref:`text-anchors` for details.

        :return: ``(left, top, right, bottom)`` bounding box
        """
        _string_length_check(text)
        size, offset = self.font.getsize(
            text, mode, direction, features, language, anchor
        )
        left, top = offset[0] - stroke_width, offset[1] - stroke_width
        width, height = size[0] + 2 * stroke_width, size[1] + 2 * stroke_width
        return left, top, left + width, top + height
