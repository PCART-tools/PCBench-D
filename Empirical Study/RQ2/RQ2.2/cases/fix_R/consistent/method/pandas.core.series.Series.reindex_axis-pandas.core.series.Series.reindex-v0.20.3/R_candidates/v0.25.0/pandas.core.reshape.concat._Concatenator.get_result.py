    def get_result(self):

        # series only
        if self._is_series:

            # stack blocks
            if self.axis == 0:
                name = com.consensus_name_attr(self.objs)

                mgr = self.objs[0]._data.concat(
                    [x._data for x in self.objs], self.new_axes
                )
                cons = _concat._get_series_result_type(mgr, self.objs)
                return cons(mgr, name=name).__finalize__(self, method="concat")

            # combine as columns in a frame
            else:
                data = dict(zip(range(len(self.objs)), self.objs))
                cons = _concat._get_series_result_type(data)

                index, columns = self.new_axes
                df = cons(data, index=index)
                df.columns = columns
                return df.__finalize__(self, method="concat")

        # combine block managers
        else:
            mgrs_indexers = []
            for obj in self.objs:
                mgr = obj._data
                indexers = {}
                for ax, new_labels in enumerate(self.new_axes):
                    if ax == self.axis:
                        # Suppress reindexing on concat axis
                        continue

                    obj_labels = mgr.axes[ax]
                    if not new_labels.equals(obj_labels):
                        indexers[ax] = obj_labels.reindex(new_labels)[1]

                mgrs_indexers.append((obj._data, indexers))

            new_data = concatenate_block_managers(
                mgrs_indexers, self.new_axes, concat_axis=self.axis, copy=self.copy
            )
            if not self.copy:
                new_data._consolidate_inplace()

            cons = _concat._get_frame_result_type(new_data, self.objs)
            return cons._from_axes(new_data, self.new_axes).__finalize__(
                self, method="concat"
            )
