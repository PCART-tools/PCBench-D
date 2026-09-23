    def _rebuild_ref_locs(self):
        """Take _ref_locs and set the individual block ref_locs, skipping Nones
        no effect on a unique index
        """
        if getattr(self, '_ref_locs', None) is not None:
            item_count = 0
            for v in self._ref_locs:
                if v is not None:
                    block, item_loc = v
                    if block._ref_locs is None:
                        block.reset_ref_locs()
                    block._ref_locs[item_loc] = item_count
                    item_count += 1
