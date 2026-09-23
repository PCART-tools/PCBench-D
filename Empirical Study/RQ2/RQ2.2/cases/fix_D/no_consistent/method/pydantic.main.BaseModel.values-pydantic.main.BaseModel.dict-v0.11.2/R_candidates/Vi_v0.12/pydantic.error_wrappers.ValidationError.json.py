    def json(self, *, indent=2):
        return json.dumps(self.errors(), indent=indent)
