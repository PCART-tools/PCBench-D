def exportdb_error_message(case_name: str) -> str:
    return (
        "For more information about this error, see: "
        + "https://pytorch.org/docs/main/generated/exportdb/index.html#"
        + case_name.replace("_", "-")
    )
