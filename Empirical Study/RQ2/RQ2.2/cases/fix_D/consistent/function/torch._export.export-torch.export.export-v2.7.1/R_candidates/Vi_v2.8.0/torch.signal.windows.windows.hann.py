@_add_docstr(
    r"""
Computes the Hann window.

The Hann window is defined as follows:

.. math::
    w_n = \frac{1}{2}\ \left[1 - \cos \left( \frac{2 \pi n}{M - 1} \right)\right] =
    \sin^2 \left( \frac{\pi n}{M - 1} \right)
    """,
    r"""

{normalization}

Arguments:
    {M}

Keyword args:
    {sym}
    {dtype}
    {layout}
    {device}
    {requires_grad}

Examples::

    >>> # Generates a symmetric Hann window.
    >>> torch.signal.windows.hann(10)
    tensor([0.0000, 0.1170, 0.4132, 0.7500, 0.9698, 0.9698, 0.7500, 0.4132, 0.1170, 0.0000])

    >>> # Generates a periodic Hann window.
    >>> torch.signal.windows.hann(10, sym=False)
    tensor([0.0000, 0.0955, 0.3455, 0.6545, 0.9045, 1.0000, 0.9045, 0.6545, 0.3455, 0.0955])
""".format(
        **window_common_args
    ),
)
def hann(
    M: int,
    *,
    sym: bool = True,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[torch.device] = None,
    requires_grad: bool = False,
) -> Tensor:
    return general_hamming(
        M,
        alpha=0.5,
        sym=sym,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )
