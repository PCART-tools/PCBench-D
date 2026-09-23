    @Appender(_shared_docs["transform"] % dict(axis="", **_shared_doc_kwargs))
    def transform(self, func, *args, **kwargs):
        result = self.agg(func, *args, **kwargs)
        if is_scalar(result) or len(result) != len(self):
            raise ValueError("transforms cannot produce " "aggregated results")

        return result
