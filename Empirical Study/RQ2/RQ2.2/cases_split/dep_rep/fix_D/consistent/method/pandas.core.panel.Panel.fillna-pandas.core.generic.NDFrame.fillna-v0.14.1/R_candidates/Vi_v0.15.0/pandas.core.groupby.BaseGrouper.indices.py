    @cache_readonly
    def indices(self):
        """ dict {group name -> group indices} """
        if len(self.groupings) == 1:
            return self.groupings[0].indices
        else:
            label_list = [ping.labels for ping in self.groupings]
            keys = [_values_from_object(ping.group_index) for ping in self.groupings]
            return _get_indices_dict(label_list, keys)
