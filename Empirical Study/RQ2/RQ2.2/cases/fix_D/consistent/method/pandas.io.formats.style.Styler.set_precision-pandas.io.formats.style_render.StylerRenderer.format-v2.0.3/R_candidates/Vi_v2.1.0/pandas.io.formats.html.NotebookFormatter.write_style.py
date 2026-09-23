    def write_style(self) -> None:
        # We use the "scoped" attribute here so that the desired
        # style properties for the data frame are not then applied
        # throughout the entire notebook.
        template_first = """\
            <style scoped>"""
        template_last = """\
            </style>"""
        template_select = """\
                .dataframe %s {
                    %s: %s;
                }"""
        element_props = [
            ("tbody tr th:only-of-type", "vertical-align", "middle"),
            ("tbody tr th", "vertical-align", "top"),
        ]
        if isinstance(self.columns, MultiIndex):
            element_props.append(("thead tr th", "text-align", "left"))
            if self.show_row_idx_names:
                element_props.append(
                    ("thead tr:last-of-type th", "text-align", "right")
                )
        else:
            element_props.append(("thead th", "text-align", "right"))
        template_mid = "\n\n".join(template_select % t for t in element_props)
        template = dedent("\n".join((template_first, template_mid, template_last)))
        self.write(template)
