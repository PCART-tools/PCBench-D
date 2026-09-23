    def add_resource(self, path, *, name=None):
        if path and not path.startswith('/'):
            raise ValueError("path should be started with / or be empty")
        if not ('{' in path or '}' in path or self.ROUTE_RE.search(path)):
            resource = PlainResource(quote(path, safe='/'), name=name)
            self._reg_resource(resource)
            return resource

        pattern = ''
        formatter = ''
        for part in self.ROUTE_RE.split(path):
            match = self.DYN.fullmatch(part)
            if match:
                pattern += '(?P<{}>{})'.format(match.group('var'), self.GOOD)
                formatter += '{' + match.group('var') + '}'
                continue

            match = self.DYN_WITH_RE.fullmatch(part)
            if match:
                pattern += '(?P<{var}>{re})'.format(**match.groupdict())
                formatter += '{' + match.group('var') + '}'
                continue

            if '{' in part or '}' in part:
                raise ValueError("Invalid path '{}'['{}']".format(path, part))

            part = quote(part, safe='/')
            formatter += part
            pattern += re.escape(part)

        try:
            compiled = re.compile(pattern)
        except re.error as exc:
            raise ValueError(
                "Bad pattern '{}': {}".format(pattern, exc)) from None
        resource = DynamicResource(compiled, formatter, name=name)
        self._reg_resource(resource)
        return resource
