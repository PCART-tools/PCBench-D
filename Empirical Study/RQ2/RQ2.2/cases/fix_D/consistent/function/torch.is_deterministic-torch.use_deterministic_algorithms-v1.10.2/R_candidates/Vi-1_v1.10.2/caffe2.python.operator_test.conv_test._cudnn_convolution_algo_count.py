def _cudnn_convolution_algo_count(direction):
    try:
        if direction == "fwd":
            return st.integers(0, C.cudnn_convolution_fwd_algo_count - 1)
        elif direction == "dgrad":
            return st.integers(0, C.cudnn_convolution_bwd_data_algo_count - 1)
        elif direction == "wgrad":
            return st.integers(0, C.cudnn_convolution_bwd_filter_algo_count - 1)
        else:
            assert False
    except Exception:
        return st.sampled_from([-1])
