@_add_docstr(
    r"""
Computes the general cosine window.

The general cosine window is defined as follows:

.. math::
    w_n = \sum^{M-1}_{i=0} (-1)^i a_i \cos{ \left( \frac{2 \pi i n}{M - 1}\right)}
    """,
    r"""

{normalization}

Arguments:
    {M}

Keyword args:
    a (Iterable): the coefficients associated to each of the cosine functions.
    {sym}
    {dtype}
    {layout}
    {device}
    {requires_grad}

Examples::

    >>> # Generates a symmetric general cosine window with 3 coefficients.
    >>> torch.signal.windows.general_cosine(10, a=[0.46, 0.23, 0.31], sym=True)
    tensor([0.5400, 0.3376, 0.1288, 0.4200, 0.9136, 0.9136, 0.4200, 0.1288, 0.3376, 0.5400])

    >>> # Generates a periodic general cosine window with 2 coefficients.
    >>> torch.signal.windows.general_cosine(10, a=[0.5, 1 - 0.5], sym=False)
    tensor([0.0000, 0.0955, 0.3455, 0.6545, 0.9045, 1.0000, 0.9045, 0.6545, 0.3455, 0.0955])
""".format(
        **window_common_args
    ),
)
def general_cosine(
    M,
    *,
    a: Iterable,
    sym: bool = True,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[torch.device] = None,
    requires_grad: bool = False,
) -> Tensor:
    if dtype is None:
        dtype = torch.get_default_dtype()

    _window_function_checks("general_cosine", M, dtype, layout)

    if M == 0:
        return torch.empty(
            (0,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    if M == 1:
        return torch.ones(
            (1,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    if not isinstance(a, Iterable):
        raise TypeError("Coefficients must be a list/tuple")

    if not a:
        raise ValueError("Coefficients cannot be empty")

    constant = 2 * torch.pi / (M if not sym else M - 1)

    k = torch.linspace(
        start=0,
        end=(M - 1) * constant,
        steps=M,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )

    a_i = torch.tensor(
        [(-1) ** i * w for i, w in enumerate(a)],
        device=device,
        dtype=dtype,
        requires_grad=requires_grad,
    )
    i = torch.arange(
        a_i.shape[0],
        dtype=a_i.dtype,
        device=a_i.device,
        requires_grad=a_i.requires_grad,
    )
    return (a_i.unsqueeze(-1) * torch.cos(i.unsqueeze(-1) * k)).sum(0)
