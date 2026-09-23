    def _choose_path(self, fast_path, slow_path, group):
        path = slow_path
        res = slow_path(group)

        # if we make it here, test if we can use the fast path
        try:
            res_fast = fast_path(group)

            # verify fast path does not change columns (and names), otherwise
            # its results cannot be joined with those of the slow path
            if res_fast.columns != group.columns:
                return path, res
            # verify numerical equality with the slow path
            if res.shape == res_fast.shape:
                res_r = res.values.ravel()
                res_fast_r = res_fast.values.ravel()
                mask = notna(res_r)
                if (res_r[mask] == res_fast_r[mask]).all():
                    path = fast_path
        except Exception:
            pass
        return path, res
