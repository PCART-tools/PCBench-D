    def _decide_output_index(self, output, labels):
        if len(output) == len(labels):
            output_keys = labels
        else:
            output_keys = sorted(output)
            try:
                output_keys.sort()
            except Exception:  # pragma: no cover
                pass

            if isinstance(labels, MultiIndex):
                output_keys = MultiIndex.from_tuples(output_keys,
                                                     names=labels.names)

        return output_keys
