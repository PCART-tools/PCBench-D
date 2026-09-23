    def _assert_contains(self, response, text, status_code, msg_prefix, html):
        # If the response supports deferred rendering and hasn't been rendered
        # yet, then ensure that it does get rendered before proceeding further.
        if (
            hasattr(response, "render")
            and callable(response.render)
            and not response.is_rendered
        ):
            response.render()

        if msg_prefix:
            msg_prefix += ": "

        self.assertEqual(
            response.status_code,
            status_code,
            msg_prefix + "Couldn't retrieve content: Response code was %d"
            " (expected %d)" % (response.status_code, status_code),
        )

        if response.streaming:
            content = b"".join(response.streaming_content)
        else:
            content = response.content
        content_repr = safe_repr(content)
        if not isinstance(text, bytes) or html:
            text = str(text)
            content = content.decode(response.charset)
            text_repr = "'%s'" % text
        else:
            text_repr = repr(text)
        if html:
            content = assert_and_parse_html(
                self, content, None, "Response's content is not valid HTML:"
            )
            text = assert_and_parse_html(
                self, text, None, "Second argument is not valid HTML:"
            )
        real_count = content.count(text)
        return text_repr, real_count, msg_prefix, content_repr
