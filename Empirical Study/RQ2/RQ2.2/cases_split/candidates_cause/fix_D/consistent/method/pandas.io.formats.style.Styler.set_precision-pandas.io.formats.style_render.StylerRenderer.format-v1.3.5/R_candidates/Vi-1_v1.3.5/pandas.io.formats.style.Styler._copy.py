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
          - hidden index state and hidden columns state (.hide_index_, .hide_columns_)
          - table_attributes
          - table_styles
          - applied styles (_todo)

        """
        # GH 40675
        styler = Styler(
            self.data,  # populates attributes 'data', 'columns', 'index' as shallow
            uuid_len=self.uuid_len,
        )
        shallow = [  # simple string or boolean immutables
            "hide_index_",
            "hide_columns_",
            "table_attributes",
            "cell_ids",
            "caption",
        ]
        deep = [  # nested lists or dicts
            "_display_funcs",
            "hidden_rows",
            "hidden_columns",
            "ctx",
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
