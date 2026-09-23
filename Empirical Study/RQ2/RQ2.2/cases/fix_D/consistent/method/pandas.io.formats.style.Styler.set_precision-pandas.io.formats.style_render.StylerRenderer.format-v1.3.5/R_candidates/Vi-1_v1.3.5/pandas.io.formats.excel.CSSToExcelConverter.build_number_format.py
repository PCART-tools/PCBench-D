    def build_number_format(self, props: Mapping[str, str]) -> dict[str, str | None]:
        return {"format_code": props.get("number-format")}
