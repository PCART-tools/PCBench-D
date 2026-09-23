@delayed
def _to_csv_chunk(df, **kwargs):
    import io
    if PY2:
        out = io.BytesIO()
    else:
        out = io.StringIO()
    df.to_csv(out, **kwargs)
    out.seek(0)
    if PY2:
        return out.getvalue()
    encoding = kwargs.get('encoding', sys.getdefaultencoding())
    return out.getvalue().encode(encoding)
