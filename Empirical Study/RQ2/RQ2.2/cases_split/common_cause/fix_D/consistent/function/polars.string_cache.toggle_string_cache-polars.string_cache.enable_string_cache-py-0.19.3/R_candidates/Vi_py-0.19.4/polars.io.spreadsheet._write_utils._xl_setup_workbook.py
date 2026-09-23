def _xl_setup_workbook(
    workbook: Workbook | BytesIO | Path | str | None, worksheet: str | None = None
) -> tuple[Workbook, Worksheet, bool]:
    """Establish the target excel workbook and worksheet."""
    from xlsxwriter import Workbook

    if isinstance(workbook, Workbook):
        wb, can_close = workbook, False
        ws = wb.get_worksheet_by_name(name=worksheet)
    else:
        workbook_options = {
            "nan_inf_to_errors": True,
            "strings_to_formulas": False,
            "default_date_format": _XL_DEFAULT_DTYPE_FORMATS_[Date],
        }
        if isinstance(workbook, BytesIO):
            wb, ws, can_close = Workbook(workbook, workbook_options), None, True
        else:
            file = Path("dataframe.xlsx" if workbook is None else workbook)
            wb = Workbook(
                (file if file.suffix else file.with_suffix(".xlsx"))
                .expanduser()
                .resolve(strict=False),
                workbook_options,
            )
            ws, can_close = None, True

    if ws is None:
        ws = wb.add_worksheet(name=worksheet)
    return wb, ws, can_close
