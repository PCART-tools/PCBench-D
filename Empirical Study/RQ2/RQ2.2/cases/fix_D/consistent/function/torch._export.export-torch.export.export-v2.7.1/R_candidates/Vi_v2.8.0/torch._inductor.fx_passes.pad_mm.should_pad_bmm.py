def should_pad_bmm(match: Match) -> bool:
    mat1, mat2 = fetch_fake_tensors(match, ("mat1", "mat2"))
    return should_pad_common(mat1, mat2) and should_pad_bench(
        match, mat1, mat2, torch.ops.aten.bmm
    )
