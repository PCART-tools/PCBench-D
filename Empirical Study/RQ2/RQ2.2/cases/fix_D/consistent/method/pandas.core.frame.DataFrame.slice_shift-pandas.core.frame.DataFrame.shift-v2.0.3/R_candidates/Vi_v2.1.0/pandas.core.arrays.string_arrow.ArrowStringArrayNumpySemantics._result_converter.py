    @classmethod
    def _result_converter(cls, values, na=None):
        if not isna(na):
            values = values.fill_null(bool(na))
        return ArrowExtensionArray(values).to_numpy(na_value=np.nan)
