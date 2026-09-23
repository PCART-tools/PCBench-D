    def __dataframe_consortium_standard__(
        self, *, api_version: str | None = None
    ) -> Any:
        """
        Provide entry point to the Consortium DataFrame Standard API.

        This is developed and maintained outside of polars.
        Please report any issues to https://github.com/data-apis/dataframe-api-compat.
        """
        return dataframe_api_compat.polars_standard.convert_to_standard_compliant_dataframe(
            self.lazy(), api_version=api_version
        )
