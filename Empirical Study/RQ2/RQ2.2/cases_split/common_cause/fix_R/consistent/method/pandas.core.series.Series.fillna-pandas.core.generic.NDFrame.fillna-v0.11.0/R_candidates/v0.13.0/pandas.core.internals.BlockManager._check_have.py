    def _check_have(self, item):
        if item not in self.items:
            raise KeyError('no item named %s' % com.pprint_thing(item))
