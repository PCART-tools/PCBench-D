    def __init__(self, *args, **kwargs):
        kwargs['name'] = '_order'
        kwargs['editable'] = False
        super(OrderWrt, self).__init__(*args, **kwargs)
