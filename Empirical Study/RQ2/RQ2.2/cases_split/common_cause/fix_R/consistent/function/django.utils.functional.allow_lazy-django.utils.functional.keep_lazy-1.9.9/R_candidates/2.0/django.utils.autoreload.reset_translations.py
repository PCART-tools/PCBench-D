def reset_translations():
    import gettext
    from django.utils.translation import trans_real
    gettext._translations = {}
    trans_real._translations = {}
    trans_real._default = None
    trans_real._active = threading.local()
