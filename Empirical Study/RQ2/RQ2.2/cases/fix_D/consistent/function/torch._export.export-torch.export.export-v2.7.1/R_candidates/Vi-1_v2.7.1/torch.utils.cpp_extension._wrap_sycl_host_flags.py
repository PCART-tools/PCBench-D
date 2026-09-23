def _wrap_sycl_host_flags(cflags):
    host_cxx = get_cxx_compiler()
    host_cflags = [
        f'-fsycl-host-compiler={host_cxx}',
        shlex.quote(f'-fsycl-host-compiler-options={cflags}'),
    ]
    return host_cflags
