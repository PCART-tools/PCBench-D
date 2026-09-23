    @final
    @doc(
        storage_options=_shared_docs["storage_options"],
        compression_options=_shared_docs["compression_options"] % "path_or_buf",
    )
    def to_json(
        self,
        path_or_buf: FilePath | WriteBuffer[bytes] | WriteBuffer[str] | None = None,
        orient: Literal["split", "records", "index", "table", "columns", "values"]
        | None = None,
        date_format: str | None = None,
        double_precision: int = 10,
        force_ascii: bool_t = True,
        date_unit: TimeUnit = "ms",
        default_handler: Callable[[Any], JSONSerializable] | None = None,
        lines: bool_t = False,
        compression: CompressionOptions = "infer",
        index: bool_t | None = None,
        indent: int | None = None,
        storage_options: StorageOptions | None = None,
        mode: Literal["a", "w"] = "w",
    ) -> str | None:
        """
        Convert the object to a JSON string.

        Note NaN's and None will be converted to null and datetime objects
        will be converted to UNIX timestamps.

        Parameters
        ----------
        path_or_buf : str, path object, file-like object, or None, default None
            String, path object (implementing os.PathLike[str]), or file-like
            object implementing a write() function. If None, the result is
            returned as a string.
        orient : str
            Indication of expected JSON string format.

            * Series:

                - default is 'index'
                - allowed values are: {{'split', 'records', 'index', 'table'}}.

            * DataFrame:

                - default is 'columns'
                - allowed values are: {{'split', 'records', 'index', 'columns',
                  'values', 'table'}}.

            * The format of the JSON string:

                - 'split' : dict like {{'index' -> [index], 'columns' -> [columns],
                  'data' -> [values]}}
                - 'records' : list like [{{column -> value}}, ... , {{column -> value}}]
                - 'index' : dict like {{index -> {{column -> value}}}}
                - 'columns' : dict like {{column -> {{index -> value}}}}
                - 'values' : just the values array
                - 'table' : dict like {{'schema': {{schema}}, 'data': {{data}}}}

                Describing the data, where data component is like ``orient='records'``.

        date_format : {{None, 'epoch', 'iso'}}
            Type of date conversion. 'epoch' = epoch milliseconds,
            'iso' = ISO8601. The default depends on the `orient`. For
            ``orient='table'``, the default is 'iso'. For all other orients,
            the default is 'epoch'.
        double_precision : int, default 10
            The number of decimal places to use when encoding
            floating point values. The possible maximal value is 15.
            Passing double_precision greater than 15 will raise a ValueError.
        force_ascii : bool, default True
            Force encoded string to be ASCII.
        date_unit : str, default 'ms' (milliseconds)
            The time unit to encode to, governs timestamp and ISO8601
            precision.  One of 's', 'ms', 'us', 'ns' for second, millisecond,
            microsecond, and nanosecond respectively.
        default_handler : callable, default None
            Handler to call if object cannot otherwise be converted to a
            suitable format for JSON. Should receive a single argument which is
            the object to convert and return a serialisable object.
        lines : bool, default False
            If 'orient' is 'records' write out line-delimited json format. Will
            throw ValueError if incorrect 'orient' since others are not
            list-like.
        {compression_options}

            .. versionchanged:: 1.4.0 Zstandard support.

        index : bool or None, default None
            The index is only used when 'orient' is 'split', 'index', 'column',
            or 'table'. Of these, 'index' and 'column' do not support
            `index=False`.

        indent : int, optional
           Length of whitespace used to indent each record.

        {storage_options}

            .. versionadded:: 1.2.0

        mode : str, default 'w' (writing)
            Specify the IO mode for output when supplying a path_or_buf.
            Accepted args are 'w' (writing) and 'a' (append) only.
            mode='a' is only supported when lines is True and orient is 'records'.

        Returns
        -------
        None or str
            If path_or_buf is None, returns the resulting json format as a
            string. Otherwise returns None.

        See Also
        --------
        read_json : Convert a JSON string to pandas object.

        Notes
        -----
        The behavior of ``indent=0`` varies from the stdlib, which does not
        indent the output but does insert newlines. Currently, ``indent=0``
        and the default ``indent=None`` are equivalent in pandas, though this
        may change in a future release.

        ``orient='table'`` contains a 'pandas_version' field under 'schema'.
        This stores the version of `pandas` used in the latest revision of the
        schema.

        Examples
        --------
        >>> from json import loads, dumps
        >>> df = pd.DataFrame(
        ...     [["a", "b"], ["c", "d"]],
        ...     index=["row 1", "row 2"],
        ...     columns=["col 1", "col 2"],
        ... )

        >>> result = df.to_json(orient="split")
        >>> parsed = loads(result)
        >>> dumps(parsed, indent=4)  # doctest: +SKIP
        {{
            "columns": [
                "col 1",
                "col 2"
            ],
            "index": [
                "row 1",
                "row 2"
            ],
            "data": [
                [
                    "a",
                    "b"
                ],
                [
                    "c",
                    "d"
                ]
            ]
        }}

        Encoding/decoding a Dataframe using ``'records'`` formatted JSON.
        Note that index labels are not preserved with this encoding.

        >>> result = df.to_json(orient="records")
        >>> parsed = loads(result)
        >>> dumps(parsed, indent=4)  # doctest: +SKIP
        [
            {{
                "col 1": "a",
                "col 2": "b"
            }},
            {{
                "col 1": "c",
                "col 2": "d"
            }}
        ]

        Encoding/decoding a Dataframe using ``'index'`` formatted JSON:

        >>> result = df.to_json(orient="index")
        >>> parsed = loads(result)
        >>> dumps(parsed, indent=4)  # doctest: +SKIP
        {{
            "row 1": {{
                "col 1": "a",
                "col 2": "b"
            }},
            "row 2": {{
                "col 1": "c",
                "col 2": "d"
            }}
        }}

        Encoding/decoding a Dataframe using ``'columns'`` formatted JSON:

        >>> result = df.to_json(orient="columns")
        >>> parsed = loads(result)
        >>> dumps(parsed, indent=4)  # doctest: +SKIP
        {{
            "col 1": {{
                "row 1": "a",
                "row 2": "c"
            }},
            "col 2": {{
                "row 1": "b",
                "row 2": "d"
            }}
        }}

        Encoding/decoding a Dataframe using ``'values'`` formatted JSON:

        >>> result = df.to_json(orient="values")
        >>> parsed = loads(result)
        >>> dumps(parsed, indent=4)  # doctest: +SKIP
        [
            [
                "a",
                "b"
            ],
            [
                "c",
                "d"
            ]
        ]

        Encoding with Table Schema:

        >>> result = df.to_json(orient="table")
        >>> parsed = loads(result)
        >>> dumps(parsed, indent=4)  # doctest: +SKIP
        {{
            "schema": {{
                "fields": [
                    {{
                        "name": "index",
                        "type": "string"
                    }},
                    {{
                        "name": "col 1",
                        "type": "string"
                    }},
                    {{
                        "name": "col 2",
                        "type": "string"
                    }}
                ],
                "primaryKey": [
                    "index"
                ],
                "pandas_version": "1.4.0"
            }},
            "data": [
                {{
                    "index": "row 1",
                    "col 1": "a",
                    "col 2": "b"
                }},
                {{
                    "index": "row 2",
                    "col 1": "c",
                    "col 2": "d"
                }}
            ]
        }}
        """
        from pandas.io import json

        if date_format is None and orient == "table":
            date_format = "iso"
        elif date_format is None:
            date_format = "epoch"

        config.is_nonnegative_int(indent)
        indent = indent or 0

        return json.to_json(
            path_or_buf=path_or_buf,
            obj=self,
            orient=orient,
            date_format=date_format,
            double_precision=double_precision,
            force_ascii=force_ascii,
            date_unit=date_unit,
            default_handler=default_handler,
            lines=lines,
            compression=compression,
            index=index,
            indent=indent,
            storage_options=storage_options,
            mode=mode,
        )
