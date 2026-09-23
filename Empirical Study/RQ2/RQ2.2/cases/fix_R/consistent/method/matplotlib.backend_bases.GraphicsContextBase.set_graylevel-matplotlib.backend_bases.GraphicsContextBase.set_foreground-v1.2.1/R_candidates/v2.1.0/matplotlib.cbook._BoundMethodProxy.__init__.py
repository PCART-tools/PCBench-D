    def __init__(self, cb):
        self._hash = hash(cb)
        self._destroy_callbacks = []
        try:
            try:
                if six.PY3:
                    self.inst = ref(cb.__self__, self._destroy)
                else:
                    self.inst = ref(cb.im_self, self._destroy)
            except TypeError:
                self.inst = None
            if six.PY3:
                self.func = cb.__func__
                self.klass = cb.__self__.__class__
            else:
                self.func = cb.im_func
                self.klass = cb.im_class
        except AttributeError:
            self.inst = None
            self.func = cb
            self.klass = None
