def replace_extern_shared(input_string):
    """Match extern __shared__ type foo[]; syntax and use HIP_DYNAMIC_SHARED() MACRO instead.
       https://github.com/ROCm-Developer-Tools/HIP/blob/master/docs/markdown/hip_kernel_language.md#__shared__
    Example:
        "extern __shared__ char smemChar[];" => "HIP_DYNAMIC_SHARED( char, smemChar)"
        "extern __shared__ unsigned char smem[];" => "HIP_DYNAMIC_SHARED( unsigned char, my_smem)"
    """
    output_string = input_string
    output_string = RE_EXTERN_SHARED.sub(
        lambda inp: "HIP_DYNAMIC_SHARED({0} {1}, {2})".format(
            inp.group(1) or "", inp.group(2), inp.group(3)), output_string)

    return output_string
