    def json(self, indent=2):
        return json.dumps(self.errors_dict, indent=indent, sort_keys=True)
