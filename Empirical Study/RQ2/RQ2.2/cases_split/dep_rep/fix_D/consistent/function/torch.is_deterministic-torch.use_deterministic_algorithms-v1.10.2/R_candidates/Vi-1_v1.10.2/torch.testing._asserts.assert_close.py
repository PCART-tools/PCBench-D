def assert_close(
    actual: Any,
    expected: Any,
    *,
    allow_subclasses: bool = True,
    rtol: Optional[float] = None,
    atol: Optional[float] = None,
    equal_nan: bool = False,
    check_device: bool = True,
    check_dtype: bool = True,
    check_stride: bool = False,
    check_is_coalesced: bool = True,
    msg: Optional[Union[str, Callable[[Tensor, Tensor, Diagnostics], str]]] = None,
) -> None:
    r"""Asserts that :attr:`actual` and :attr:`expected` are close.

    If :attr:`actual` and :attr:`expected` are strided, non-quantized, real-valued, and finite, they are considered
    close if

    .. math::

        \lvert \text{actual} - \text{expected} \rvert \le \texttt{atol} + \texttt{rtol} \cdot \lvert \text{expected} \rvert

    and they have the same :attr:`~torch.Tensor.device` (if :attr:`check_device` is ``True``), same ``dtype`` (if
    :attr:`check_dtype` is ``True``), and the same stride (if :attr:`check_stride` is ``True``). Non-finite values
    (``-inf`` and ``inf``) are only considered close if and only if they are equal. ``NaN``'s are only considered equal
    to each other if :attr:`equal_nan` is ``True``.

    If :attr:`actual` and :attr:`expected` are sparse (either having COO or CSR layout), their strided members are
    checked individually. Indices, namely ``indices`` for COO or ``crow_indices``  and ``col_indices`` for CSR layout,
    are always checked for equality whereas the values are checked for closeness according to the definition above.
    Sparse COO tensors are only considered close if both are either coalesced or uncoalesced (if
    :attr:`check_is_coalesced` is ``True``).

    If :attr:`actual` and :attr:`expected` are quantized, they are considered close if they have the same
    :meth:`~torch.Tensor.qscheme` and the result of :meth:`~torch.Tensor.dequantize` is close according to the
    definition above.

    :attr:`actual` and :attr:`expected` can be :class:`~torch.Tensor`'s or any tensor-or-scalar-likes from which
    :class:`torch.Tensor`'s can be constructed with :func:`torch.as_tensor`. Except for Python scalars the input types
    have to be directly related. In addition, :attr:`actual` and :attr:`expected` can be
    :class:`~collections.abc.Sequence`'s or :class:`~collections.abc.Mapping`'s in which case they are considered close
    if their structure matches and all their elements are considered close according to the above definition.

    .. note::

        Python scalars are an exception to the type relation requirement, because their :func:`type`, i.e.
        :class:`int`, :class:`float`, and :class:`complex`, is equivalent to the ``dtype`` of a tensor-like. Thus,
        Python scalars of different types can be checked, but require :attr:`check_dtype` to be set to ``False``.

    Args:
        actual (Any): Actual input.
        expected (Any): Expected input.
        allow_subclasses (bool): If ``True`` (default) and except for Python scalars, inputs of directly related types
            are allowed. Otherwise type equality is required.
        rtol (Optional[float]): Relative tolerance. If specified :attr:`atol` must also be specified. If omitted,
            default values based on the :attr:`~torch.Tensor.dtype` are selected with the below table.
        atol (Optional[float]): Absolute tolerance. If specified :attr:`rtol` must also be specified. If omitted,
            default values based on the :attr:`~torch.Tensor.dtype` are selected with the below table.
        equal_nan (Union[bool, str]): If ``True``, two ``NaN`` values will be considered equal.
        check_device (bool): If ``True`` (default), asserts that corresponding tensors are on the same
            :attr:`~torch.Tensor.device`. If this check is disabled, tensors on different
            :attr:`~torch.Tensor.device`'s are moved to the CPU before being compared.
        check_dtype (bool): If ``True`` (default), asserts that corresponding tensors have the same ``dtype``. If this
            check is disabled, tensors with different ``dtype``'s are promoted  to a common ``dtype`` (according to
            :func:`torch.promote_types`) before being compared.
        check_stride (bool): If ``True`` and corresponding tensors are strided, asserts that they have the same stride.
        check_is_coalesced (bool): If ``True`` (default) and corresponding tensors are sparse COO, checks that both
            :attr:`actual` and :attr:`expected` are either coalesced or uncoalesced. If this check is disabled,
            tensors are :meth:`~torch.Tensor.coalesce`'ed before being compared.
        msg (Optional[Union[str, Callable[[Tensor, Tensor, Diagnostics], str]]]): Optional error message to use if the
            values of corresponding tensors mismatch. Can be passed as callable in which case it will be called with
            the mismatching tensors and a namespace of diagnostics about the mismatches. See below for details.

    Raises:
        ValueError: If no :class:`torch.Tensor` can be constructed from an input.
        ValueError: If only :attr:`rtol` or :attr:`atol` is specified.
        AssertionError: If corresponding inputs are not Python scalars and are not directly related.
        AssertionError: If :attr:`allow_subclasses` is ``False``, but corresponding inputs are not Python scalars and
            have different types.
        AssertionError: If the inputs are :class:`~collections.abc.Sequence`'s, but their length does not match.
        AssertionError: If the inputs are :class:`~collections.abc.Mapping`'s, but their set of keys do not match.
        AssertionError: If corresponding tensors do not have the same :attr:`~torch.Tensor.shape`.
        AssertionError: If corresponding tensors do not have the same :attr:`~torch.Tensor.layout`.
        AssertionError: If corresponding tensors are quantized, but have different :meth:`~torch.Tensor.qscheme`'s.
        AssertionError: If :attr:`check_device` is ``True``, but corresponding tensors are not on the same
            :attr:`~torch.Tensor.device`.
        AssertionError: If :attr:`check_dtype` is ``True``, but corresponding tensors do not have the same ``dtype``.
        AssertionError: If :attr:`check_stride` is ``True``, but corresponding strided tensors do not have the same
            stride.
        AssertionError: If :attr:`check_is_coalesced`  is ``True``, but corresponding sparse COO tensors are not both
            either coalesced or uncoalesced.
        AssertionError: If the values of corresponding tensors are not close according to the definition above.

    The following table displays the default ``rtol`` and ``atol`` for different ``dtype``'s. In case of mismatching
    ``dtype``'s, the maximum of both tolerances is used.

    +---------------------------+------------+----------+
    | ``dtype``                 | ``rtol``   | ``atol`` |
    +===========================+============+==========+
    | :attr:`~torch.float16`    | ``1e-3``   | ``1e-5`` |
    +---------------------------+------------+----------+
    | :attr:`~torch.bfloat16`   | ``1.6e-2`` | ``1e-5`` |
    +---------------------------+------------+----------+
    | :attr:`~torch.float32`    | ``1.3e-6`` | ``1e-5`` |
    +---------------------------+------------+----------+
    | :attr:`~torch.float64`    | ``1e-7``   | ``1e-7`` |
    +---------------------------+------------+----------+
    | :attr:`~torch.complex32`  | ``1e-3``   | ``1e-5`` |
    +---------------------------+------------+----------+
    | :attr:`~torch.complex64`  | ``1.3e-6`` | ``1e-5`` |
    +---------------------------+------------+----------+
    | :attr:`~torch.complex128` | ``1e-7``   | ``1e-7`` |
    +---------------------------+------------+----------+
    | other                     | ``0.0``    | ``0.0``  |
    +---------------------------+------------+----------+

    The namespace of diagnostics that will be passed to :attr:`msg` if its a callable has the following attributes:

    - ``number_of_elements`` (int): Number of elements in each tensor being compared.
    - ``total_mismatches`` (int): Total number of mismatches.
    - ``max_abs_diff`` (Union[int, float]): Greatest absolute difference of the inputs.
    - ``max_abs_diff_idx`` (Union[int, Tuple[int, ...]]): Index of greatest absolute difference.
    - ``atol`` (float): Allowed absolute tolerance.
    - ``max_rel_diff`` (Union[int, float]): Greatest relative difference of the inputs.
    - ``max_rel_diff_idx`` (Union[int, Tuple[int, ...]]): Index of greatest relative difference.
    - ``rtol`` (float): Allowed relative tolerance.

    For ``max_abs_diff`` and ``max_rel_diff`` the type depends on the :attr:`~torch.Tensor.dtype` of the inputs.

    .. note::

        :func:`~torch.testing.assert_close` is highly configurable with strict default settings. Users are encouraged
        to :func:`~functools.partial` it to fit their use case. For example, if an equality check is needed, one might
        define an ``assert_equal`` that uses zero tolrances for every ``dtype`` by default:

        >>> import functools
        >>> assert_equal = functools.partial(torch.testing.assert_close, rtol=0, atol=0)
        >>> assert_equal(1e-9, 1e-10)
        Traceback (most recent call last):
        ...
        AssertionError: Scalars are not equal!
        <BLANKLINE>
        Absolute difference: 8.999999703829253e-10
        Relative difference: 8.999999583666371

    Examples:
        >>> # tensor to tensor comparison
        >>> expected = torch.tensor([1e0, 1e-1, 1e-2])
        >>> actual = torch.acos(torch.cos(expected))
        >>> torch.testing.assert_close(actual, expected)

        >>> # scalar to scalar comparison
        >>> import math
        >>> expected = math.sqrt(2.0)
        >>> actual = 2.0 / math.sqrt(2.0)
        >>> torch.testing.assert_close(actual, expected)

        >>> # numpy array to numpy array comparison
        >>> import numpy as np
        >>> expected = np.array([1e0, 1e-1, 1e-2])
        >>> actual = np.arccos(np.cos(expected))
        >>> torch.testing.assert_close(actual, expected)

        >>> # sequence to sequence comparison
        >>> import numpy as np
        >>> # The types of the sequences do not have to match. They only have to have the same
        >>> # length and their elements have to match.
        >>> expected = [torch.tensor([1.0]), 2.0, np.array(3.0)]
        >>> actual = tuple(expected)
        >>> torch.testing.assert_close(actual, expected)

        >>> # mapping to mapping comparison
        >>> from collections import OrderedDict
        >>> import numpy as np
        >>> foo = torch.tensor(1.0)
        >>> bar = 2.0
        >>> baz = np.array(3.0)
        >>> # The types and a possible ordering of mappings do not have to match. They only
        >>> # have to have the same set of keys and their elements have to match.
        >>> expected = OrderedDict([("foo", foo), ("bar", bar), ("baz", baz)])
        >>> actual = {"baz": baz, "bar": bar, "foo": foo}
        >>> torch.testing.assert_close(actual, expected)

        >>> expected = torch.tensor([1.0, 2.0, 3.0])
        >>> actual = expected.clone()
        >>> # By default, directly related instances can be compared
        >>> torch.testing.assert_close(torch.nn.Parameter(actual), expected)
        >>> # This check can be made more strict with allow_subclasses=False
        >>> torch.testing.assert_close(
        ...     torch.nn.Parameter(actual), expected, allow_subclasses=False
        ... )
        Traceback (most recent call last):
        ...
        AssertionError: Except for Python scalars, type equality is required if
        allow_subclasses=False, but got <class 'torch.nn.parameter.Parameter'> and
        <class 'torch.Tensor'> instead.
        >>> # If the inputs are not directly related, they are never considered close
        >>> torch.testing.assert_close(actual.numpy(), expected)
        Traceback (most recent call last):
        ...
        AssertionError: Except for Python scalars, input types need to be directly
        related, but got <class 'numpy.ndarray'> and <class 'torch.Tensor'> instead.
        >>> # Exceptions to these rules are Python scalars. They can be checked regardless of
        >>> # their type if check_dtype=False.
        >>> torch.testing.assert_close(1.0, 1, check_dtype=False)

        >>> # NaN != NaN by default.
        >>> expected = torch.tensor(float("Nan"))
        >>> actual = expected.clone()
        >>> torch.testing.assert_close(actual, expected)
        Traceback (most recent call last):
        ...
        AssertionError: Scalars are not close!
        <BLANKLINE>
        Absolute difference: nan (up to 1e-05 allowed)
        Relative difference: nan (up to 1.3e-06 allowed)
        >>> torch.testing.assert_close(actual, expected, equal_nan=True)

        >>> expected = torch.tensor([1.0, 2.0, 3.0])
        >>> actual = torch.tensor([1.0, 4.0, 5.0])
        >>> # The default mismatch message can be overwritten.
        >>> torch.testing.assert_close(actual, expected, msg="Argh, the tensors are not close!")
        Traceback (most recent call last):
        ...
        AssertionError: Argh, the tensors are not close!
        >>> # The error message can also created at runtime by passing a callable.
        >>> def custom_msg(actual, expected, diagnostics):
        ...     ratio = diagnostics.total_mismatches / diagnostics.number_of_elements
        ...     return (
        ...         f"Argh, we found {diagnostics.total_mismatches} mismatches! "
        ...         f"That is {ratio:.1%}!"
        ...     )
        >>> torch.testing.assert_close(actual, expected, msg=custom_msg)
        Traceback (most recent call last):
        ...
        AssertionError: Argh, we found 2 mismatches! That is 66.7%!
    """
    # Hide this function from `pytest`'s traceback
    __tracebackhide__ = True

    if (rtol is None) ^ (atol is None):
        # We require both tolerance to be omitted or specified, because specifying only one might lead to surprising
        # results. Imagine setting atol=0.0 and the tensors still match because rtol>0.0.
        raise ValueError(
            f"Both 'rtol' and 'atol' must be either specified or omitted, "
            f"but got no {'rtol' if rtol is None else 'atol'}.",
        )

    error_meta, pair = _parse_inputs(actual, expected, allow_subclasses=allow_subclasses)
    if error_meta:
        raise error_meta.to_error()
    else:
        pair = cast(Union[_TensorPair, List, Dict], pair)

    error_meta = _check_pair_close(
        pair,
        rtol=rtol,
        atol=atol,
        equal_nan=equal_nan,
        check_device=check_device,
        check_dtype=check_dtype,
        check_stride=check_stride,
        check_is_coalesced=check_is_coalesced,
        msg=msg,
    )
    if error_meta:
        raise error_meta.to_error()
