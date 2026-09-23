    def _choose_path(self, fast_path: Callable, slow_path: Callable, group: DataFrame):
        path = slow_path
        res = slow_path(group)

        if self.ngroups == 1:
            # no need to evaluate multiple paths when only
            # a single group exists
            return path, res

        # if we make it here, test if we can use the fast path
        try:
            res_fast = fast_path(group)
        except AssertionError:
            raise  # pragma: no cover
        except Exception:
            # GH#29631 For user-defined function, we can't predict what may be
            #  raised; see test_transform.test_transform_fastpath_raises
            return path, res

        # verify fast path returns either:
        # a DataFrame with columns equal to group.columns
        # OR a Series with index equal to group.columns
        if isinstance(res_fast, DataFrame):
            if not res_fast.columns.equals(group.columns):
                return path, res
        elif isinstance(res_fast, Series):
            if not res_fast.index.equals(group.columns):
                return path, res
        else:
            return path, res

        if res_fast.equals(res):
            path = fast_path

        return path, res
