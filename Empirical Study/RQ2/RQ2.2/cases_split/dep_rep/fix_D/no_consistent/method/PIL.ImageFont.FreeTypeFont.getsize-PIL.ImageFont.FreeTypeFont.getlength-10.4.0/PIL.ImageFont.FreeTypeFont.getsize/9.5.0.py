    def getsize(
        self,
        text,
        direction=None,
        features=None,
        language=None,
        stroke_width=0,
    ):
        """
        .. deprecated:: 9.2.0

        Use :py:meth:`getlength()` to measure the offset of following text with
        1/64 pixel precision.
        Use :py:meth:`getbbox()` to get the exact bounding box based on an anchor.

        See :ref:`deprecations <Font size and offset methods>` for more information.

        Returns width and height (in pixels) of given text if rendered in font with
        provided direction, features, and language.

        .. note:: For historical reasons this function measures text height from
            the ascender line instead of the top, see :ref:`text-anchors`.
            If you wish to measure text height from the top, it is recommended
            to use the bottom value of :meth:`getbbox` with ``anchor='lt'`` instead.

        :param text: Text to measure.

        :param direction: Direction of the text. It can be 'rtl' (right to
                          left), 'ltr' (left to right) or 'ttb' (top to bottom).
                          Requires libraqm.

                          .. versionadded:: 4.2.0

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

                         .. versionadded:: 4.2.0

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
        deprecate("getsize", 10, "getbbox or getlength")
        # vertical offset is added for historical reasons
        # see https://github.com/python-pillow/Pillow/pull/4910#discussion_r486682929
        size, offset = self.font.getsize(text, "L", direction, features, language)
        return (
            size[0] + stroke_width * 2,
            size[1] + stroke_width * 2 + offset[1],
        )
