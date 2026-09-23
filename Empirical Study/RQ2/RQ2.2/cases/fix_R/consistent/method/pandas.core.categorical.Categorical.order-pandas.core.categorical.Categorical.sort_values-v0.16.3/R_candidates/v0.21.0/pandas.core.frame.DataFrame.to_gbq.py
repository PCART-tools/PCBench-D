    def to_gbq(self, destination_table, project_id, chunksize=10000,
               verbose=True, reauth=False, if_exists='fail', private_key=None):
        """Write a DataFrame to a Google BigQuery table.

        The main method a user calls to export pandas DataFrame contents to
        Google BigQuery table.

        Google BigQuery API Client Library v2 for Python is used.
        Documentation is available `here
        <https://developers.google.com/api-client-library/python/apis/bigquery/v2>`__

        Authentication to the Google BigQuery service is via OAuth 2.0.

        - If "private_key" is not provided:

          By default "application default credentials" are used.

          If default application credentials are not found or are restrictive,
          user account credentials are used. In this case, you will be asked to
          grant permissions for product name 'pandas GBQ'.

        - If "private_key" is provided:

          Service account credentials will be used to authenticate.

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
        if_exists : {'fail', 'replace', 'append'}, default 'fail'
            'fail': If table exists, do nothing.
            'replace': If table exists, drop it, recreate it, and insert data.
            'append': If table exists, insert data. Create if does not exist.
        private_key : str (optional)
            Service account private key in JSON format. Can be file path
            or string contents. This is useful for remote server
            authentication (eg. jupyter iPython notebook on remote host)
        """

        from pandas.io import gbq
        return gbq.to_gbq(self, destination_table, project_id=project_id,
                          chunksize=chunksize, verbose=verbose, reauth=reauth,
                          if_exists=if_exists, private_key=private_key)
