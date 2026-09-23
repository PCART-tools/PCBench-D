    def write_style(self) -> None:
        style = """\
            <style>
            .dataframe > thead > tr,
            .dataframe > tbody > tr {
              text-align: right;
              white-space: pre-wrap;
            }
            </style>
        """
        self.write(dedent(style))
