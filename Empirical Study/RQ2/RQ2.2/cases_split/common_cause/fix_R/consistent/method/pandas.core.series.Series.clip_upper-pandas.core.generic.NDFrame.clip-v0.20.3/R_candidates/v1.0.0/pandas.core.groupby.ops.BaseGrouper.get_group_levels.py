    def get_group_levels(self):
        if not self.compressed and len(self.groupings) == 1:
            return [self.groupings[0].result_index]

        name_list = []
        for ping, codes in zip(self.groupings, self.reconstructed_codes):
            codes = ensure_platform_int(codes)
            levels = ping.result_index.take(codes)

            name_list.append(levels)

        return name_list
