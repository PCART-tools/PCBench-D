    @staticmethod
    def _norm_per_subplot_kw(per_subplot_kw):
        expanded = {}
        for k, v in per_subplot_kw.items():
            if isinstance(k, tuple):
                for sub_key in k:
                    if sub_key in expanded:
                        raise ValueError(f'The key {sub_key!r} appears multiple times.')
                    expanded[sub_key] = v
            else:
                if k in expanded:
                    raise ValueError(f'The key {k!r} appears multiple times.')
                expanded[k] = v
        return expanded
