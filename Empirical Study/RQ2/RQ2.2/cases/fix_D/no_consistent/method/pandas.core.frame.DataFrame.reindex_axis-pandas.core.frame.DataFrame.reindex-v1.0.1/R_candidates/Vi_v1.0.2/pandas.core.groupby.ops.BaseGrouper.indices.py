    @cache_readonly
    def indices(self):
        """ dict {group name -> group indices} """
        if len(self.groupings) == 1:
            return self.groupings[0].indices
        else:
            codes_list = [ping.codes for ping in self.groupings]
            keys = [com.values_from_object(ping.group_index) for ping in self.groupings]
            return get_indexer_dict(codes_list, keys)
