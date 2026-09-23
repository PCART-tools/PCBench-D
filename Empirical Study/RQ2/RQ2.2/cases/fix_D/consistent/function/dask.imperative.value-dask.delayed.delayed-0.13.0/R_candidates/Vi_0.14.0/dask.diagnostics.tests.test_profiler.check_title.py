def check_title(p, title):
    # bokeh 0.12 changed the title attribute to not a string
    return getattr(p.title, 'text', p.title) == title
