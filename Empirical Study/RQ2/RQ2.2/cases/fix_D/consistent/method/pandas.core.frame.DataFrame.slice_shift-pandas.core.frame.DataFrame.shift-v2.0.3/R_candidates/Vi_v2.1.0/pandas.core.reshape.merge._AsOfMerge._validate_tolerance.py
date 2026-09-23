    def _validate_tolerance(self, left_join_keys: list[ArrayLike]) -> None:
        # validate tolerance; datetime.timedelta or Timedelta if we have a DTI
        if self.tolerance is not None:
            if self.left_index:
                lt = self.left.index._values
            else:
                lt = left_join_keys[-1]

            msg = (
                f"incompatible tolerance {self.tolerance}, must be compat "
                f"with type {repr(lt.dtype)}"
            )

            if needs_i8_conversion(lt.dtype):
                if not isinstance(self.tolerance, datetime.timedelta):
                    raise MergeError(msg)
                if self.tolerance < Timedelta(0):
                    raise MergeError("tolerance must be positive")

            elif is_integer_dtype(lt.dtype):
                if not is_integer(self.tolerance):
                    raise MergeError(msg)
                if self.tolerance < 0:
                    raise MergeError("tolerance must be positive")

            elif is_float_dtype(lt.dtype):
                if not is_number(self.tolerance):
                    raise MergeError(msg)
                # error: Unsupported operand types for > ("int" and "Number")
                if self.tolerance < 0:  # type: ignore[operator]
                    raise MergeError("tolerance must be positive")

            else:
                raise MergeError("key must be integer, timestamp or float")
