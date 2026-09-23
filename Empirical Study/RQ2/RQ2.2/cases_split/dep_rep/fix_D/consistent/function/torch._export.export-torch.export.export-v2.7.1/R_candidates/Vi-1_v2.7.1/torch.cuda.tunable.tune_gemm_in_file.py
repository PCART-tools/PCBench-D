def tune_gemm_in_file(filename: str) -> None:
    r"""tune GEMM in file."""

    assert is_enabled()
    assert tuning_is_enabled()

    deviceid = torch.cuda.current_device()

    with open(filename) as file:
        for line in file:
            if line.startswith(("Gemm", "ScaledGemm")):
                _process_single_offline_gemm(line, deviceid)
