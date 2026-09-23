    def to_gbq(self, destination_table, project_id=None, chunksize=None,
               reauth=False, if_exists='fail', auth_local_webserver=False,
               table_schema=None, location=None, progress_bar=True,
               credentials=None, verbose=None, private_key=None):
        """
        Write a DataFrame to a Google BigQuery table.

        This function requires the `pandas-gbq package
        <https://pandas-gbq.readthedocs.io>`__.

        See the `How to authenticate with Google BigQuery
        <https://pandas-gbq.readthedocs.io/en/latest/howto/authentication.html>`__
        guide for authentication instructions.

        Parameters
        ----------
        destination_table : str
            Name of table to be written, in the form ``dataset.tablename``.
        project_id : str, optional
            Google BigQuery Account project ID. Optional when available from
            the environment.
        chunksize : int, optional
            Number of rows to be inserted in each chunk from the dataframe.
            Set to ``None`` to load the whole dataframe at once.
        reauth : bool, default False
            Force Google BigQuery to re-authenticate the user. This is useful
            if multiple accounts are used.
        if_exists : str, default 'fail'
            Behavior when the destination table exists. Value can be one of:

            ``'fail'``
                If table exists, do nothing.
            ``'replace'``
                If table exists, drop it, recreate it, and insert data.
            ``'append'``
                If table exists, insert data. Create if does not exist.
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
        location : str, optional
            Location where the load job should run. See the `BigQuery locations
            documentation
            <https://cloud.google.com/bigquery/docs/dataset-locations>`__ for a
            list of available locations. The location must match that of the
            target dataset.

            *New in version 0.5.0 of pandas-gbq*.
        progress_bar : bool, default True
            Use the library `tqdm` to show the progress bar for the upload,
            chunk by chunk.

            *New in version 0.5.0 of pandas-gbq*.
        credentials : google.auth.credentials.Credentials, optional
            Credentials for accessing Google APIs. Use this parameter to
            override default credentials, such as to use Compute Engine
            :class:`google.auth.compute_engine.Credentials` or Service
            Account :class:`google.oauth2.service_account.Credentials`
            directly.

            *New in version 0.8.0 of pandas-gbq*.

            .. versionadded:: 0.24.0
        verbose : bool, deprecated
            Deprecated in pandas-gbq version 0.4.0. Use the `logging module
            to adjust verbosity instead
            <https://pandas-gbq.readthedocs.io/en/latest/intro.html#logging>`__.
        private_key : str, deprecated
            Deprecated in pandas-gbq version 0.8.0. Use the ``credentials``
            parameter and
            :func:`google.oauth2.service_account.Credentials.from_service_account_info`
            or
            :func:`google.oauth2.service_account.Credentials.from_service_account_file`
            instead.

            Service account private key in JSON format. Can be file path
            or string contents. This is useful for remote server
            authentication (eg. Jupyter/IPython notebook on remote host).

        See Also
        --------
        pandas_gbq.to_gbq : This function in the pandas-gbq library.
        pandas.read_gbq : Read a DataFrame from Google BigQuery.
        """
        from pandas.io import gbq
        return gbq.to_gbq(
            self, destination_table, project_id=project_id,
            chunksize=chunksize, reauth=reauth, if_exists=if_exists,
            auth_local_webserver=auth_local_webserver,
            table_schema=table_schema, location=location,
            progress_bar=progress_bar, credentials=credentials,
            verbose=verbose, private_key=private_key)
