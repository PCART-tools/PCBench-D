def _get_glibcxx_abi_build_flags():
    glibcxx_abi_cflags = ['-D_GLIBCXX_USE_CXX11_ABI=' + str(int(torch._C._GLIBCXX_USE_CXX11_ABI))]
    return glibcxx_abi_cflags
