    def __init__(
        self,
        freq="Min",
        closed: Literal["left", "right"] | None = None,
        label: str | None = None,
        how="mean",
        axis=0,
        fill_method=None,
        limit=None,
        loffset=None,
        kind: str | None = None,
        convention: str | None = None,
        base: int | None = None,
        origin: str | TimestampConvertibleTypes = "start_day",
        offset: TimedeltaConvertibleTypes | None = None,
        **kwargs,
    ):
        # Check for correctness of the keyword arguments which would
        # otherwise silently use the default if misspelled
        if label not in {None, "left", "right"}:
            raise ValueError(f"Unsupported value {label} for `label`")
        if closed not in {None, "left", "right"}:
            raise ValueError(f"Unsupported value {closed} for `closed`")
        if convention not in {None, "start", "end", "e", "s"}:
            raise ValueError(f"Unsupported value {convention} for `convention`")

        freq = to_offset(freq)

        end_types = {"M", "A", "Q", "BM", "BA", "BQ", "W"}
        rule = freq.rule_code
        if rule in end_types or ("-" in rule and rule[: rule.find("-")] in end_types):
            if closed is None:
                closed = "right"
            if label is None:
                label = "right"
        else:
            # The backward resample sets ``closed`` to ``'right'`` by default
            # since the last value should be considered as the edge point for
            # the last bin. When origin in "end" or "end_day", the value for a
            # specific ``Timestamp`` index stands for the resample result from
            # the current ``Timestamp`` minus ``freq`` to the current
            # ``Timestamp`` with a right close.
            if origin in ["end", "end_day"]:
                if closed is None:
                    closed = "right"
                if label is None:
                    label = "right"
            else:
                if closed is None:
                    closed = "left"
                if label is None:
                    label = "left"

        self.closed = closed
        self.label = label
        self.kind = kind

        self.convention = convention or "E"
        self.convention = self.convention.lower()

        self.how = how
        self.fill_method = fill_method
        self.limit = limit

        if origin in ("epoch", "start", "start_day", "end", "end_day"):
            self.origin = origin
        else:
            try:
                self.origin = Timestamp(origin)
            except (ValueError, TypeError) as err:
                raise ValueError(
                    "'origin' should be equal to 'epoch', 'start', 'start_day', "
                    "'end', 'end_day' or "
                    f"should be a Timestamp convertible type. Got '{origin}' instead."
                ) from err

        try:
            self.offset = Timedelta(offset) if offset is not None else None
        except (ValueError, TypeError) as err:
            raise ValueError(
                "'offset' should be a Timedelta convertible type. "
                f"Got '{offset}' instead."
            ) from err

        # always sort time groupers
        kwargs["sort"] = True

        # Handle deprecated arguments since v1.1.0 of `base` and `loffset` (GH #31809)
        if base is not None and offset is not None:
            raise ValueError("'offset' and 'base' cannot be present at the same time")

        if base and isinstance(freq, Tick):
            # this conversion handle the default behavior of base and the
            # special case of GH #10530. Indeed in case when dealing with
            # a TimedeltaIndex base was treated as a 'pure' offset even though
            # the default behavior of base was equivalent of a modulo on
            # freq_nanos.
            self.offset = Timedelta(base * freq.nanos // freq.n)

        if isinstance(loffset, str):
            loffset = to_offset(loffset)
        self.loffset = loffset

        super().__init__(freq=freq, axis=axis, **kwargs)
