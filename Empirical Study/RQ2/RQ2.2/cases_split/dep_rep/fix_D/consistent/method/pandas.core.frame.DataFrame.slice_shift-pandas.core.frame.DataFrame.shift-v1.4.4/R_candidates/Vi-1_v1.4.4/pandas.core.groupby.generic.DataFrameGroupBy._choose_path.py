    def _choose_path(self, fast_path: Callable, slow_path: Callable, group: DataFrame):
        path = slow_path
        res = slow_path(group)

        # if we make it here, test if we can use the fast path
        try:
            res_fast = fast_path(group)
        except AssertionError:
            raise  # pragma: no cover
        except Exception:
            # GH#29631 For user-defined function, we can't predict what may be
            #  raised; see test_transform.test_transform_fastpath_raises
            return path, res

        # verify fast path does not change columns (and names), otherwise
        # its results cannot be joined with those of the slow path
        if not isinstance(res_fast, DataFrame):
            return path, res

        if not res_fast.columns.equals(group.columns):
            return path, res

        if res_fast.equals(res):
            path = fast_path

        return path, res
