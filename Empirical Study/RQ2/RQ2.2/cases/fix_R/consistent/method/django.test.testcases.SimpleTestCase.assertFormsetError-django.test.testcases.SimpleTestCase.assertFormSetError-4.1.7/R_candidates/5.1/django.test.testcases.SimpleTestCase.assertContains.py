    def assertContains(
        self, response, text, count=None, status_code=200, msg_prefix="", html=False
    ):
        """
        Assert that a response indicates that some content was retrieved
        successfully, (i.e., the HTTP status code was as expected) and that
        ``text`` occurs ``count`` times in the content of the response.
        If ``count`` is None, the count doesn't matter - the assertion is true
        if the text occurs at least once in the response.
        """
        text_repr, real_count, msg_prefix, content_repr = self._assert_contains(
            response, text, status_code, msg_prefix, html
        )

        if count is not None:
            self.assertEqual(
                real_count,
                count,
                (
                    f"{msg_prefix}Found {real_count} instances of {text_repr} "
                    f"(expected {count}) in the following response\n{content_repr}"
                ),
            )
        else:
            self.assertTrue(
                real_count != 0,
                (
                    f"{msg_prefix}Couldn't find {text_repr} in the following response\n"
                    f"{content_repr}"
                ),
            )
