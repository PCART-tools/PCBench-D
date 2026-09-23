def persistent_mm_options(mat1, mat2):
    res = dict(
        A_ROW_MAJOR=not mat1.layout.is_transposed(),
        B_ROW_MAJOR=not mat2.layout.is_transposed(),
        NUM_SMS=get_num_sms(),
        TMA_SIZE=TMA_DESCRIPTOR_SIZE,
    )
    res.update(tma_options())
    return res
