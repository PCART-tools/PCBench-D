    def __init__(
        self,
        data: FrameOrSeriesUnion,
        precision: int | None = None,
        table_styles: CSSStyles | None = None,
        uuid: str | None = None,
        caption: str | tuple | None = None,
        table_attributes: str | None = None,
        cell_ids: bool = True,
        na_rep: str | None = None,
        uuid_len: int = 5,
        decimal: str = ".",
        thousands: str | None = None,
        escape: str | None = None,
    ):
        super().__init__(
            data=data,
            uuid=uuid,
            uuid_len=uuid_len,
            table_styles=table_styles,
            table_attributes=table_attributes,
            caption=caption,
            cell_ids=cell_ids,
        )

        # validate ordered args
        self.precision = precision  # can be removed on set_precision depr cycle
        self.na_rep = na_rep  # can be removed on set_na_rep depr cycle
        self.format(
            formatter=None,
            precision=precision,
            na_rep=na_rep,
            escape=escape,
            decimal=decimal,
            thousands=thousands,
        )
