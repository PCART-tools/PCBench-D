def get_verbose_code_part(code_part: str, guard: Guard) -> str:
    extra = ""
    if guard is not None:
        if guard.user_stack:
            for fs in reversed(guard.user_stack):
                if fs.filename not in uninteresting_files():
                    extra = f"  # {format_frame(fs, line=True)}"
                    break
        elif guard.stack:
            extra = f"  # {format_frame(guard.stack.summary()[-1])}"
    return f"{code_part:<60}{extra}"
