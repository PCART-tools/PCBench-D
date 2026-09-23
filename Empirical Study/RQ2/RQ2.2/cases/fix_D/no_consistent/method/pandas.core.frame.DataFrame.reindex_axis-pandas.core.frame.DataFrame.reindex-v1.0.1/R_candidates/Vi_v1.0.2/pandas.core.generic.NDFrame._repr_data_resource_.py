    def _repr_data_resource_(self):
        """
        Not a real Jupyter special repr method, but we use the same
        naming convention.
        """
        if config.get_option("display.html.table_schema"):
            data = self.head(config.get_option("display.max_rows"))
            payload = json.loads(
                data.to_json(orient="table"), object_pairs_hook=collections.OrderedDict
            )
            return payload
