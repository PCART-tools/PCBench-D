    def to_gbq(self, destination_table, project_id=None, chunksize=10000,
               verbose=True, reauth=False):
        """Write a DataFrame to a Google BigQuery table.

        THIS IS AN EXPERIMENTAL LIBRARY

        If the table exists, the dataframe will be written to the table using
        the defined table schema and column types. For simplicity, this method
        uses the Google BigQuery streaming API. The to_gbq method chunks data
        into a default chunk size of 10,000. Failures return the complete error
        response which can be quite long depending on the size of the insert.
        There are several important limitations of the Google streaming API
        which are detailed at:
        https://developers.google.com/bigquery/streaming-data-into-bigquery.

        Parameters
        ----------
        dataframe : DataFrame
            DataFrame to be written
        destination_table : string
            Name of table to be written, in the form 'dataset.tablename'
        project_id : str
            Google BigQuery Account project ID.
        chunksize : int (default 10000)
            Number of rows to be inserted in each chunk from the dataframe.
        verbose : boolean (default True)
            Show percentage complete
        reauth : boolean (default False)
            Force Google BigQuery to reauthenticate the user. This is useful
            if multiple accounts are used.

        """

        from pandas.io import gbq
        return gbq.to_gbq(self, destination_table, project_id=project_id,
                          chunksize=chunksize, verbose=verbose,
                          reauth=reauth)
