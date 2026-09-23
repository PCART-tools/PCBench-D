    def get_result(self):
        cons: Callable[..., DataFrame | Series]
        sample: DataFrame | Series

        # series only
        if self._is_series:
            sample = cast("Series", self.objs[0])

            # stack blocks
            if self.bm_axis == 0:
                name = com.consensus_name_attr(self.objs)
                cons = sample._constructor

                arrs = [ser._values for ser in self.objs]

                res = concat_compat(arrs, axis=0)

                new_index: Index
                if self.ignore_index:
                    # We can avoid surprisingly-expensive _get_concat_axis
                    new_index = default_index(len(res))
                else:
                    new_index = self.new_axes[0]

                mgr = type(sample._mgr).from_array(res, index=new_index)

                result = sample._constructor_from_mgr(mgr, axes=mgr.axes)
                result._name = name
                return result.__finalize__(self, method="concat")

            # combine as columns in a frame
            else:
                data = dict(zip(range(len(self.objs)), self.objs))

                # GH28330 Preserves subclassed objects through concat
                cons = sample._constructor_expanddim

                index, columns = self.new_axes
                df = cons(data, index=index, copy=self.copy)
                df.columns = columns
                return df.__finalize__(self, method="concat")

        # combine block managers
        else:
            sample = cast("DataFrame", self.objs[0])

            mgrs_indexers = []
            for obj in self.objs:
                indexers = {}
                for ax, new_labels in enumerate(self.new_axes):
                    # ::-1 to convert BlockManager ax to DataFrame ax
                    if ax == self.bm_axis:
                        # Suppress reindexing on concat axis
                        continue

                    # 1-ax to convert BlockManager axis to DataFrame axis
                    obj_labels = obj.axes[1 - ax]
                    if not new_labels.equals(obj_labels):
                        indexers[ax] = obj_labels.get_indexer(new_labels)

                mgrs_indexers.append((obj._mgr, indexers))

            new_data = concatenate_managers(
                mgrs_indexers, self.new_axes, concat_axis=self.bm_axis, copy=self.copy
            )
            if not self.copy and not using_copy_on_write():
                new_data._consolidate_inplace()

            out = sample._constructor_from_mgr(new_data, axes=new_data.axes)
            return out.__finalize__(self, method="concat")
