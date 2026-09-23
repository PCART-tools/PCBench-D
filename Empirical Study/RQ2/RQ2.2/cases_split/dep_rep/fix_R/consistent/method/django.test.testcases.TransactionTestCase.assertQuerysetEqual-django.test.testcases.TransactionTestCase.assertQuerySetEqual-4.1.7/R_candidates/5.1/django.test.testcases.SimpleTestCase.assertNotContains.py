    def assertNotContains(
        self, response, text, status_code=200, msg_prefix="", html=False
    ):
        """
        Assert that a response indicates that some content was retrieved
        successfully, (i.e., the HTTP status code was as expected) and that
        ``text`` doesn't occur in the content of the response.
        """
        text_repr, real_count, msg_prefix, content_repr = self._assert_contains(
            response, text, status_code, msg_prefix, html
        )

        self.assertEqual(
            real_count,
            0,
            (
                f"{msg_prefix}{text_repr} unexpectedly found in the following response"
                f"\n{content_repr}"
            ),
        )
