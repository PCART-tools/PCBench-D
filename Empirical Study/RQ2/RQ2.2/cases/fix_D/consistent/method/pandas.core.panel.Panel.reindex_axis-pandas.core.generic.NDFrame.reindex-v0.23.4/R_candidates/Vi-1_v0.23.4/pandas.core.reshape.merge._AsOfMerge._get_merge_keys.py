    def _get_merge_keys(self):

        # note this function has side effects
        (left_join_keys,
         right_join_keys,
         join_names) = super(_AsOfMerge, self)._get_merge_keys()

        # validate index types are the same
        for i, (lk, rk) in enumerate(zip(left_join_keys, right_join_keys)):
            if not is_dtype_equal(lk.dtype, rk.dtype):
                raise MergeError("incompatible merge keys [{i}] {lkdtype} and "
                                 "{rkdtype}, must be the same type"
                                 .format(i=i, lkdtype=lk.dtype,
                                         rkdtype=rk.dtype))

        # validate tolerance; must be a Timedelta if we have a DTI
        if self.tolerance is not None:

            if self.left_index:
                lt = self.left.index
            else:
                lt = left_join_keys[-1]

            msg = ("incompatible tolerance {tolerance}, must be compat "
                   "with type {lkdtype}".format(
                       tolerance=type(self.tolerance),
                       lkdtype=lt.dtype))

            if is_datetime64_dtype(lt) or is_datetime64tz_dtype(lt):
                if not isinstance(self.tolerance, Timedelta):
                    raise MergeError(msg)
                if self.tolerance < Timedelta(0):
                    raise MergeError("tolerance must be positive")

            elif is_int64_dtype(lt):
                if not is_integer(self.tolerance):
                    raise MergeError(msg)
                if self.tolerance < 0:
                    raise MergeError("tolerance must be positive")

            else:
                raise MergeError("key must be integer or timestamp")

        # validate allow_exact_matches
        if not is_bool(self.allow_exact_matches):
            msg = "allow_exact_matches must be boolean, passed {passed}"
            raise MergeError(msg.format(passed=self.allow_exact_matches))

        return left_join_keys, right_join_keys, join_names
