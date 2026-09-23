    def to_gbq(self, destination_table, project_id, chunksize=None,
               verbose=None, reauth=False, if_exists='fail', private_key=None,
               auth_local_webserver=False, table_schema=None):
        """
        Write a DataFrame to a Google BigQuery table.

        This function requires the `pandas-gbq package
        <https://pandas-gbq.readthedocs.io>`__.

        Authentication to the Google BigQuery service is via OAuth 2.0.

        - If ``private_key`` is provided, the library loads the JSON service
          account credentials and uses those to authenticate.

        - If no ``private_key`` is provided, the library tries `application
          default credentials`_.

          .. _application default credentials:
              https://cloud.google.com/docs/authentication/production#providing_credentials_to_your_application

        - If application default credentials are not found or cannot be used
          with BigQuery, the library authenticates with user account
          credentials. In this case, you will be asked to grant permissions
          for product name 'pandas GBQ'.

        Parameters
        ----------
        destination_table : str
            Name of table to be written, in the form 'dataset.tablename'.
        project_id : str
            Google BigQuery Account project ID.
        chunksize : int, optional
            Number of rows to be inserted in each chunk from the dataframe.
            Set to ``None`` to load the whole dataframe at once.
        reauth : bool, default False
            Force Google BigQuery to reauthenticate the user. This is useful
            if multiple accounts are used.
        if_exists : str, default 'fail'
            Behavior when the destination table exists. Value can be one of:

            ``'fail'``
                If table exists, do nothing.
            ``'replace'``
                If table exists, drop it, recreate it, and insert data.
            ``'append'``
                If table exists, insert data. Create if does not exist.
        private_key : str, optional
            Service account private key in JSON format. Can be file path
            or string contents. This is useful for remote server
            authentication (eg. Jupyter/IPython notebook on remote host).
        auth_local_webserver : bool, default False
            Use the `local webserver flow`_ instead of the `console flow`_
            when getting user credentials.

            .. _local webserver flow:
                http://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow.run_local_server
            .. _console flow:
                http://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow.run_console

            *New in version 0.2.0 of pandas-gbq*.
        table_schema : list of dicts, optional
            List of BigQuery table fields to which according DataFrame
            columns conform to, e.g. ``[{'name': 'col1', 'type':
            'STRING'},...]``. If schema is not provided, it will be
            generated according to dtypes of DataFrame columns. See
            BigQuery API documentation on available names of a field.

            *New in version 0.3.1 of pandas-gbq*.
        verbose : boolean, deprecated
            *Deprecated in Pandas-GBQ 0.4.0.* Use the `logging module
            to adjust verbosity instead
            <https://pandas-gbq.readthedocs.io/en/latest/intro.html#logging>`__.

        See Also
        --------
        pandas_gbq.to_gbq : This function in the pandas-gbq library.
        pandas.read_gbq : Read a DataFrame from Google BigQuery.
        """
        from pandas.io import gbq
        return gbq.to_gbq(
            self, destination_table, project_id, chunksize=chunksize,
            verbose=verbose, reauth=reauth, if_exists=if_exists,
            private_key=private_key, auth_local_webserver=auth_local_webserver,
            table_schema=table_schema)
