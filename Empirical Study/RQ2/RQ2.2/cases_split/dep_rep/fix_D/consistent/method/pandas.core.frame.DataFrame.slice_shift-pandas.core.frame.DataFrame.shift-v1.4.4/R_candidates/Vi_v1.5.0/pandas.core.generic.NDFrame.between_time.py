    @final
    def between_time(
        self: NDFrameT,
        start_time,
        end_time,
        include_start: bool_t | lib.NoDefault = lib.no_default,
        include_end: bool_t | lib.NoDefault = lib.no_default,
        inclusive: IntervalClosedType | None = None,
        axis=None,
    ) -> NDFrameT:
        """
        Select values between particular times of the day (e.g., 9:00-9:30 AM).

        By setting ``start_time`` to be later than ``end_time``,
        you can get the times that are *not* between the two times.

        Parameters
        ----------
        start_time : datetime.time or str
            Initial time as a time filter limit.
        end_time : datetime.time or str
            End time as a time filter limit.
        include_start : bool, default True
            Whether the start time needs to be included in the result.

            .. deprecated:: 1.4.0
               Arguments `include_start` and `include_end` have been deprecated
               to standardize boundary inputs. Use `inclusive` instead, to set
               each bound as closed or open.
        include_end : bool, default True
            Whether the end time needs to be included in the result.

            .. deprecated:: 1.4.0
               Arguments `include_start` and `include_end` have been deprecated
               to standardize boundary inputs. Use `inclusive` instead, to set
               each bound as closed or open.
        inclusive : {"both", "neither", "left", "right"}, default "both"
            Include boundaries; whether to set each bound as closed or open.
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Determine range time on index or columns value.
            For `Series` this parameter is unused and defaults to 0.

        Returns
        -------
        Series or DataFrame
            Data from the original object filtered to the specified dates range.

        Raises
        ------
        TypeError
            If the index is not  a :class:`DatetimeIndex`

        See Also
        --------
        at_time : Select values at a particular time of the day.
        first : Select initial periods of time series based on a date offset.
        last : Select final periods of time series based on a date offset.
        DatetimeIndex.indexer_between_time : Get just the index locations for
            values between particular times of the day.

        Examples
        --------
        >>> i = pd.date_range('2018-04-09', periods=4, freq='1D20min')
        >>> ts = pd.DataFrame({'A': [1, 2, 3, 4]}, index=i)
        >>> ts
                             A
        2018-04-09 00:00:00  1
        2018-04-10 00:20:00  2
        2018-04-11 00:40:00  3
        2018-04-12 01:00:00  4

        >>> ts.between_time('0:15', '0:45')
                             A
        2018-04-10 00:20:00  2
        2018-04-11 00:40:00  3

        You get the times that are *not* between two times by setting
        ``start_time`` later than ``end_time``:

        >>> ts.between_time('0:45', '0:15')
                             A
        2018-04-09 00:00:00  1
        2018-04-12 01:00:00  4
        """
        if axis is None:
            axis = self._stat_axis_number
        axis = self._get_axis_number(axis)

        index = self._get_axis(axis)
        if not isinstance(index, DatetimeIndex):
            raise TypeError("Index must be DatetimeIndex")

        old_include_arg_used = (include_start != lib.no_default) or (
            include_end != lib.no_default
        )

        if old_include_arg_used and inclusive is not None:
            raise ValueError(
                "Deprecated arguments `include_start` and `include_end` "
                "cannot be passed if `inclusive` has been given."
            )
        # If any of the deprecated arguments ('include_start', 'include_end')
        # have been passed
        elif old_include_arg_used:
            warnings.warn(
                "`include_start` and `include_end` are deprecated in "
                "favour of `inclusive`.",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
            left = True if include_start is lib.no_default else include_start
            right = True if include_end is lib.no_default else include_end

            inc_dict: dict[tuple[bool_t, bool_t], IntervalClosedType] = {
                (True, True): "both",
                (True, False): "left",
                (False, True): "right",
                (False, False): "neither",
            }
            inclusive = inc_dict[(left, right)]
        elif inclusive is None:
            # On arg removal inclusive can default to "both"
            inclusive = "both"
        left_inclusive, right_inclusive = validate_inclusive(inclusive)
        indexer = index.indexer_between_time(
            start_time,
            end_time,
            include_start=left_inclusive,
            include_end=right_inclusive,
        )
        return self._take_with_is_copy(indexer, axis=axis)
