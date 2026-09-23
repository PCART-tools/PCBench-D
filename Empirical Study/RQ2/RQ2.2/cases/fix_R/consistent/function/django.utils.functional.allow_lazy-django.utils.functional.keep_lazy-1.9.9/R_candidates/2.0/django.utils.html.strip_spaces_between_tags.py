@keep_lazy_text
def strip_spaces_between_tags(value):
    """Return the given HTML with spaces between tags removed."""
    return re.sub(r'>\s+<', '><', force_text(value))
