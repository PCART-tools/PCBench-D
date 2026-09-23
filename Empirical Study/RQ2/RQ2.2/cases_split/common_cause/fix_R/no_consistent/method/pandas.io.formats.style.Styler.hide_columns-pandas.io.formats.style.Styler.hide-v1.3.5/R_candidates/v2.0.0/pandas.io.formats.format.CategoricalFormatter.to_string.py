    def to_string(self) -> str:
        categorical = self.categorical

        if len(categorical) == 0:
            if self.footer:
                return self._get_footer()
            else:
                return ""

        fmt_values = self._get_formatted_values()

        fmt_values = [i.strip() for i in fmt_values]
        values = ", ".join(fmt_values)
        result = ["[" + values + "]"]
        if self.footer:
            footer = self._get_footer()
            if footer:
                result.append(footer)

        return str("\n".join(result))
