    @unstable()
    def to_jax(
        self,
        return_type: JaxExportType = "array",
        *,
        device: jax.Device | str | None = None,
        label: str | Expr | Sequence[str | Expr] | None = None,
        features: str | Expr | Sequence[str | Expr] | None = None,
        dtype: PolarsDataType | None = None,
        order: IndexOrder = "fortran",
    ) -> jax.Array | dict[str, jax.Array]:
        """
        Convert DataFrame to a Jax Array, or dict of Jax Arrays.

        .. versionadded:: 0.20.27

        .. warning::
            This functionality is currently considered **unstable**. It may be
            changed at any point without it being considered a breaking change.

        Parameters
        ----------
        return_type : {"array", "dict"}
            Set return type; a Jax Array, or dict of Jax Arrays.
        device
            Specify the jax `Device` on which the array will be created; can provide
            a string (such as "cpu", "gpu", or "tpu") in which case the device is
            retrieved as `jax.devices(string)[0]`. For more specific control you
            can supply the instantiated `Device` directly. If None, arrays are
            created on the default device.
        label
            One or more column names, expressions, or selectors that label the feature
            data; results in a `{"label": ..., "features": ...}` dict being returned
            when `return_type` is "dict" instead of a `{"col": array, }` dict.
        features
            One or more column names, expressions, or selectors that contain the feature
            data; if omitted, all columns that are not designated as part of the label
            are used. Only applies when `return_type` is "dict".
        dtype
            Unify the dtype of all returned arrays; this casts any column that is
            not already of the required dtype before converting to Array. Note that
            export will be single-precision (32bit) unless the Jax config/environment
            directs otherwise (eg: "jax_enable_x64" was set True in the config object
            at startup, or "JAX_ENABLE_X64" is set to "1" in the environment).
        order : {"c", "fortran"}
            The index order of the returned Jax array, either C-like (row-major) or
            Fortran-like (column-major).

        See Also
        --------
        to_dummies
        to_numpy
        to_torch

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "lbl": [0, 1, 2, 3],
        ...         "feat1": [1, 0, 0, 1],
        ...         "feat2": [1.5, -0.5, 0.0, -2.25],
        ...     }
        ... )

        Standard return type (2D Array), on the standard device:

        >>> df.to_jax()
        Array([[ 0.  ,  1.  ,  1.5 ],
               [ 1.  ,  0.  , -0.5 ],
               [ 2.  ,  0.  ,  0.  ],
               [ 3.  ,  1.  , -2.25]], dtype=float32)

        Create the Array on the default GPU device:

        >>> a = df.to_jax(device="gpu")  # doctest: +SKIP
        >>> a.device()  # doctest: +SKIP
        GpuDevice(id=0, process_index=0)

        Create the Array on a specific GPU device:

        >>> gpu_device = jax.devices("gpu")[1])  # doctest: +SKIP
        >>> a = df.to_jax(device=gpu_device)  # doctest: +SKIP
        >>> a.device()  # doctest: +SKIP
        GpuDevice(id=1, process_index=0)

        As a dictionary of individual Arrays:

        >>> df.to_jax("dict")
        {'lbl': Array([0, 1, 2, 3], dtype=int32),
         'feat1': Array([1, 0, 0, 1], dtype=int32),
         'feat2': Array([ 1.5 , -0.5 ,  0.  , -2.25], dtype=float32)}

        As a "label" and "features" dictionary; note that as "features" is not
        declared, it defaults to all the columns that are not in "label":

        >>> df.to_jax("dict", label="lbl")
        {'label': Array([[0],
                [1],
                [2],
                [3]], dtype=int32),
         'features': Array([[ 1.  ,  1.5 ],
                [ 0.  , -0.5 ],
                [ 0.  ,  0.  ],
                [ 1.  , -2.25]], dtype=float32)}

        As a "label" and "features" dictionary where each is designated using
        a col or selector expression (which can also be used to cast the data
        if the label and features are better-represented with different dtypes):

        >>> import polars.selectors as cs
        >>> df.to_jax(
        ...     return_type="dict",
        ...     features=cs.float(),
        ...     label=pl.col("lbl").cast(pl.UInt8),
        ... )
        {'label': Array([[0],
                [1],
                [2],
                [3]], dtype=uint8),
         'features': Array([[ 1.5 ],
                [-0.5 ],
                [ 0.  ],
                [-2.25]], dtype=float32)}
        """
        if return_type != "dict" and (label is not None or features is not None):
            msg = "`label` and `features` only apply when `return_type` is 'dict'"
            raise ValueError(msg)
        elif return_type == "dict" and label is None and features is not None:
            msg = "`label` is required if setting `features` when `return_type='dict'"
            raise ValueError(msg)

        jx = import_optional(
            "jax",
            install_message="Please see `https://jax.readthedocs.io/en/latest/installation.html` "
            "for specific installation recommendations for the Jax package",
        )
        enabled_double_precision = jx.config.jax_enable_x64 or bool(
            int(os.environ.get("JAX_ENABLE_X64", "0"))
        )
        if dtype:
            frame = self.cast(dtype)
        elif not enabled_double_precision:
            # enforce single-precision unless environment/config directs otherwise
            frame = self.cast({Float64: Float32, Int64: Int32, UInt64: UInt32})
        else:
            frame = self

        if isinstance(device, str):
            device = jx.devices(device)[0]

        with contextlib.nullcontext() if device is None else jx.default_device(device):
            if return_type == "array":
                return jx.numpy.asarray(
                    # note: jax arrays are immutable, so can avoid a copy (vs torch)
                    a=frame.to_numpy(writable=False, order=order),
                    order="K",
                )
            elif return_type == "dict":
                if label is not None:
                    # return a {"label": array(s), "features": array(s)} dict
                    label_frame = frame.select(label)
                    features_frame = (
                        frame.select(features)
                        if features is not None
                        else frame.drop(*label_frame.columns)
                    )
                    return {
                        "label": label_frame.to_jax(),
                        "features": features_frame.to_jax(),
                    }
                else:
                    # return a {"col": array} dict
                    return {srs.name: srs.to_jax() for srs in frame}
            else:
                valid_jax_types = ", ".join(get_args(JaxExportType))
                msg = f"invalid `return_type`: {return_type!r}\nExpected one of: {valid_jax_types}"
                raise ValueError(msg)
