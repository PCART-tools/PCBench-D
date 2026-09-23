    @unstable()
    def to_torch(
        self,
        return_type: TorchExportType = "tensor",
        *,
        label: str | Expr | Sequence[str | Expr] | None = None,
        features: str | Expr | Sequence[str | Expr] | None = None,
        dtype: PolarsDataType | None = None,
    ) -> torch.Tensor | dict[str, torch.Tensor] | PolarsDataset:
        """
        Convert DataFrame to a PyTorch Tensor, Dataset, or dict of Tensors.

        .. versionadded:: 0.20.23

        .. warning::
            This functionality is currently considered **unstable**. It may be
            changed at any point without it being considered a breaking change.

        Parameters
        ----------
        return_type : {"tensor", "dataset", "dict"}
            Set return type; a PyTorch Tensor, PolarsDataset (a frame-specialized
            TensorDataset), or dict of Tensors.
        label
            One or more column names, expressions, or selectors that label the feature
            data; when `return_type` is "dataset", the PolarsDataset will return
            `(features, label)` tensor tuples for each row. Otherwise, it returns
            `(features,)` tensor tuples where the feature contains all the row data.
        features
            One or more column names, expressions, or selectors that contain the feature
            data; if omitted, all columns that are not designated as part of the label
            are used.
        dtype
            Unify the dtype of all returned tensors; this casts any column that is
            not of the required dtype before converting to Tensor. This includes
            the label column *unless* the label is an expression (such as
            `pl.col("label_column").cast(pl.Int16)`).

        See Also
        --------
        to_dummies
        to_jax
        to_numpy

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "lbl": [0, 1, 2, 3],
        ...         "feat1": [1, 0, 0, 1],
        ...         "feat2": [1.5, -0.5, 0.0, -2.25],
        ...     }
        ... )

        Standard return type (Tensor), with f32 supertype:

        >>> df.to_torch(dtype=pl.Float32)
        tensor([[ 0.0000,  1.0000,  1.5000],
                [ 1.0000,  0.0000, -0.5000],
                [ 2.0000,  0.0000,  0.0000],
                [ 3.0000,  1.0000, -2.2500]])

        As a dictionary of individual Tensors:

        >>> df.to_torch("dict")
        {'lbl': tensor([0, 1, 2, 3]),
         'feat1': tensor([1, 0, 0, 1]),
         'feat2': tensor([ 1.5000, -0.5000,  0.0000, -2.2500], dtype=torch.float64)}

        As a "label" and "features" dictionary; note that as "features" is not
        declared, it defaults to all the columns that are not in "label":

        >>> df.to_torch("dict", label="lbl", dtype=pl.Float32)
        {'label': tensor([[0.],
                 [1.],
                 [2.],
                 [3.]]),
         'features': tensor([[ 1.0000,  1.5000],
                 [ 0.0000, -0.5000],
                 [ 0.0000,  0.0000],
                 [ 1.0000, -2.2500]])}

        As a PolarsDataset, with f64 supertype:

        >>> ds = df.to_torch("dataset", dtype=pl.Float64)
        >>> ds[3]
        (tensor([ 3.0000,  1.0000, -2.2500], dtype=torch.float64),)
        >>> ds[:2]
        (tensor([[ 0.0000,  1.0000,  1.5000],
                 [ 1.0000,  0.0000, -0.5000]], dtype=torch.float64),)
        >>> ds[[0, 3]]
        (tensor([[ 0.0000,  1.0000,  1.5000],
                 [ 3.0000,  1.0000, -2.2500]], dtype=torch.float64),)

        As a convenience the PolarsDataset can opt in to half-precision data
        for experimentation (usually this would be set on the model/pipeline):

        >>> list(ds.half())
        [(tensor([0.0000, 1.0000, 1.5000], dtype=torch.float16),),
         (tensor([ 1.0000,  0.0000, -0.5000], dtype=torch.float16),),
         (tensor([2., 0., 0.], dtype=torch.float16),),
         (tensor([ 3.0000,  1.0000, -2.2500], dtype=torch.float16),)]

        Pass PolarsDataset to a DataLoader, designating the label:

        >>> from torch.utils.data import DataLoader
        >>> ds = df.to_torch("dataset", label="lbl")
        >>> dl = DataLoader(ds, batch_size=2)
        >>> batches = list(dl)
        >>> batches[0]
        [tensor([[ 1.0000,  1.5000],
                 [ 0.0000, -0.5000]], dtype=torch.float64), tensor([0, 1])]

        Note that labels can be given as expressions, allowing them to have
        a dtype independent of the feature columns (multi-column labels are
        supported).

        >>> ds = df.to_torch(
        ...     return_type="dataset",
        ...     dtype=pl.Float32,
        ...     label=pl.col("lbl").cast(pl.Int16),
        ... )
        >>> ds[:2]
        (tensor([[ 1.0000,  1.5000],
                 [ 0.0000, -0.5000]]), tensor([0, 1], dtype=torch.int16))

        Easily integrate with (for example) scikit-learn and other datasets:

        >>> from sklearn.datasets import fetch_california_housing  # doctest: +SKIP
        >>> housing = fetch_california_housing()  # doctest: +SKIP
        >>> df = pl.DataFrame(
        ...     data=housing.data,
        ...     schema=housing.feature_names,
        ... ).with_columns(
        ...     Target=housing.target,
        ... )  # doctest: +SKIP
        >>> train = df.to_torch("dataset", label="Target")  # doctest: +SKIP
        >>> loader = DataLoader(
        ...     train,
        ...     shuffle=True,
        ...     batch_size=64,
        ... )  # doctest: +SKIP
        """
        if return_type not in ("dataset", "dict") and (
            label is not None or features is not None
        ):
            msg = "`label` and `features` only apply when `return_type` is 'dataset' or 'dict'"
            raise ValueError(msg)
        elif return_type == "dict" and label is None and features is not None:
            msg = "`label` is required if setting `features` when `return_type='dict'"
            raise ValueError(msg)

        torch = import_optional("torch")

        if dtype in (UInt16, UInt32, UInt64):
            msg = f"PyTorch does not support u16, u32, or u64 dtypes; given {dtype}"
            raise ValueError(msg)
        else:
            to_dtype = dtype or {UInt16: Int32, UInt32: Int64, UInt64: Int64}
            frame = self.cast(to_dtype)  # type: ignore[arg-type]

        if return_type == "tensor":
            # note: torch tensors are not immutable, so we must consider them writable
            return torch.from_numpy(frame.to_numpy(writable=True))

        elif return_type == "dict":
            if label is not None:
                # return a {"label": tensor(s), "features": tensor(s)} dict
                label_frame = frame.select(label)
                features_frame = (
                    frame.select(features)
                    if features is not None
                    else frame.drop(*label_frame.columns)
                )
                return {
                    "label": label_frame.to_torch(),
                    "features": features_frame.to_torch(),
                }
            else:
                # return a {"col": tensor} dict
                return {srs.name: srs.to_torch() for srs in frame}

        elif return_type == "dataset":
            # return a torch Dataset object
            from polars.ml.torch import PolarsDataset

            return PolarsDataset(frame, label=label, features=features)
        else:
            valid_torch_types = ", ".join(get_args(TorchExportType))
            msg = f"invalid `return_type`: {return_type!r}\nExpected one of: {valid_torch_types}"
            raise ValueError(msg)
