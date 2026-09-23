def _nvtx_range_pop():
    """If PyTorch is installed with CUDA support, this terminates NVTX range.

    Check torch.cuda.nvtx.range_pop's document for more details.
    """
    if torch.cuda.is_available():
        torch.cuda.nvtx.range_pop()
