def gen_pyi(native_yaml_path: str, deprecated_yaml_path: str, fm: FileManager) -> None:
    """gen_pyi()

    This function generates a pyi file for torch.
    """

    # Some of this logic overlaps with generate_python_signature in
    # tools/autograd/gen_python_functions.py; however, this
    # function is all about generating mypy type signatures, whereas
    # the other function generates are custom format for argument
    # checking.  If you are update this, consider if your change
    # also needs to update the other file.

    # Dictionary for NamedTuple definitions
    namedtuples: Dict[str, str] = {}

    # Generate type signatures for top-level functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    unsorted_function_hints: Dict[str, List[str]] = collections.defaultdict(list)
    unsorted_function_hints.update({
        'set_flush_denormal': ['def set_flush_denormal(mode: _bool) -> _bool: ...'],
        'get_default_dtype': ['def get_default_dtype() -> _dtype: ...'],
        'asarray': ['def asarray(obj: Any, *, dtype: Optional[_dtype]=None, '
                    'device: Union[_device, str, None]=None, copy: Optional[_bool]=None, '
                    'requires_grad: _bool=False) -> Tensor: ...'],
        'from_numpy': ['def from_numpy(ndarray) -> Tensor: ...'],
        'frombuffer': ['def frombuffer(buffer: Any, *, dtype: _dtype, count: int=-1, '
                       'offset: int=0, device: Union[_device, str, None]=None, '
                       'requires_grad: _bool=False) -> Tensor: ...'],
        'numel': ['def numel(self: Tensor) -> _int: ...'],
        'as_tensor': ["def as_tensor(data: Any, dtype: _dtype=None, device: Optional[_device]=None) -> Tensor: ..."],
        'get_num_threads': ['def get_num_threads() -> _int: ...'],
        'set_num_threads': ['def set_num_threads(num: _int) -> None: ...'],
        'init_num_threads': ['def init_num_threads() -> None: ...'],
        'get_num_interop_threads': ['def get_num_interop_threads() -> _int: ...'],
        'set_num_interop_threads': ['def set_num_interop_threads(num: _int) -> None: ...'],
        # These functions are explicitly disabled by
        # SKIP_PYTHON_BINDINGS because they are hand bound.
        # Correspondingly, we must hand-write their signatures.
        'tensor': ["def tensor(data: Any, {}) -> Tensor: ...".format(FACTORY_PARAMS)],
        'sparse_coo_tensor': ['def sparse_coo_tensor(indices: Tensor, values: Union[Tensor,List],'
                              ' size: Optional[_size]=None, *, dtype: Optional[_dtype]=None,'
                              ' device: Union[_device, str, None]=None, requires_grad:_bool=False) -> Tensor: ...'],
        'sparse_csr_tensor' : ['def sparse_csr_tensor(crow_indices: Union[Tensor, List],'
                               'col_indices: Union[Tensor, List],'
                               ' values: Union[Tensor, List], size: Optional[_size]=None,'
                               ' *, dtype: Optional[_dtype]=None,'
                               ' device: Union[_device, str, None]=None, requires_grad:_bool=False) -> Tensor: ...'],
        '_sparse_coo_tensor_unsafe': ['def _sparse_coo_tensor_unsafe(indices: Tensor, values: Tensor, size: List[int],'
                                      ' dtype: Optional[_dtype] = None, device: Optional[_device] = None,'
                                      ' requires_grad: bool = False) -> Tensor: ...'],
        '_sparse_csr_tensor_unsafe': ['def _sparse_csr_tensor_unsafe(crow_indices: Union[Tensor, List],'
                                      'col_indices: Union[Tensor, List],'
                                      ' values: Union[Tensor, List], size: List[int],'
                                      ' dtype: Optional[_dtype] = None, device: Optional[_device] = None,'
                                      ' requires_grad: bool = False) -> Tensor: ...'],
        'range': ['def range(start: Number, end: Number,'
                  ' step: Number=1, *, out: Optional[Tensor]=None, {}) -> Tensor: ...'
                  .format(FACTORY_PARAMS)],
        'arange': ['def arange(start: Number, end: Number, step: Number, *,'
                   ' out: Optional[Tensor]=None, {}) -> Tensor: ...'
                   .format(FACTORY_PARAMS),
                   'def arange(start: Number, end: Number, *, out: Optional[Tensor]=None, {}) -> Tensor: ...'
                   .format(FACTORY_PARAMS),
                   'def arange(end: Number, *, out: Optional[Tensor]=None, {}) -> Tensor: ...'
                   .format(FACTORY_PARAMS)],
        'linspace': ['def linspace(start: Number, end: Number, steps: Optional[_int]=None, *,'
                     ' out: Optional[Tensor]=None, {}) -> Tensor: ...'.format(FACTORY_PARAMS)],
        'logspace': ['def logspace(start: Number, end: Number, steps: Optional[_int]=None, base: _float=10.0, *,'
                     ' out: Optional[Tensor]=None, {}) -> Tensor: ...'.format(FACTORY_PARAMS)],
        'randint': ['def randint(low: _int, high: _int, size: _size, *,'
                    ' generator: Optional[Generator]=None, {}) -> Tensor: ...'
                    .format(FACTORY_PARAMS),
                    'def randint(high: _int, size: _size, *,'
                    ' generator: Optional[Generator]=None, {}) -> Tensor: ...'
                    .format(FACTORY_PARAMS)],
        'full': ['def full(size: _size, fill_value: Number, *,'
                 ' out: Optional[Tensor]=None,'
                 ' layout: _layout=strided, {}) -> Tensor: ...'
                 .format(FACTORY_PARAMS),
                 'def full(size: _size, fill_value: Number, *,'
                 ' names: List[Union[str, None]],'
                 ' layout: _layout=strided, {}) -> Tensor: ...'
                 .format(FACTORY_PARAMS)],
        'is_grad_enabled': ['def is_grad_enabled() -> _bool: ...'],
        'is_inference_mode_enabled': ['def is_inference_mode_enabled() -> _bool: ...'],
        'nonzero': ['def nonzero(input: Tensor, *, as_tuple: Literal[False]=False, out: Optional[Tensor]=None) -> Tensor: ...',
                    'def nonzero(input: Tensor, *, as_tuple: Literal[True]) -> Tuple[Tensor, ...]: ...'],
        'binary_cross_entropy_with_logits': ['def binary_cross_entropy_with_logits(input: Tensor, target: Tensor, '
                                             'weight: Optional[Tensor] = None, size_average: Optional[bool] = None, '
                                             'reduce: Optional[bool] = None, reduction: str = ..., '
                                             'pos_weight: Optional[Tensor] = None) -> Tensor: ...'],
        'cosine_embedding_loss': ['def cosine_embedding_loss(input1: Tensor, input2: Tensor, '
                                  'target: Tensor, margin: float = ..., size_average: Optional[bool] = ..., '
                                  'reduce: Optional[bool] = ..., reduction: str = ...) -> Tensor: ...'],
        'ctc_loss': ['def ctc_loss(log_probs: Tensor, targets: Tensor, input_lengths: Tensor, target_lengths: Tensor,'
                     ' blank: int = ..., reduction: str = ..., zero_infinity: bool = ...) -> Tensor: ...'],
        'hinge_embedding_loss': ['def hinge_embedding_loss(input: Tensor, target: Tensor, margin: float = ...,'
                                 ' size_average: Optional[bool] = ..., reduce: Optional[bool] = ..., '
                                 'reduction: str = ...) -> Tensor: ...'],
        'kl_div': ['def kl_div(input: Tensor, target: Tensor, size_average: Optional[bool] = ..., '
                   'reduce: Optional[bool] = ..., reduction: str = ..., log_target: bool = ...) -> Tensor: ...'],
        'margin_ranking_loss': ['def margin_ranking_loss(input1: Tensor, input2: Tensor, target: Tensor,'
                                ' margin: float = ..., size_average: Optional[bool] = ..., '
                                ' reduce: Optional[bool] = ..., reduction: str = ...) -> Tensor: ...'],
        'triplet_margin_loss': ['def triplet_margin_loss(anchor: Tensor, positive: Tensor, negative: Tensor, '
                                'margin: float = ..., p: float = ..., eps: float = ..., swap: bool = ..., '
                                'size_average: Optional[bool] = ..., '
                                'reduce: Optional[bool] = ..., reduction: str = ...) -> Tensor: ...'],
        'dsmm': ['def dsmm(input: Tensor, mat2: Tensor) -> Tensor: ...'],
        'hsmm': ['def hsmm(input: Tensor, mat2: Tensor) -> Tensor: ...'],
        'saddmm': ['def saddmm(input: Tensor, mat1: Tensor, mat2: Tensor, *, beta: Number=1, '
                   'alpha: Number=1, out: Optional[Tensor]=None) -> Tensor: ...'],
        'spmm': ['def spmm(input: Tensor, mat2: Tensor) -> Tensor: ...'],
        'div': ['def div(input: Union[Tensor, Number], other: Union[Tensor, Number], *, '
                'rounding_mode: Optional[str] = None, out: Optional[Tensor]=None) -> Tensor: ...'],
    })
    for binop in ['mul', 'true_divide', 'floor_divide']:
        unsorted_function_hints[binop].append(
            'def {}(input: Union[Tensor, Number],'
            ' other: Union[Tensor, Number],'
            ' *, out: Optional[Tensor]=None) -> Tensor: ...'.format(binop))
    for binop in ['add', 'sub']:
        unsorted_function_hints[binop].append(
            'def {}(input: Union[Tensor, Number],'
            ' other: Union[Tensor, Number],'
            ' *, alpha: Optional[Number]=1, out: Optional[Tensor]=None) -> Tensor: ...'.format(binop))

    native_functions = parse_native_yaml(native_yaml_path).native_functions
    native_functions = list(filter(should_generate_py_binding, native_functions))

    function_signatures = load_signatures(native_functions, deprecated_yaml_path, method=False, pyi=True)
    sig_groups = get_py_torch_functions(function_signatures)
    for group in sorted(sig_groups, key=lambda g: g.signature.name):
        name = group.signature.name
        unsorted_function_hints[name] += generate_type_hints(group)

        named_tuple = group.signature.returns.named_tuple_pyi()
        if named_tuple is not None and not group.signature.deprecated:
            # deprecated namedtuples are currently not included for torch functions
            tuple_name, tuple_def = named_tuple
            if tuple_name in namedtuples:
                assert namedtuples[tuple_name] == tuple_def
            else:
                namedtuples[tuple_name] = tuple_def

    function_hints = []
    for name, hints in sorted(unsorted_function_hints.items()):
        if len(hints) > 1:
            hints = ['@overload\n' + h for h in hints]
        function_hints += hints

    # Generate type signatures for Tensor methods
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    unsorted_tensor_method_hints: Dict[str, List[str]] = collections.defaultdict(list)
    unsorted_tensor_method_hints.update({
        'size': ['def size(self) -> Size: ...',
                 'def size(self, dim: _int) -> _int: ...'],
        'stride': ['def stride(self) -> Tuple[_int]: ...',
                   'def stride(self, _int) -> _int: ...'],
        'new_ones': ['def new_ones(self, size: _size, {}) -> Tensor: ...'.
                     format(FACTORY_PARAMS)],
        'new_tensor': ["def new_tensor(self, data: Any, {}) -> Tensor: ...".format(FACTORY_PARAMS)],
        # new and __init__ have the same signatures differ only in return type
        # Adapted from legacy_tensor_ctor and legacy_tensor_new
        'new': ['def new(self, *args: Any, {}) ->Tensor: ...'.format(DEVICE_PARAM),
                'def new(self, storage: Storage) -> Tensor: ...',
                'def new(self, other: Tensor) -> Tensor: ...',
                'def new(self, size: _size, *, {}) -> Tensor: ...'.format(DEVICE_PARAM),
                ],
        '__init__': ['def __init__(self, *args: Any, {}) -> None: ...'.format(DEVICE_PARAM),
                     'def __init__(self, storage: Storage) -> None: ...',
                     'def __init__(self, other: Tensor) -> None: ...',
                     'def __init__(self, size: _size, *, {}) -> None: ...'.format(DEVICE_PARAM),
                     ],
        'as_subclass': ["def as_subclass(self, cls: Tensor) -> Tensor: ..."],
        '_make_subclass': ["def _make_subclass(cls, data: Tensor, require_grad: _bool = False) -> Tensor: ..."],
        '__getitem__': ["def __getitem__(self, {}) -> Tensor: ...".format(INDICES)],
        '__setitem__': ["def __setitem__(self, {}, val: Union[Tensor, Number])"
                        " -> None: ...".format(INDICES)],
        'tolist': ['def tolist(self) -> List: ...'],
        'requires_grad_': ['def requires_grad_(self, mode: _bool=True) -> Tensor: ...'],
        'element_size': ['def element_size(self) -> _int: ...'],
        'data_ptr': ['def data_ptr(self) -> _int: ...'],
        'dim': ['def dim(self) -> _int: ...'],
        'nonzero': ['def nonzero(self, *, as_tuple: Literal[False]=False) -> Tensor: ...',
                    'def nonzero(self, *, as_tuple: Literal[True]) -> Tuple[Tensor, ...]: ...'],
        'numel': ['def numel(self) -> _int: ...'],
        'ndimension': ['def ndimension(self) -> _int: ...'],
        'nelement': ['def nelement(self) -> _int: ...'],
        'cuda': ['def cuda(self, device: Optional[Union[_device, _int, str]]=None, non_blocking: _bool=False) -> Tensor: ...'],
        'numpy': ['def numpy(self) -> Any: ...'],
        'apply_': ['def apply_(self, callable: Callable) -> Tensor: ...'],
        'map_': ['def map_(self, tensor: Tensor, callable: Callable) -> Tensor: ...'],
        'map2_': ['def map2_(self, x: Tensor, y: Tensor, callable: Callable) -> Tensor: ...'],
        'storage': ['def _storage(self) -> Storage: ...'],
        'storage_type': ['def storage_type(self) -> Storage: ...'],
        'type': ['def type(self, dtype: None=None, non_blocking: _bool=False) -> str: ...',
                 'def type(self, dtype: Union[str, _dtype], non_blocking: _bool=False) -> Tensor: ...',
                 ],
        'get_device': ['def get_device(self) -> _int: ...'],
        'contiguous': ['def contiguous(self, memory_format=torch.contiguous_format) -> Tensor: ...'],
        'has_names': ['def has_names(self) -> _bool: ...'],
        'is_contiguous': ['def is_contiguous(self, memory_format=torch.contiguous_format) -> _bool: ...'],
        '_is_view': ['def _is_view(self) -> _bool: ...'],
        'is_cuda': ['is_cuda: _bool'],
        'is_leaf': ['is_leaf: _bool'],
        'is_sparse': ['is_sparse: _bool'],
        'is_sparse_csr' : ['is_sparse_csr: _bool'],
        'is_quantized': ['is_quantized: _bool'],
        'is_meta': ['is_meta: _bool'],
        'is_ort': ['is_ort: _bool'],
        'is_mkldnn': ['is_mkldnn: _bool'],
        'is_vulkan': ['is_vulkan: _bool'],
        'storage_offset': ['def storage_offset(self) -> _int: ...'],
        'to': ['def to(self, dtype: _dtype, non_blocking: _bool=False, copy: _bool=False) -> Tensor: ...',
               'def to(self, device: Optional[Union[_device, str]]=None, dtype: Optional[_dtype]=None, '
               'non_blocking: _bool=False, copy: _bool=False) -> Tensor: ...',
               'def to(self, other: Tensor, non_blocking: _bool=False, copy: _bool=False) -> Tensor: ...',
               ],
        'item': ["def item(self) -> Number: ..."],
        'copy_': ["def copy_(self, src: Tensor, non_blocking: _bool=False) -> Tensor: ..."],
        'set_': ['def set_(self, storage: Union[Storage, _TypedStorage], offset: _int, size: _size, stride: _size) -> Tensor: ...',
                 'def set_(self, storage: Union[Storage, _TypedStorage]) -> Tensor: ...'],
        'split': ['def split(self, split_size: _int, dim: _int=0) -> Sequence[Tensor]: ...',
                  'def split(self, split_size: Tuple[_int, ...], dim: _int=0) -> Sequence[Tensor]: ...'],
        'div': ['def div(self, other: Union[Tensor, Number], *, rounding_mode: Optional[str] = None) -> Tensor: ...'],
        'div_': ['def div_(self, other: Union[Tensor, Number], *, rounding_mode: Optional[str] = None) -> Tensor: ...'],
    })
    for binop in ['mul', 'true_divide', 'floor_divide']:
        for inplace in [False, True]:
            out_suffix = ', *, out: Optional[Tensor]=None'
            if inplace:
                binop += '_'
                out_suffix = ''
            unsorted_tensor_method_hints[binop].append(
                'def {}(self, other: Union[Tensor, Number]{})'
                ' -> Tensor: ...'.format(binop, out_suffix))
    for binop in ['add', 'sub']:
        for inplace in [False, True]:
            out_suffix = ', out: Optional[Tensor]=None'
            if inplace:
                binop += '_'
                out_suffix = ''
            unsorted_tensor_method_hints[binop].append(
                'def {}(self, other: Union[Tensor, Number], '
                '*, alpha: Optional[Number]=1{})'
                ' -> Tensor: ...'.format(binop, out_suffix))
    simple_conversions = ['byte', 'char', 'cpu', 'double', 'float',
                          'half', 'int', 'long', 'short', 'bool',
                          'bfloat16']
    for name in simple_conversions:
        unsorted_tensor_method_hints[name].append('def {}(self) -> Tensor: ...'.format(name))

    # pyi tensor methods don't currently include deprecated signatures for some reason
    # TODO: we should probably add them in
    tensor_method_signatures = load_signatures(native_functions, deprecated_yaml_path, method=True, skip_deprecated=True, pyi=True)
    tensor_method_sig_groups = get_py_torch_functions(tensor_method_signatures, method=True)

    for group in sorted(tensor_method_sig_groups, key=lambda g: g.signature.name):
        name = group.signature.name
        unsorted_tensor_method_hints[name] += generate_type_hints(group)

        named_tuple = group.signature.returns.named_tuple_pyi()
        if named_tuple is not None and not group.signature.deprecated:
            # deprecated namedtuples are currently not included for torch functions
            tuple_name, tuple_def = named_tuple
            if tuple_name in namedtuples:
                assert namedtuples[tuple_name] == tuple_def
            else:
                namedtuples[tuple_name] = tuple_def

    for op in all_ops:
        name = '__{}__'.format(op)
        unsorted_tensor_method_hints[name] += sig_for_ops(name)

    tensor_method_hints = []
    for name, hints in sorted(unsorted_tensor_method_hints.items()):
        if len(hints) > 1:
            hints = ['@overload\n' + h for h in hints]
        tensor_method_hints += hints

    # TODO: Missing type hints for nn

    # Generate namedtuple definitions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    namedtuple_defs = ['{} = {}'.format(name, defn) for name, defn in namedtuples.items()]

    # Generate type signatures for legacy classes
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # TODO: These are deprecated, maybe we shouldn't type hint them
    legacy_storage_base_hints = []
    dt = ('Double', 'Float', 'Long', 'Int',
          'Short', 'Char', 'Byte', 'Bool',
          'Half', 'BFloat16', 'ComplexDouble',
          'ComplexFloat', 'QUInt8', 'QInt8', 'QInt32', 'QUInt4x2', 'QUInt2x4')
    for c in dt:
        legacy_storage_base_hints.append('class {}StorageBase(object): ...'.format(c))
    for c in dt:
        legacy_storage_base_hints.append('class Cuda{}StorageBase(object): ...'.format(c))

    legacy_class_hints = []
    for c in ('DoubleTensor', 'FloatTensor', 'LongTensor', 'IntTensor',
              'ShortTensor', 'HalfTensor', 'CharTensor', 'ByteTensor', 'BoolTensor'):
        legacy_class_hints.append('class {}(Tensor): ...'.format(c))

    # Generate type signatures for dtype classes
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # TODO: don't explicitly list dtypes here; get it from canonical
    # source
    dtype_class_hints = ['{}: dtype = ...'.format(n)
                         for n in
                         ['float32', 'float', 'float64', 'double', 'float16', 'bfloat16', 'half',
                          'uint8', 'int8', 'int16', 'short', 'int32', 'int', 'int64', 'long',
                          'complex64', 'cfloat', 'complex128', 'cdouble',
                          'quint8', 'qint8', 'qint32', 'bool', 'quint4x2', 'quint2x4']]

    # Generate __all__ directive
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Include only the functions that contain hints, to prevent undefined
    # symbols to be included in the `__all__` directive.
    hinted_function_names = [name for name, hint in unsorted_function_hints.items() if hint]
    all_symbols = sorted(list(namedtuples.keys()) + hinted_function_names)
    all_directive = pformat(all_symbols, width=100, compact=True).split('\n')
    all_directive[0] = '__all__ = {}'.format(all_directive[0])

    # Write out the stub
    # ~~~~~~~~~~~~~~~~~~

    env = {
        'namedtuple_defs': namedtuple_defs,
        'function_hints': function_hints,
        'tensor_method_hints': tensor_method_hints,
        'legacy_class_hints': legacy_class_hints,
        'legacy_storage_base_hints': legacy_storage_base_hints,
        'dtype_class_hints': dtype_class_hints,
        'all_directive': all_directive
    }
    fm.write_with_template('torch/_C/__init__.pyi', 'torch/_C/__init__.pyi.in', lambda: {
        'generated_comment': '@' + 'generated from torch/_C/__init__.pyi.in',
        **env,
    })
    fm.write_with_template('torch/_C/_VariableFunctions.pyi', 'torch/_C/_VariableFunctions.pyi.in', lambda: {
        'generated_comment': '@' + 'generated from torch/_C/_VariableFunctions.pyi.in',
        **env,
    })
    fm.write_with_template('torch/_VF.pyi', 'torch/_C/_VariableFunctions.pyi.in', lambda: {
        'generated_comment': '@' + 'generated from torch/_C/_VariableFunctions.pyi.in',
        **env,
    })
    gen_nn_functional(fm)
