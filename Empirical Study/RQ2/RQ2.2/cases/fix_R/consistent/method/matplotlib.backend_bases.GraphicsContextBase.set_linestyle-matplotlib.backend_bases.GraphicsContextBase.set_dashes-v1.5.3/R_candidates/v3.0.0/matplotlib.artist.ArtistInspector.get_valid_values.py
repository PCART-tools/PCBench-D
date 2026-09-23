    def get_valid_values(self, attr):
        """
        Get the legal arguments for the setter associated with *attr*.

        This is done by querying the docstring of the function *set_attr*
        for a line that begins with "ACCEPTS" or ".. ACCEPTS":

        e.g., for a line linestyle, return
        "[ ``'-'`` | ``'--'`` | ``'-.'`` | ``':'`` | ``'steps'`` | ``'None'``
        ]"
        """

        name = 'set_%s' % attr
        if not hasattr(self.o, name):
            raise AttributeError('%s has no function %s' % (self.o, name))
        func = getattr(self.o, name)

        docstring = func.__doc__
        if docstring is None:
            return 'unknown'

        if docstring.startswith('alias for '):
            return None

        match = self._get_valid_values_regex.search(docstring)
        if match is not None:
            return re.sub("\n *", " ", match.group(1))

        # Much faster than list(inspect.signature(func).parameters)[1],
        # although barely relevant wrt. matplotlib's total import time.
        param_name = func.__code__.co_varnames[1]
        match = re.search("(?m)^ *{} : (.+)".format(param_name), docstring)
        if match:
            return match.group(1)

        return 'unknown'
