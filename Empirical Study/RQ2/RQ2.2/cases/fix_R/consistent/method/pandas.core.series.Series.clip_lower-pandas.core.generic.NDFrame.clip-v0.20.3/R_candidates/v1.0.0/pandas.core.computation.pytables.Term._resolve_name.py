    def _resolve_name(self):
        # must be a queryables
        if self.side == "left":
            # Note: The behavior of __new__ ensures that self.name is a str here
            if self.name not in self.env.queryables:
                raise NameError(f"name {repr(self.name)} is not defined")
            return self.name

        # resolve the rhs (and allow it to be None)
        try:
            return self.env.resolve(self.name, is_local=False)
        except UndefinedVariableError:
            return self.name
