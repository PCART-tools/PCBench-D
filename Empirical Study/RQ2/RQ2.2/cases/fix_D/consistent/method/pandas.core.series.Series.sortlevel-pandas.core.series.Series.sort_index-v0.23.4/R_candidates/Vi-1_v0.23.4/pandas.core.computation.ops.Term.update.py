    def update(self, value):
        """
        search order for local (i.e., @variable) variables:

        scope, key_variable
        [('locals', 'local_name'),
         ('globals', 'local_name'),
         ('locals', 'key'),
         ('globals', 'key')]
        """
        key = self.name

        # if it's a variable name (otherwise a constant)
        if isinstance(key, string_types):
            self.env.swapkey(self.local_name, key, new_value=value)

        self.value = value
