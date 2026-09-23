    def __dataframe_consortium_standard__(
        self, *, api_version: str | None = None
    ) -> Any:
        """
        Provide entry point to the Consortium DataFrame Standard API.

        This is developed and maintained outside of pandas.
        Please report any issues to https://github.com/data-apis/dataframe-api-compat.
        """
        dataframe_api_compat = import_optional_dependency("dataframe_api_compat")
        convert_to_standard_compliant_dataframe = (
            dataframe_api_compat.pandas_standard.convert_to_standard_compliant_dataframe
        )
        return convert_to_standard_compliant_dataframe(self, api_version=api_version)
