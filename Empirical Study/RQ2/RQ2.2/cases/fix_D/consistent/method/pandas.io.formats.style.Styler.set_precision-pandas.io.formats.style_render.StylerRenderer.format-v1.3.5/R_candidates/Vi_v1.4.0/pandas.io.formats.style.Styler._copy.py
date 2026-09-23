    def _copy(self, deepcopy: bool = False) -> Styler:
        """
        Copies a Styler, allowing for deepcopy or shallow copy

        Copying a Styler aims to recreate a new Styler object which contains the same
        data and styles as the original.

        Data dependent attributes [copied and NOT exported]:
          - formatting (._display_funcs)
          - hidden index values or column values (.hidden_rows, .hidden_columns)
          - tooltips
          - cell_context (cell css classes)
          - ctx (cell css styles)
          - caption

        Non-data dependent attributes [copied and exported]:
          - css
          - hidden index state and hidden columns state (.hide_index_, .hide_columns_)
          - table_attributes
          - table_styles
          - applied styles (_todo)

        """
        # GH 40675
        styler = Styler(
            self.data,  # populates attributes 'data', 'columns', 'index' as shallow
        )
        shallow = [  # simple string or boolean immutables
            "hide_index_",
            "hide_columns_",
            "hide_column_names",
            "hide_index_names",
            "table_attributes",
            "cell_ids",
            "caption",
            "uuid",
            "uuid_len",
            "template_latex",  # also copy templates if these have been customised
            "template_html_style",
            "template_html_table",
            "template_html",
        ]
        deep = [  # nested lists or dicts
            "css",
            "_display_funcs",
            "_display_funcs_index",
            "_display_funcs_columns",
            "hidden_rows",
            "hidden_columns",
            "ctx",
            "ctx_index",
            "ctx_columns",
            "cell_context",
            "_todo",
            "table_styles",
            "tooltips",
        ]

        for attr in shallow:
            setattr(styler, attr, getattr(self, attr))

        for attr in deep:
            val = getattr(self, attr)
            setattr(styler, attr, copy.deepcopy(val) if deepcopy else val)

        return styler
