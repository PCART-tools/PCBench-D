def get_float32_precision():
    if (
        torch.get_float32_matmul_precision() == "highest"
        or torch.version.hip
        or torch.mtia.is_available()
    ):
        return "'ieee'"
    else:
        return "'tf32'"
