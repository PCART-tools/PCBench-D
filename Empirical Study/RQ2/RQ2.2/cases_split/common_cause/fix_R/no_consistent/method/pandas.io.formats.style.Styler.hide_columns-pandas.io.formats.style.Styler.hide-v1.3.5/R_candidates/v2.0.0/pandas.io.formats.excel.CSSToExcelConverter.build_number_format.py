    def build_number_format(self, props: Mapping[str, str]) -> dict[str, str | None]:
        fc = props.get("number-format")
        fc = fc.replace("§", ";") if isinstance(fc, str) else fc
        return {"format_code": fc}
