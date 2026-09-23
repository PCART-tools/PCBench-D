@_add_docstr(
    r"""
Computes the Hamming window.

The Hamming window is defined as follows:

.. math::
    w_n = \alpha - \beta\ \cos \left( \frac{2 \pi n}{M - 1} \right)
    """,
    r"""

{normalization}

Arguments:
    {M}

Keyword args:
    {sym}
    alpha (float, optional): The coefficient :math:`\alpha` in the equation above.
    beta (float, optional): The coefficient :math:`\beta` in the equation above.
    {dtype}
    {layout}
    {device}
    {requires_grad}

Examples::

    >>> # Generates a symmetric Hamming window.
    >>> torch.signal.windows.hamming(10)
    tensor([0.0800, 0.1876, 0.4601, 0.7700, 0.9723, 0.9723, 0.7700, 0.4601, 0.1876, 0.0800])

    >>> # Generates a periodic Hamming window.
    >>> torch.signal.windows.hamming(10, sym=False)
    tensor([0.0800, 0.1679, 0.3979, 0.6821, 0.9121, 1.0000, 0.9121, 0.6821, 0.3979, 0.1679])
""".format(
        **window_common_args
    ),
)
def hamming(
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
        sym=sym,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )
