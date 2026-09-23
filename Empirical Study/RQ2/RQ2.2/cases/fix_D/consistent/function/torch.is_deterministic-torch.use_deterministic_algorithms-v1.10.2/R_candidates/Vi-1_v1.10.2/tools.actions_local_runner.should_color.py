def should_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
