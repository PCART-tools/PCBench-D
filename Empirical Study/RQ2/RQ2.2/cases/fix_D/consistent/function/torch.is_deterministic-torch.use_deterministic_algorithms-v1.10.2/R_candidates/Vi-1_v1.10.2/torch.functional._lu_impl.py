def _lu_impl(A, pivot=True, get_infos=False, out=None):
    # type: (Tensor, bool, bool, Any) -> Tuple[Tensor, Tensor, Tensor]
    r"""Computes the LU factorization of a matrix or batches of matrices
    :attr:`A`. Returns a tuple containing the LU factorization and
    pivots of :attr:`A`.  Pivoting is done if :attr:`pivot` is set to
    ``True``.

    .. note::
        * The pivots returned by the function are 1-indexed. If :attr:`pivot`
          is ``False``, then the returned pivots is a tensor filled with
          zeros of the appropriate size.
        * LU factorization with :attr:`pivot` = ``False`` is not available
          for CPU, and attempting to do so will throw an error. However,
          LU factorization with :attr:`pivot` = ``False`` is available for
          CUDA.
        * This function does not check if the factorization was successful
          or not if :attr:`get_infos` is ``True`` since the status of the
          factorization is present in the third element of the return tuple.
        * In the case of batches of square matrices with size less or equal
          to 32 on a CUDA device, the LU factorization is repeated for
          singular matrices due to the bug in the MAGMA library
          (see magma issue 13).
        * ``L``, ``U``, and ``P`` can be derived using :func:`torch.lu_unpack`.

    .. warning::
        The gradients of this function will only be finite when :attr:`A` is full rank.
        This is because the LU decomposition is just differentiable at full rank matrices.
        Furthermore, if :attr:`A` is close to not being full rank,
        the gradient will be numerically unstable as it depends on the computation of :math:`L^{-1}` and :math:`U^{-1}`.

    Args:
        A (Tensor): the tensor to factor of size :math:`(*, m, n)`
        pivot (bool, optional): controls whether pivoting is done. Default: ``True``
        get_infos (bool, optional): if set to ``True``, returns an info IntTensor.
                                    Default: ``False``
        out (tuple, optional): optional output tuple. If :attr:`get_infos` is ``True``,
                               then the elements in the tuple are Tensor, IntTensor,
                               and IntTensor. If :attr:`get_infos` is ``False``, then the
                               elements in the tuple are Tensor, IntTensor. Default: ``None``

    Returns:
        (Tensor, IntTensor, IntTensor (optional)): A tuple of tensors containing

            - **factorization** (*Tensor*): the factorization of size :math:`(*, m, n)`

            - **pivots** (*IntTensor*): the pivots of size :math:`(*, \text{min}(m, n))`.
              ``pivots`` stores all the intermediate transpositions of rows.
              The final permutation ``perm`` could be reconstructed by
              applying ``swap(perm[i], perm[pivots[i] - 1])`` for ``i = 0, ..., pivots.size(-1) - 1``,
              where ``perm`` is initially the identity permutation of :math:`m` elements
              (essentially this is what :func:`torch.lu_unpack` is doing).

            - **infos** (*IntTensor*, *optional*): if :attr:`get_infos` is ``True``, this is a tensor of
              size :math:`(*)` where non-zero values indicate whether factorization for the matrix or
              each minibatch has succeeded or failed

    Example::

        >>> A = torch.randn(2, 3, 3)
        >>> A_LU, pivots = torch.lu(A)
        >>> A_LU
        tensor([[[ 1.3506,  2.5558, -0.0816],
                 [ 0.1684,  1.1551,  0.1940],
                 [ 0.1193,  0.6189, -0.5497]],

                [[ 0.4526,  1.2526, -0.3285],
                 [-0.7988,  0.7175, -0.9701],
                 [ 0.2634, -0.9255, -0.3459]]])
        >>> pivots
        tensor([[ 3,  3,  3],
                [ 3,  3,  3]], dtype=torch.int32)
        >>> A_LU, pivots, info = torch.lu(A, get_infos=True)
        >>> if info.nonzero().size(0) == 0:
        ...   print('LU factorization succeeded for all samples!')
        LU factorization succeeded for all samples!
    """
    # If get_infos is True, then we don't need to check for errors and vice versa
    return torch._lu_with_info(A, pivot=pivot, check_errors=(not get_infos))
