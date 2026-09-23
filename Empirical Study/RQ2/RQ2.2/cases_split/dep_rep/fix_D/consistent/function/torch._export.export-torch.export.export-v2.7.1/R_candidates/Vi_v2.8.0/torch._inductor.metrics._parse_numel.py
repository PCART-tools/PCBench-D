def _parse_numel(proper_kernel_fn_code: str, numel_arg_name: str) -> Optional[int]:
    m = re.search(f"{numel_arg_name} = ([\\d]+)", proper_kernel_fn_code)
    if m:
        return int(m.group(1))
    else:
        return None
