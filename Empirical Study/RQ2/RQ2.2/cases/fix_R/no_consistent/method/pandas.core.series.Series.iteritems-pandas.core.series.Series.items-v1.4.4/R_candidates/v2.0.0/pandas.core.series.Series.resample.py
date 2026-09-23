    @doc(NDFrame.resample, **_shared_doc_kwargs)  # type: ignore[has-type]
    def resample(
        self,
        rule,
        axis: Axis = 0,
        closed: str | None = None,
        label: str | None = None,
        convention: str = "start",
        kind: str | None = None,
        on: Level = None,
        level: Level = None,
        origin: str | TimestampConvertibleTypes = "start_day",
        offset: TimedeltaConvertibleTypes | None = None,
        group_keys: bool = False,
    ) -> Resampler:
        return super().resample(
            rule=rule,
            axis=axis,
            closed=closed,
            label=label,
            convention=convention,
            kind=kind,
            on=on,
            level=level,
            origin=origin,
            offset=offset,
            group_keys=group_keys,
        )
