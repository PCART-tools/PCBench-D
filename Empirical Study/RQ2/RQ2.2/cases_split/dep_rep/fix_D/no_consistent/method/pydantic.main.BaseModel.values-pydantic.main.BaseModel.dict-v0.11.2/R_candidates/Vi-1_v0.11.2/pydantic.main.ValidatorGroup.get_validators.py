    def get_validators(self, name):
        self.used_validators.add(name)
        specific_validators = self.validators.get(name)
        wildcard_validators = self.validators.get('*')
        if specific_validators or wildcard_validators:
            return (specific_validators or []) + (wildcard_validators or [])
