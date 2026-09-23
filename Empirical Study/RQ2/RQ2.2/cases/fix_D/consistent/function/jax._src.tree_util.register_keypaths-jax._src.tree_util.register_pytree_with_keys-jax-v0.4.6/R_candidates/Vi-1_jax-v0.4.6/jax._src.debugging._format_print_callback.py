def _format_print_callback(fmt: str, *args, **kwargs):
  sys.stdout.write(fmt.format(*args, **kwargs) + "\n")
