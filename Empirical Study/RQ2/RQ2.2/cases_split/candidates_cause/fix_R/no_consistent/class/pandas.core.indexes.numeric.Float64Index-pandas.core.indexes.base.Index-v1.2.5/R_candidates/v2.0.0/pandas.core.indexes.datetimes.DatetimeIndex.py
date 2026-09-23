@inherit_names(
    DatetimeArray._field_ops
    + [
        method
        for method in DatetimeArray._datetimelike_methods
        if method not in ("tz_localize", "tz_convert", "strftime")
    ],
    DatetimeArray,
    wrap=True,
)
@inherit_names(["is_normalized"], DatetimeArray, cache=True)
@inherit_names(
    [
        "tz",
        "tzinfo",
        "dtype",
        "to_pydatetime",
        "_format_native_types",
        "date",
        "time",
        "timetz",
        "std",
    ]
    + DatetimeArray._bool_ops,
    DatetimeArray,
)
class DatetimeIndex(DatetimeTimedeltaMixin):
    """
    Immutable ndarray-like of datetime64 data.

    Represented internally as int64, and which can be boxed to Timestamp objects
    that are subclasses of datetime and carry metadata.

    .. versionchanged:: 2.0.0
        The various numeric date/time attributes (:attr:`~DatetimeIndex.day`,
        :attr:`~DatetimeIndex.month`, :attr:`~DatetimeIndex.year` etc.) now have dtype
        ``int32``. Previously they had dtype ``int64``.

    Parameters
    ----------
    data : array-like (1-dimensional)
        Datetime-like data to construct index with.
    freq : str or pandas offset object, optional
        One of pandas date offset strings or corresponding objects. The string
        'infer' can be passed in order to set the frequency of the index as the
        inferred frequency upon creation.
    tz : pytz.timezone or dateutil.tz.tzfile or datetime.tzinfo or str
        Set the Timezone of the data.
    normalize : bool, default False
        Normalize start/end dates to midnight before generating date range.
    closed : {'left', 'right'}, optional
        Set whether to include `start` and `end` that are on the
        boundary. The default includes boundary points on either end.
    ambiguous : 'infer', bool-ndarray, 'NaT', default 'raise'
        When clocks moved backward due to DST, ambiguous times may arise.
        For example in Central European Time (UTC+01), when going from 03:00
        DST to 02:00 non-DST, 02:30:00 local time occurs both at 00:30:00 UTC
        and at 01:30:00 UTC. In such a situation, the `ambiguous` parameter
        dictates how ambiguous times should be handled.

        - 'infer' will attempt to infer fall dst-transition hours based on
          order
        - bool-ndarray where True signifies a DST time, False signifies a
          non-DST time (note that this flag is only applicable for ambiguous
          times)
        - 'NaT' will return NaT where there are ambiguous times
        - 'raise' will raise an AmbiguousTimeError if there are ambiguous times.
    dayfirst : bool, default False
        If True, parse dates in `data` with the day first order.
    yearfirst : bool, default False
        If True parse dates in `data` with the year first order.
    dtype : numpy.dtype or DatetimeTZDtype or str, default None
        Note that the only NumPy dtype allowed is ‘datetime64[ns]’.
    copy : bool, default False
        Make a copy of input ndarray.
    name : label, default None
        Name to be stored in the index.

    Attributes
    ----------
    year
    month
    day
    hour
    minute
    second
    microsecond
    nanosecond
    date
    time
    timetz
    dayofyear
    day_of_year
    weekofyear
    week
    dayofweek
    day_of_week
    weekday
    quarter
    tz
    freq
    freqstr
    is_month_start
    is_month_end
    is_quarter_start
    is_quarter_end
    is_year_start
    is_year_end
    is_leap_year
    inferred_freq

    Methods
    -------
    normalize
    strftime
    snap
    tz_convert
    tz_localize
    round
    floor
    ceil
    to_period
    to_pydatetime
    to_series
    to_frame
    month_name
    day_name
    mean
    std

    See Also
    --------
    Index : The base pandas Index type.
    TimedeltaIndex : Index of timedelta64 data.
    PeriodIndex : Index of Period data.
    to_datetime : Convert argument to datetime.
    date_range : Create a fixed-frequency DatetimeIndex.

    Notes
    -----
    To learn more about the frequency strings, please see `this link
    <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases>`__.
    """

    _typ = "datetimeindex"

    _data_cls = DatetimeArray
    _supports_partial_string_indexing = True

    @property
    def _engine_type(self) -> type[libindex.DatetimeEngine]:
        return libindex.DatetimeEngine

    _data: DatetimeArray
    tz: dt.tzinfo | None

    # --------------------------------------------------------------------
    # methods that dispatch to DatetimeArray and wrap result

    @doc(DatetimeArray.strftime)
    def strftime(self, date_format) -> Index:
        arr = self._data.strftime(date_format)
        return Index(arr, name=self.name, dtype=object)

    @doc(DatetimeArray.tz_convert)
    def tz_convert(self, tz) -> DatetimeIndex:
        arr = self._data.tz_convert(tz)
        return type(self)._simple_new(arr, name=self.name, refs=self._references)

    @doc(DatetimeArray.tz_localize)
    def tz_localize(
        self,
        tz,
        ambiguous: TimeAmbiguous = "raise",
        nonexistent: TimeNonexistent = "raise",
    ) -> DatetimeIndex:
        arr = self._data.tz_localize(tz, ambiguous, nonexistent)
        return type(self)._simple_new(arr, name=self.name)

    @doc(DatetimeArray.to_period)
    def to_period(self, freq=None) -> PeriodIndex:
        from pandas.core.indexes.api import PeriodIndex

        arr = self._data.to_period(freq)
        return PeriodIndex._simple_new(arr, name=self.name)

    @doc(DatetimeArray.to_julian_date)
    def to_julian_date(self) -> Index:
        arr = self._data.to_julian_date()
        return Index._simple_new(arr, name=self.name)

    @doc(DatetimeArray.isocalendar)
    def isocalendar(self) -> DataFrame:
        df = self._data.isocalendar()
        return df.set_index(self)

    @cache_readonly
    def _resolution_obj(self) -> Resolution:
        return self._data._resolution_obj

    # --------------------------------------------------------------------
    # Constructors

    def __new__(
        cls,
        data=None,
        freq: Frequency | lib.NoDefault = lib.no_default,
        tz=lib.no_default,
        normalize: bool = False,
        closed=None,
        ambiguous: TimeAmbiguous = "raise",
        dayfirst: bool = False,
        yearfirst: bool = False,
        dtype: Dtype | None = None,
        copy: bool = False,
        name: Hashable = None,
    ) -> DatetimeIndex:
        if is_scalar(data):
            cls._raise_scalar_data_error(data)

        # - Cases checked above all return/raise before reaching here - #

        name = maybe_extract_name(name, data, cls)

        if (
            isinstance(data, DatetimeArray)
            and freq is lib.no_default
            and tz is lib.no_default
            and dtype is None
        ):
            # fastpath, similar logic in TimedeltaIndex.__new__;
            # Note in this particular case we retain non-nano.
            if copy:
                data = data.copy()
            return cls._simple_new(data, name=name)

        dtarr = DatetimeArray._from_sequence_not_strict(
            data,
            dtype=dtype,
            copy=copy,
            tz=tz,
            freq=freq,
            dayfirst=dayfirst,
            yearfirst=yearfirst,
            ambiguous=ambiguous,
        )
        refs = None
        if not copy and isinstance(data, (Index, ABCSeries)):
            refs = data._references

        subarr = cls._simple_new(dtarr, name=name, refs=refs)
        return subarr

    # --------------------------------------------------------------------

    @cache_readonly
    def _is_dates_only(self) -> bool:
        """
        Return a boolean if we are only dates (and don't have a timezone)

        Returns
        -------
        bool
        """
        from pandas.io.formats.format import is_dates_only

        # error: Argument 1 to "is_dates_only" has incompatible type
        # "Union[ExtensionArray, ndarray]"; expected "Union[ndarray,
        # DatetimeArray, Index, DatetimeIndex]"
        return self.tz is None and is_dates_only(self._values)  # type: ignore[arg-type]

    def __reduce__(self):
        d = {"data": self._data, "name": self.name}
        return _new_DatetimeIndex, (type(self), d), None

    def _is_comparable_dtype(self, dtype: DtypeObj) -> bool:
        """
        Can we compare values of the given dtype to our own?
        """
        if self.tz is not None:
            # If we have tz, we can compare to tzaware
            return is_datetime64tz_dtype(dtype)
        # if we dont have tz, we can only compare to tznaive
        return is_datetime64_dtype(dtype)

    # --------------------------------------------------------------------
    # Rendering Methods

    @property
    def _formatter_func(self):
        from pandas.io.formats.format import get_format_datetime64

        formatter = get_format_datetime64(is_dates_only_=self._is_dates_only)
        return lambda x: f"'{formatter(x)}'"

    # --------------------------------------------------------------------
    # Set Operation Methods

    def _can_range_setop(self, other) -> bool:
        # GH 46702: If self or other have non-UTC tzs, DST transitions prevent
        # range representation due to no singular step
        if (
            self.tz is not None
            and not timezones.is_utc(self.tz)
            and not timezones.is_fixed_offset(self.tz)
        ):
            return False
        if (
            other.tz is not None
            and not timezones.is_utc(other.tz)
            and not timezones.is_fixed_offset(other.tz)
        ):
            return False
        return super()._can_range_setop(other)

    # --------------------------------------------------------------------

    def _get_time_micros(self) -> npt.NDArray[np.int64]:
        """
        Return the number of microseconds since midnight.

        Returns
        -------
        ndarray[int64_t]
        """
        values = self._data._local_timestamps()

        ppd = periods_per_day(self._data._creso)

        frac = values % ppd
        if self.unit == "ns":
            micros = frac // 1000
        elif self.unit == "us":
            micros = frac
        elif self.unit == "ms":
            micros = frac * 1000
        elif self.unit == "s":
            micros = frac * 1_000_000
        else:  # pragma: no cover
            raise NotImplementedError(self.unit)

        micros[self._isnan] = -1
        return micros

    def snap(self, freq: Frequency = "S") -> DatetimeIndex:
        """
        Snap time stamps to nearest occurring frequency.

        Returns
        -------
        DatetimeIndex
        """
        # Superdumb, punting on any optimizing
        freq = to_offset(freq)

        dta = self._data.copy()

        for i, v in enumerate(self):
            s = v
            if not freq.is_on_offset(s):
                t0 = freq.rollback(s)
                t1 = freq.rollforward(s)
                if abs(s - t0) < abs(t1 - s):
                    s = t0
                else:
                    s = t1
            dta[i] = s

        return DatetimeIndex._simple_new(dta, name=self.name)

    # --------------------------------------------------------------------
    # Indexing Methods

    def _parsed_string_to_bounds(self, reso: Resolution, parsed: dt.datetime):
        """
        Calculate datetime bounds for parsed time string and its resolution.

        Parameters
        ----------
        reso : Resolution
            Resolution provided by parsed string.
        parsed : datetime
            Datetime from parsed string.

        Returns
        -------
        lower, upper: pd.Timestamp
        """
        per = Period(parsed, freq=reso.attr_abbrev)
        start, end = per.start_time, per.end_time

        # GH 24076
        # If an incoming date string contained a UTC offset, need to localize
        # the parsed date to this offset first before aligning with the index's
        # timezone
        start = start.tz_localize(parsed.tzinfo)
        end = end.tz_localize(parsed.tzinfo)

        if parsed.tzinfo is not None:
            if self.tz is None:
                raise ValueError(
                    "The index must be timezone aware when indexing "
                    "with a date string with a UTC offset"
                )
        # The flipped case with parsed.tz is None and self.tz is not None
        #  is ruled out bc parsed and reso are produced by _parse_with_reso,
        #  which localizes parsed.
        return start, end

    def _parse_with_reso(self, label: str):
        parsed, reso = super()._parse_with_reso(label)

        parsed = Timestamp(parsed)

        if self.tz is not None and parsed.tzinfo is None:
            # we special-case timezone-naive strings and timezone-aware
            #  DatetimeIndex
            # https://github.com/pandas-dev/pandas/pull/36148#issuecomment-687883081
            parsed = parsed.tz_localize(self.tz)

        return parsed, reso

    def _disallow_mismatched_indexing(self, key) -> None:
        """
        Check for mismatched-tzawareness indexing and re-raise as KeyError.
        """
        # we get here with isinstance(key, self._data._recognized_scalars)
        try:
            # GH#36148
            self._data._assert_tzawareness_compat(key)
        except TypeError as err:
            raise KeyError(key) from err

    def get_loc(self, key):
        """
        Get integer location for requested label

        Returns
        -------
        loc : int
        """
        self._check_indexing_error(key)

        orig_key = key
        if is_valid_na_for_dtype(key, self.dtype):
            key = NaT

        if isinstance(key, self._data._recognized_scalars):
            # needed to localize naive datetimes
            self._disallow_mismatched_indexing(key)
            key = Timestamp(key)

        elif isinstance(key, str):
            try:
                parsed, reso = self._parse_with_reso(key)
            except (ValueError, pytz.NonExistentTimeError) as err:
                raise KeyError(key) from err
            self._disallow_mismatched_indexing(parsed)

            if self._can_partial_date_slice(reso):
                try:
                    return self._partial_date_slice(reso, parsed)
                except KeyError as err:
                    raise KeyError(key) from err

            key = parsed

        elif isinstance(key, dt.timedelta):
            # GH#20464
            raise TypeError(
                f"Cannot index {type(self).__name__} with {type(key).__name__}"
            )

        elif isinstance(key, dt.time):
            return self.indexer_at_time(key)

        else:
            # unrecognized type
            raise KeyError(key)

        try:
            return Index.get_loc(self, key)
        except KeyError as err:
            raise KeyError(orig_key) from err

    @doc(DatetimeTimedeltaMixin._maybe_cast_slice_bound)
    def _maybe_cast_slice_bound(self, label, side: str):
        # GH#42855 handle date here instead of get_slice_bound
        if isinstance(label, dt.date) and not isinstance(label, dt.datetime):
            # Pandas supports slicing with dates, treated as datetimes at midnight.
            # https://github.com/pandas-dev/pandas/issues/31501
            label = Timestamp(label).to_pydatetime()

        label = super()._maybe_cast_slice_bound(label, side)
        self._data._assert_tzawareness_compat(label)
        return Timestamp(label)

    def slice_indexer(self, start=None, end=None, step=None):
        """
        Return indexer for specified label slice.
        Index.slice_indexer, customized to handle time slicing.

        In addition to functionality provided by Index.slice_indexer, does the
        following:

        - if both `start` and `end` are instances of `datetime.time`, it
          invokes `indexer_between_time`
        - if `start` and `end` are both either string or None perform
          value-based selection in non-monotonic cases.

        """
        # For historical reasons DatetimeIndex supports slices between two
        # instances of datetime.time as if it were applying a slice mask to
        # an array of (self.hour, self.minute, self.seconds, self.microsecond).
        if isinstance(start, dt.time) and isinstance(end, dt.time):
            if step is not None and step != 1:
                raise ValueError("Must have step size of 1 with time slices")
            return self.indexer_between_time(start, end)

        if isinstance(start, dt.time) or isinstance(end, dt.time):
            raise KeyError("Cannot mix time and non-time slice keys")

        def check_str_or_none(point) -> bool:
            return point is not None and not isinstance(point, str)

        # GH#33146 if start and end are combinations of str and None and Index is not
        # monotonic, we can not use Index.slice_indexer because it does not honor the
        # actual elements, is only searching for start and end
        if (
            check_str_or_none(start)
            or check_str_or_none(end)
            or self.is_monotonic_increasing
        ):
            return Index.slice_indexer(self, start, end, step)

        mask = np.array(True)
        raise_mask = np.array(True)
        if start is not None:
            start_casted = self._maybe_cast_slice_bound(start, "left")
            mask = start_casted <= self
            raise_mask = start_casted == self

        if end is not None:
            end_casted = self._maybe_cast_slice_bound(end, "right")
            mask = (self <= end_casted) & mask
            raise_mask = (end_casted == self) | raise_mask

        if not raise_mask.any():
            raise KeyError(
                "Value based partial slicing on non-monotonic DatetimeIndexes "
                "with non-existing keys is not allowed.",
            )
        indexer = mask.nonzero()[0][::step]
        if len(indexer) == len(self):
            return slice(None)
        else:
            return indexer

    # --------------------------------------------------------------------

    @property
    def inferred_type(self) -> str:
        # b/c datetime is represented as microseconds since the epoch, make
        # sure we can't have ambiguous indexing
        return "datetime64"

    def indexer_at_time(self, time, asof: bool = False) -> npt.NDArray[np.intp]:
        """
        Return index locations of values at particular time of day.

        Parameters
        ----------
        time : datetime.time or str
            Time passed in either as object (datetime.time) or as string in
            appropriate format ("%H:%M", "%H%M", "%I:%M%p", "%I%M%p",
            "%H:%M:%S", "%H%M%S", "%I:%M:%S%p", "%I%M%S%p").

        Returns
        -------
        np.ndarray[np.intp]

        See Also
        --------
        indexer_between_time : Get index locations of values between particular
            times of day.
        DataFrame.at_time : Select values at particular time of day.
        """
        if asof:
            raise NotImplementedError("'asof' argument is not supported")

        if isinstance(time, str):
            from dateutil.parser import parse

            time = parse(time).time()

        if time.tzinfo:
            if self.tz is None:
                raise ValueError("Index must be timezone aware.")
            time_micros = self.tz_convert(time.tzinfo)._get_time_micros()
        else:
            time_micros = self._get_time_micros()
        micros = _time_to_micros(time)
        return (time_micros == micros).nonzero()[0]

    def indexer_between_time(
        self, start_time, end_time, include_start: bool = True, include_end: bool = True
    ) -> npt.NDArray[np.intp]:
        """
        Return index locations of values between particular times of day.

        Parameters
        ----------
        start_time, end_time : datetime.time, str
            Time passed either as object (datetime.time) or as string in
            appropriate format ("%H:%M", "%H%M", "%I:%M%p", "%I%M%p",
            "%H:%M:%S", "%H%M%S", "%I:%M:%S%p","%I%M%S%p").
        include_start : bool, default True
        include_end : bool, default True

        Returns
        -------
        np.ndarray[np.intp]

        See Also
        --------
        indexer_at_time : Get index locations of values at particular time of day.
        DataFrame.between_time : Select values between particular times of day.
        """
        start_time = to_time(start_time)
        end_time = to_time(end_time)
        time_micros = self._get_time_micros()
        start_micros = _time_to_micros(start_time)
        end_micros = _time_to_micros(end_time)

        if include_start and include_end:
            lop = rop = operator.le
        elif include_start:
            lop = operator.le
            rop = operator.lt
        elif include_end:
            lop = operator.lt
            rop = operator.le
        else:
            lop = rop = operator.lt

        if start_time <= end_time:
            join_op = operator.and_
        else:
            join_op = operator.or_

        mask = join_op(lop(start_micros, time_micros), rop(time_micros, end_micros))

        return mask.nonzero()[0]
