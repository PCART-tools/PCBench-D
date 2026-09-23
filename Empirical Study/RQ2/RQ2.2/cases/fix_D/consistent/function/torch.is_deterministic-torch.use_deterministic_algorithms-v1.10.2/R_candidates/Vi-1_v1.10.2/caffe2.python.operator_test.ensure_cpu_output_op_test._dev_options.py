@st.composite
def _dev_options(draw):
    op_dev = draw(st.sampled_from(hu.device_options))
    if op_dev == hu.cpu_do:
        # the CPU op can only handle CPU tensor
        input_blob_dev = hu.cpu_do
    else:
        input_blob_dev = draw(st.sampled_from(hu.device_options))

    return op_dev, input_blob_dev
