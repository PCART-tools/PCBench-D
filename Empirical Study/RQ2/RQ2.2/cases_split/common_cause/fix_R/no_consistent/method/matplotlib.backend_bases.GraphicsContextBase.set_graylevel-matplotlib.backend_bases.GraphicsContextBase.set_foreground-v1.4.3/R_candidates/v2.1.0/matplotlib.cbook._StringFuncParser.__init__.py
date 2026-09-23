    def __init__(self, str_func):
        """
        Parameters
        ----------
        str_func : string
            String to be parsed.

        """

        if not isinstance(str_func, six.string_types):
            raise ValueError("'%s' must be a string." % str_func)
        self._str_func = six.text_type(str_func)
        self._key, self._params = self._get_key_params()
        self._func = self._parse_func()
