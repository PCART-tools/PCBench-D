    def _resolve_name(self):
        # must be a queryables
        if self.side == 'left':
            if self.name not in self.env.queryables:
                raise NameError('name {0!r} is not defined'.format(self.name))
            return self.name

        # resolve the rhs (and allow it to be None)
        try:
            return self.env.resolve(self.name, is_local=False)
        except UndefinedVariableError:
            return self.name
