from __future__ import annotations

import ast
import re
import copy
import textwrap
import warnings
from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple

from zss import Node, simple_distance

_API_DEF_RE = re.compile(r"(?:async\s+def|def|class)\b")
# =========================
# 数据结构
# =========================

@dataclass(frozen=True)
class APITree:
    """
    表示用于相似度计算的轻量树节点。

    参数:
        label: 当前树节点的标签，例如 'FunctionDef:foo'、'If'、'Call'。
        children: 当前节点的子节点元组。
    """
    label: str
    children: Tuple["APITree", ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class BuiltTree:
    """
    表示一次树构建后的聚合结果。

    参数:
        zss_node: 供 zss.simple_distance 使用的树节点。
        size: 当前树的节点总数。
        api_tree: 可选的 APITree。仅在需要 detail 大对象时保留。
    """
    zss_node: Node
    size: int
    api_tree: Optional[APITree] = None


@dataclass(frozen=True)
class BuiltClassRepresentation:
    """
    表示类级 API 的分层比较表示。

    说明：
        class 不再整体构造成一棵巨大的 zss 树做 TED，
        而是拆成类头部、类属性集合、方法集合和匹配方法树。
        函数/方法本身的 BuiltTree 构建逻辑保持不变。

    参数:
        header_tree: 类头部小树，包含类名、父类、类关键字和类装饰器。
        class_attributes: 直接定义在 class body 下的类属性名集合。
        methods: 方法名到方法 BuiltTree 的映射。
        size: 类级表示的统计规模，仅用于 meta / detail 展示。
    """
    header_tree: BuiltTree
    class_attributes: FrozenSet[str]
    methods: Dict[str, BuiltTree]
    size: int


CLASS_HEADER_WEIGHT = 0.15
CLASS_ATTRIBUTE_WEIGHT = 0.10
CLASS_METHOD_SET_WEIGHT = 0.15
CLASS_MATCHED_METHOD_WEIGHT = 0.60


# =========================
# 对外主接口
# =========================

def build_representation(src: str, keep_api_tree: bool = False) -> Dict[str, Any]:
    """
    对单个 API 源码做预处理并构建可复用表示。

    说明:
        - callable API 仍然构造成单棵 BuiltTree，保持原有函数级 TED 逻辑不变
        - class API 改为分层表示，避免整棵 class AST 直接进入 zss.simple_distance
        - 返回结果可直接供 similarity_from_representation /
          detail_from_representation 复用

    参数:
        src: 单个 API 源码字符串。
        keep_api_tree: 是否同时保留 APITree，大多数比较场景无需开启。

    返回:
        表示字典，包含算法名、API 类型、规范化源码和内部表示。
    """
    normalized_source = normalize_source(src)
    api_node = preprocess_api_node(normalized_source)
    api_kind = get_api_kind(api_node)

    if isinstance(api_node, ast.ClassDef):
        # 类属性名需要保留原始绑定名，因此额外解析一份未做局部绑定归一化的 class AST。
        # 方法树仍然基于 api_node 构建，保持函数/方法内部归一化逻辑不变。
        raw_api_node = parse_api_node(normalized_source)
        remove_docstrings_inplace(raw_api_node)
        built = build_class_representation(
            raw_node=raw_api_node,
            normalized_node=api_node,
            keep_api_tree=keep_api_tree,
        )
        tree_size = built.size
        has_api_tree = keep_api_tree
    else:
        built = build_comparison_tree(api_node, keep_api_tree=keep_api_tree)
        tree_size = built.size
        has_api_tree = built.api_tree is not None

    return {
        "algorithm": "treeBased",
        "api_kind": api_kind,
        "normalized_source": normalized_source,
        "representation": built,
        "meta": {
            "tree_size": tree_size,
            "has_api_tree": has_api_tree,
        },
    }

def similarity_from_representation(
    repr_a: Dict[str, Any],
    repr_b: Dict[str, Any],
) -> float:
    """
    基于两段已编译表示计算结构相似度。

    参数:
        repr_a: 第一个 API 的已编译表示。
        repr_b: 第二个 API 的已编译表示。

    返回:
        一个 [0, 1] 区间的浮点数，数值越大表示越相似。
    """
    result = _compute_similarity_from_representations(
        repr_a,
        repr_b,
        keep_trees=False,
    )
    return result["similarity"]


def detail_from_representation(
    repr_a: Dict[str, Any],
    repr_b: Dict[str, Any],
) -> Dict[str, Any]:
    """
    基于两段已编译表示计算结构相似度，并返回详细信息。

    注意:
        若输入表示在 build_representation 时未开启 keep_api_tree，
        则返回中的 tree_1 / tree_2 会是 None。

    参数:
        repr_a: 第一个 API 的已编译表示。
        repr_b: 第二个 API 的已编译表示。

    返回:
        detail 结果字典。
    """
    return _compute_similarity_from_representations(
        repr_a,
        repr_b,
        keep_trees=True,
    )


def similarity(src1: str, src2: str) -> float:
    """
    计算两个 API 源代码的结构相似度。

    该函数不会再走 detail 路径，也不会保留 detail 级的大对象树，
    以降低内存占用并减少不必要的中间对象构建。

    参数:
        src1: 第一个 API 的源码字符串。
        src2: 第二个 API 的源码字符串。

    返回:
        一个 [0, 1] 区间的浮点数，数值越大表示越相似。
    """
    repr1 = build_representation(src1, keep_api_tree=False)
    repr2 = build_representation(src2, keep_api_tree=False)
    return similarity_from_representation(repr1, repr2)


def api_similarity_detail(src1: str, src2: str) -> Dict[str, Any]:
    """
    计算两个 API 的结构相似度，并返回详细信息。

    参数:
        src1: 第一个 API 的源码字符串。
        src2: 第二个 API 的源码字符串。

    返回:
        一个字典，包含以下字段：
        - kind: API 类型，'class' 或 'callable'
        - similarity: 归一化后的相似度
        - tree_edit_distance: 树编辑距离
        - tree_size_1: 第一个 API 树的节点数
        - tree_size_2: 第二个 API 树的节点数
        - tree_1: 第一个轻量树对象
        - tree_2: 第二个轻量树对象
    """
    repr1 = build_representation(src1, keep_api_tree=True)
    repr2 = build_representation(src2, keep_api_tree=True)
    return detail_from_representation(repr1, repr2)


def _compute_similarity_from_representations(
    repr_a: Dict[str, Any],
    repr_b: Dict[str, Any],
    keep_trees: bool,
) -> Dict[str, Any]:
    """
    统一的“已编译表示 -> 相似度结果”核心逻辑。

    说明：
        - callable 仍然走原有单棵函数树 TED 逻辑
        - class 走分层类级相似度逻辑，避免整棵 class 树直接 TED
    """
    built1, kind1 = _validate_and_extract_representation(repr_a)
    built2, kind2 = _validate_and_extract_representation(repr_b)

    if kind1 != kind2:
        raise ValueError(f"输入 API 类型不一致: {kind1} vs {kind2}")

    if kind1 == "class":
        if not isinstance(built1, BuiltClassRepresentation) or not isinstance(built2, BuiltClassRepresentation):
            raise TypeError("class 的 representation 字段必须是 BuiltClassRepresentation")
        return _compute_class_similarity_from_built(built1, built2, keep_trees=keep_trees)

    if not isinstance(built1, BuiltTree) or not isinstance(built2, BuiltTree):
        raise TypeError("callable 的 representation 字段必须是 BuiltTree")

    ted = simple_distance(
        built1.zss_node,
        built2.zss_node,
        get_children=lambda n: n.children,
        get_label=lambda n: n.label,
        label_dist=label_distance,
    )

    denom = max(built1.size + built2.size, 1)
    similarity_value = 1.0 - (ted / denom)
    similarity_value = max(0.0, min(1.0, similarity_value))

    result: Dict[str, Any] = {
        "kind": kind1,
        "similarity": similarity_value,
        "tree_edit_distance": ted,
        "tree_size_1": built1.size,
        "tree_size_2": built2.size,
    }
    if keep_trees:
        result["tree_1"] = built1.api_tree
        result["tree_2"] = built2.api_tree
    return result


def _validate_and_extract_representation(repr_obj: Dict[str, Any]) -> Tuple[Any, str]:
    """
    校验单个表示对象，并提取核心字段。

    参数:
        repr_obj: build_representation 的返回字典。

    返回:
        (representation, api_kind)
    """
    if not isinstance(repr_obj, dict):
        raise TypeError("表示对象必须是 dict")

    if repr_obj.get("algorithm") != "treeBased":
        raise ValueError(f"表示对象不是 treeBased: {repr_obj.get('algorithm')}")

    api_kind = repr_obj.get("api_kind")
    built = repr_obj.get("representation")

    if api_kind not in {"class", "callable"}:
        raise ValueError(f"无效的 api_kind: {api_kind}")

    if api_kind == "callable" and not isinstance(built, BuiltTree):
        raise TypeError("callable 的 representation 字段必须是 BuiltTree")

    if api_kind == "class" and not isinstance(built, BuiltClassRepresentation):
        raise TypeError("class 的 representation 字段必须是 BuiltClassRepresentation")

    return built, api_kind


def _compute_tree_similarity_detail(built1: BuiltTree, built2: BuiltTree) -> Dict[str, Any]:
    """
    对两棵 BuiltTree 计算 TED 相似度。

    该函数复用原有 simple_distance、label_distance 和归一化方式，
    用于类头部小树和匹配方法树。
    """
    ted = simple_distance(
        built1.zss_node,
        built2.zss_node,
        get_children=lambda n: n.children,
        get_label=lambda n: n.label,
        label_dist=label_distance,
    )

    return {
        "tree_edit_distance": ted,
        "tree_size_1": built1.size,
        "tree_size_2": built2.size,
        "similarity": _normalize_ted_similarity(ted, built1.size, built2.size),
    }


def _normalize_ted_similarity(ted: float, size1: int, size2: int) -> float:
    """
    使用原有归一化方式将 TED 转为 [0, 1] 相似度。
    """
    denom = max(size1 + size2, 1)
    similarity_value = 1.0 - (ted / denom)
    return max(0.0, min(1.0, similarity_value))


def _jaccard_similarity(items_a: Any, items_b: Any) -> float:
    """
    计算两个字符串集合的 Jaccard 相似度。
    """
    if not items_a and not items_b:
        return 1.0

    union = items_a | items_b
    if not union:
        return 1.0

    return len(items_a & items_b) / len(union)


def _compute_class_similarity_from_built(
    built1: BuiltClassRepresentation,
    built2: BuiltClassRepresentation,
    keep_trees: bool,
) -> Dict[str, Any]:
    """
    计算分层 class 相似度。

    公式：
        class_similarity =
            0.15 * header_ted_similarity
          + 0.10 * attribute_jaccard_similarity
          + 0.15 * method_set_jaccard_similarity
          + 0.60 * method_set_jaccard_similarity * matched_method_ted_similarity
    """
    header_result = _compute_tree_similarity_detail(built1.header_tree, built2.header_tree)
    header_similarity = header_result["similarity"]

    attribute_similarity = _jaccard_similarity(
        built1.class_attributes,
        built2.class_attributes,
    )

    methods1 = frozenset(built1.methods.keys())
    methods2 = frozenset(built2.methods.keys())
    method_set_similarity = _jaccard_similarity(methods1, methods2)

    common_methods = sorted(methods1 & methods2)
    method_scores: Dict[str, float] = {}
    method_details: Dict[str, Dict[str, Any]] = {}

    for method_name in common_methods:
        method_result = _compute_tree_similarity_detail(
            built1.methods[method_name],
            built2.methods[method_name],
        )
        method_scores[method_name] = method_result["similarity"]
        if keep_trees:
            method_details[method_name] = method_result

    if method_scores:
        matched_method_similarity = sum(method_scores.values()) / len(method_scores)
    else:
        matched_method_similarity = 0.0

    coverage_weighted_method_similarity = method_set_similarity * matched_method_similarity

    final_similarity = (
        CLASS_HEADER_WEIGHT * header_similarity
        + CLASS_ATTRIBUTE_WEIGHT * attribute_similarity
        + CLASS_METHOD_SET_WEIGHT * method_set_similarity
        + CLASS_MATCHED_METHOD_WEIGHT * coverage_weighted_method_similarity
    )
    final_similarity = max(0.0, min(1.0, final_similarity))

    result: Dict[str, Any] = {
        "kind": "class",
        "similarity": final_similarity,
        "tree_edit_distance": None,
        "tree_size_1": built1.size,
        "tree_size_2": built2.size,
        "components": {
            "header_similarity": header_similarity,
            "attribute_similarity": attribute_similarity,
            "method_set_similarity": method_set_similarity,
            "matched_method_similarity": matched_method_similarity,
            "coverage_weighted_method_similarity": coverage_weighted_method_similarity,
            "weights": {
                "header": CLASS_HEADER_WEIGHT,
                "attribute": CLASS_ATTRIBUTE_WEIGHT,
                "method_set": CLASS_METHOD_SET_WEIGHT,
                "coverage_weighted_method": CLASS_MATCHED_METHOD_WEIGHT,
            },
        },
    }

    if keep_trees:
        result["header_detail"] = header_result
        result["method_scores"] = method_scores
        result["method_details"] = method_details
        result["class_attributes_1"] = sorted(built1.class_attributes)
        result["class_attributes_2"] = sorted(built2.class_attributes)
        result["methods_1"] = sorted(methods1)
        result["methods_2"] = sorted(methods2)
        result["header_tree_1"] = built1.header_tree.api_tree
        result["header_tree_2"] = built2.header_tree.api_tree

    return result

# =========================
# 源码标准化与 AST 预处理
# =========================

def preprocess_api_node(src: str) -> ast.AST:
    """
    对源码完成一次性预处理，并返回可用于构树的 AST。

    预处理步骤：
    1. 解析单个顶层 API
    2. 原地删除 docstring
    3. 原地做局部绑定名归一化

    这里不再做两次 deepcopy。
    parse_api_node 返回的是新解析出的 AST，后续可直接原地改写，
    这样可以显著降低内存占用。

    参数:
        src: API 源码字符串。

    返回:
        预处理后的 AST 节点。
    """
    node = parse_api_node(src)
    remove_docstrings_inplace(node)
    normalize_local_bindings(node, copy_tree=False)
    return node


def parse_api_node(src: str) -> ast.AST:
    """
    将源码字符串解析为单个顶层 API 节点。

    参数:
        src: API 源码字符串，通常来自 inspect.getsource 的输出。

    返回:
        顶层 API 对应的 ast.AST 节点。

    异常:
        ValueError: 当源码为空，或者不只包含一个顶层 API 定义时抛出。
        SyntaxError: 当源码本身无法被 Python 解析时抛出。
    """
    normalized = normalize_source(src)

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=r".*invalid escape sequence.*",
            category=SyntaxWarning,
        )
        try:
            module = ast.parse(normalized)
        except SyntaxError:
            from .py2_to_py3_converter import convert_py2_to_py3
            try:
                py3_normalized = convert_py2_to_py3(normalized)
                module = ast.parse(py3_normalized)
            except Exception as e:
                raise SyntaxError(f"AST 解析失败且尝试 Py2 转译也失败: {e}")

    candidates = [
        node for node in module.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    if len(candidates) != 1:
        raise ValueError(
            "源码必须只包含一个顶层 API 定义（一个 class / function / async function）"
        )

    return candidates[0]


def normalize_source(src: str) -> str:
    """
    对输入源码进行标准化处理。

    核心原则：
    - 不使用 .strip() 直接处理整段源码，避免破坏首行装饰器缩进
    - 按第一个 def / async def / class 行的缩进作为基准缩进
    - 只删除首尾空白行，不删除有效代码行的前导空格
    """
    if not isinstance(src, str):
        raise TypeError(f"src 必须是字符串，当前类型为：{type(src)}")

    src = src.replace("\r\n", "\n").replace("\r", "\n")
    lines = src.split("\n")

    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        raise ValueError("源码为空")

    base_prefix = ""
    for line in lines:
        stripped = line.lstrip(" \t")
        if _API_DEF_RE.match(stripped):
            base_prefix = line[: len(line) - len(stripped)]
            break

    if base_prefix:
        lines = [
            line[len(base_prefix):] if line.startswith(base_prefix) else line
            for line in lines
        ]
    else:
        lines = textwrap.dedent("\n".join(lines)).split("\n")

    normalized = "\n".join(lines).rstrip() + "\n"

    if not normalized.strip():
        raise ValueError("源码为空")

    return normalized

def get_api_kind(node: ast.AST) -> str:
    """
    获取 API 节点的类型标签。

    参数:
        node: 顶层 API AST 节点。

    返回:
        - 'class'：表示类
        - 'callable'：表示函数 / 方法 / async 函数
    """
    if isinstance(node, ast.ClassDef):
        return "class"
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return "callable"
    raise TypeError(f"不支持的 API 类型: {type(node).__name__}")


def remove_docstrings_inplace(node: ast.AST) -> ast.AST:
    """
    原地删除 AST 中所有适合作为 docstring 的语句节点。

    参数:
        node: 原始 AST 节点。

    返回:
        删除 docstring 后的同一个 AST 节点。
    """
    for sub in ast.walk(node):
        body = getattr(sub, "body", None)
        if isinstance(body, list) and body and is_docstring_stmt(body[0]):
            del body[0]
    return node


def remove_docstrings(node: ast.AST, copy_tree: bool = True) -> ast.AST:
    """
    删除 AST 中所有适合作为 docstring 的语句节点。

    参数:
        node: 原始 AST 节点。
        copy_tree: 是否先复制一份再删除。默认保持兼容行为。

    返回:
        删除 docstring 后的 AST。
    """
    working = copy.deepcopy(node) if copy_tree else node
    return remove_docstrings_inplace(working)


def is_docstring_stmt(stmt: ast.stmt) -> bool:
    """
    判断一个语句节点是否是 docstring 语句。

    参数:
        stmt: 待判断的语句节点。

    返回:
        True 表示该节点是 docstring 语句，否则为 False。
    """
    if not isinstance(stmt, ast.Expr):
        return False
    value = stmt.value
    return isinstance(value, ast.Constant) and isinstance(value.value, str)


# =========================
# 局部绑定名归一化
# =========================

class LocalBindingNormalizer(ast.NodeTransformer):
    """
    对 API AST 中的“局部绑定名”做归一化。

    这里修复了类相关作用域问题：
    - 类体本身有独立作用域，类属性赋值、类体推导式等不会再因无作用域而出错
    - 但类作用域不会向方法内部泄漏，避免把类属性名错误当成方法内部的闭包变量
    """

    def __init__(self) -> None:
        super().__init__()
        self.scopes: List[Dict[str, Any]] = []

    # ---------- 作用域管理 ----------

    def _push_scope(self, kind: str) -> None:
        """
        压入一个新的局部作用域。

        参数:
            kind: 作用域类型，可取 'function'、'lambda'、'class'。
        """
        self.scopes.append({
            "kind": kind,
            "name_map": {},
            "counter": 0,
        })

    def _pop_scope(self) -> None:
        """
        弹出当前局部作用域。
        """
        if not self.scopes:
            raise RuntimeError("作用域栈为空，无法弹出")
        self.scopes.pop()

    def _current_scope(self) -> Dict[str, Any]:
        """
        获取当前作用域对象。
        """
        if not self.scopes:
            raise RuntimeError("当前没有可用作用域")
        return self.scopes[-1]

    # ---------- 名字绑定与查询 ----------

    def _bind_name(self, original: str, prefix: str = "local") -> str:
        """
        在当前作用域中为一个原始名字分配规范名。

        参数:
            original: 原始变量名。
            prefix: 规范名前缀，例如 'param'、'local'、'exc'。

        返回:
            归一化后的规范名字。
        """
        scope = self._current_scope()
        name_map: Dict[str, str] = scope["name_map"]

        if original in name_map:
            return name_map[original]

        index = scope["counter"]
        scope["counter"] += 1
        normalized = f"{prefix}_{index}"
        name_map[original] = normalized
        return normalized

    def _lookup_name(self, name: str) -> Optional[str]:
        """
        从内到外查找一个名字是否已经在某个局部作用域中绑定。

        规则：
        - 函数 / lambda 内可以看到外层函数 / lambda 作用域
        - 但不会穿透 class 作用域去捕获类体中的绑定名

        参数:
            name: 待查询的原始名字。

        返回:
            若该名字已绑定，返回对应规范名；否则返回 None。
        """
        seen_function_like_scope = False

        for scope in reversed(self.scopes):
            kind = scope["kind"]
            if kind == "class" and seen_function_like_scope:
                break

            name_map: Dict[str, str] = scope["name_map"]
            if name in name_map:
                return name_map[name]

            if kind in {"function", "lambda"}:
                seen_function_like_scope = True

        return None

    # ---------- 绑定目标处理 ----------

    def _bind_target(self, node: ast.AST, prefix: str = "local") -> ast.AST:
        """
        对“绑定目标”做归一化。

        参数:
            node: 绑定目标 AST 节点。
            prefix: 规范名前缀。

        返回:
            归一化后的目标节点。
        """
        if isinstance(node, ast.Name):
            return ast.copy_location(
                ast.Name(id=self._bind_name(node.id, prefix=prefix), ctx=node.ctx),
                node,
            )

        if isinstance(node, ast.Tuple):
            return ast.copy_location(
                ast.Tuple(
                    elts=[self._bind_target(elt, prefix=prefix) for elt in node.elts],
                    ctx=node.ctx,
                ),
                node,
            )

        if isinstance(node, ast.List):
            return ast.copy_location(
                ast.List(
                    elts=[self._bind_target(elt, prefix=prefix) for elt in node.elts],
                    ctx=node.ctx,
                ),
                node,
            )

        if isinstance(node, ast.Starred):
            return ast.copy_location(
                ast.Starred(
                    value=self._bind_target(node.value, prefix=prefix),
                    ctx=node.ctx,
                ),
                node,
            )

        if isinstance(node, ast.Subscript):
            return self.generic_visit(node)

        if isinstance(node, ast.Attribute):
            return self.generic_visit(node)

        return self.generic_visit(node)

    # ---------- 顶层 API 入口 ----------

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        """
        访问普通函数定义，并在其局部作用域中归一化参数与函数体中的局部绑定名。

        参数:
            node: ast.FunctionDef 节点。

        返回:
            归一化后的 ast.FunctionDef 节点。
        """
        self._push_scope("function")
        try:
            node.args = self.visit(node.args)
            node.decorator_list = [self.visit(d) for d in node.decorator_list]
            if node.returns is not None:
                node.returns = self.visit(node.returns)
            node.body = [self.visit(stmt) for stmt in node.body]
            return node
        finally:
            self._pop_scope()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
        """
        访问异步函数定义，并在其局部作用域中归一化参数与函数体中的局部绑定名。

        参数:
            node: ast.AsyncFunctionDef 节点。

        返回:
            归一化后的 ast.AsyncFunctionDef 节点。
        """
        self._push_scope("function")
        try:
            node.args = self.visit(node.args)
            node.decorator_list = [self.visit(d) for d in node.decorator_list]
            if node.returns is not None:
                node.returns = self.visit(node.returns)
            node.body = [self.visit(stmt) for stmt in node.body]
            return node
        finally:
            self._pop_scope()

    def visit_Lambda(self, node: ast.Lambda) -> ast.AST:
        """
        访问 lambda 表达式，并为其建立独立局部作用域。

        参数:
            node: ast.Lambda 节点。

        返回:
            归一化后的 ast.Lambda 节点。
        """
        self._push_scope("lambda")
        try:
            node.args = self.visit(node.args)
            node.body = self.visit(node.body)
            return node
        finally:
            self._pop_scope()

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:
        """
        访问类定义。

        类头部 decorators / bases / keywords 中也可能出现推导式，
        因此需要给类头部表达式一个临时作用域，避免无作用域绑定报错。
        类体仍然使用独立 class 作用域。
        """

        self._push_scope("class_header")
        try:
            node.bases = [self.visit(base) for base in node.bases]
            node.keywords = [self.visit(kw) for kw in node.keywords]
            node.decorator_list = [self.visit(d) for d in node.decorator_list]
        finally:
            self._pop_scope()

        self._push_scope("class")
        try:
            node.body = [self.visit(stmt) for stmt in node.body]
            return node
        finally:
            self._pop_scope()

    # ---------- 参数归一化 ----------

    def visit_arguments(self, node: ast.arguments) -> ast.AST:
        """
        访问函数参数列表，并将参数名归一化。

        参数:
            node: ast.arguments 节点。

        返回:
            归一化后的 ast.arguments 节点。
        """
        node.posonlyargs = [self.visit(arg) for arg in node.posonlyargs]
        node.args = [self.visit(arg) for arg in node.args]

        if node.vararg is not None:
            node.vararg = self.visit(node.vararg)

        node.kwonlyargs = [self.visit(arg) for arg in node.kwonlyargs]

        if node.kwarg is not None:
            node.kwarg = self.visit(node.kwarg)

        node.defaults = [self.visit(d) for d in node.defaults]
        node.kw_defaults = [self.visit(d) if d is not None else None for d in node.kw_defaults]
        return node

    def visit_arg(self, node: ast.arg) -> ast.AST:
        """
        访问单个参数节点，并将参数名归一化。

        参数:
            node: ast.arg 节点。

        返回:
            归一化后的 ast.arg 节点。
        """
        node.arg = self._bind_name(node.arg, prefix="param")
        if node.annotation is not None:
            node.annotation = self.visit(node.annotation)
        return node

    # ---------- 普通名字引用替换 ----------

    def visit_Name(self, node: ast.Name) -> ast.AST:
        """
        访问普通名字节点。

        参数:
            node: ast.Name 节点。

        返回:
            处理后的 ast.Name 节点。
        """
        normalized = self._lookup_name(node.id)
        if normalized is None:
            return node

        return ast.copy_location(
            ast.Name(id=normalized, ctx=node.ctx),
            node,
        )

    # ---------- 各类绑定语句 ----------

    def visit_Assign(self, node: ast.Assign) -> ast.AST:
        """
        访问赋值语句，并归一化赋值目标中的局部绑定名。

        参数:
            node: ast.Assign 节点。

        返回:
            归一化后的 ast.Assign 节点。
        """
        node.value = self.visit(node.value)
        node.targets = [self._bind_target(t, prefix="local") for t in node.targets]
        return node

    def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AST:
        """
        访问带注解赋值语句，并归一化其绑定目标中的局部变量名。

        参数:
            node: ast.AnnAssign 节点。

        返回:
            归一化后的 ast.AnnAssign 节点。
        """
        node.annotation = self.visit(node.annotation)
        if node.value is not None:
            node.value = self.visit(node.value)
        node.target = self._bind_target(node.target, prefix="local")
        return node

    def visit_AugAssign(self, node: ast.AugAssign) -> ast.AST:
        """
        访问增量赋值语句。

        参数:
            node: ast.AugAssign 节点。

        返回:
            归一化后的 ast.AugAssign 节点。
        """
        node.target = self.visit(node.target)
        node.value = self.visit(node.value)
        return node

    def visit_For(self, node: ast.For) -> ast.AST:
        """
        访问 for 循环，并归一化循环变量。

        参数:
            node: ast.For 节点。

        返回:
            归一化后的 ast.For 节点。
        """
        node.iter = self.visit(node.iter)
        node.target = self._bind_target(node.target, prefix="local")
        node.body = [self.visit(stmt) for stmt in node.body]
        node.orelse = [self.visit(stmt) for stmt in node.orelse]
        return node

    def visit_AsyncFor(self, node: ast.AsyncFor) -> ast.AST:
        """
        访问 async for 循环，并归一化循环变量。

        参数:
            node: ast.AsyncFor 节点。

        返回:
            归一化后的 ast.AsyncFor 节点。
        """
        node.iter = self.visit(node.iter)
        node.target = self._bind_target(node.target, prefix="local")
        node.body = [self.visit(stmt) for stmt in node.body]
        node.orelse = [self.visit(stmt) for stmt in node.orelse]
        return node

    def visit_With(self, node: ast.With) -> ast.AST:
        """
        访问 with 语句，并归一化 with ... as 里的绑定变量。

        参数:
            node: ast.With 节点。

        返回:
            归一化后的 ast.With 节点。
        """
        node.items = [self.visit(item) for item in node.items]
        node.body = [self.visit(stmt) for stmt in node.body]
        return node

    def visit_AsyncWith(self, node: ast.AsyncWith) -> ast.AST:
        """
        访问 async with 语句，并归一化 with ... as 里的绑定变量。

        参数:
            node: ast.AsyncWith 节点。

        返回:
            归一化后的 ast.AsyncWith 节点。
        """
        node.items = [self.visit(item) for item in node.items]
        node.body = [self.visit(stmt) for stmt in node.body]
        return node

    def visit_withitem(self, node: ast.withitem) -> ast.AST:
        """
        访问单个 withitem。

        参数:
            node: ast.withitem 节点。

        返回:
            归一化后的 ast.withitem 节点。
        """
        node.context_expr = self.visit(node.context_expr)
        if node.optional_vars is not None:
            node.optional_vars = self._bind_target(node.optional_vars, prefix="local")
        return node

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> ast.AST:
        """
        访问 except 分支，并归一化 `except ... as e` 中的异常绑定名。

        参数:
            node: ast.ExceptHandler 节点。

        返回:
            归一化后的 ast.ExceptHandler 节点。
        """
        if node.type is not None:
            node.type = self.visit(node.type)

        if node.name is not None:
            node.name = self._bind_name(node.name, prefix="exc")

        node.body = [self.visit(stmt) for stmt in node.body]
        return node

    def visit_comprehension(self, node: ast.comprehension) -> ast.AST:
        """
        访问推导式子句，并归一化推导变量。

        参数:
            node: ast.comprehension 节点。

        返回:
            归一化后的 ast.comprehension 节点。
        """
        node.iter = self.visit(node.iter)
        node.target = self._bind_target(node.target, prefix="local")
        node.ifs = [self.visit(cond) for cond in node.ifs]
        return node


def normalize_local_bindings(node: ast.AST, copy_tree: bool = True) -> ast.AST:
    """
    对 API AST 中的局部绑定名进行归一化。

    参数:
        node: 原始 API AST 节点。
        copy_tree: 是否先深拷贝再归一化。默认保持兼容行为。

    返回:
        归一化后的 AST 节点。
    """
    working = copy.deepcopy(node) if copy_tree else node
    normalizer = LocalBindingNormalizer()
    normalized = normalizer.visit(working)
    return ast.fix_missing_locations(normalized)


# =========================
# 类级分层表示构建
# =========================

def build_class_representation(
    raw_node: ast.AST,
    normalized_node: ast.AST,
    keep_api_tree: bool = False,
) -> BuiltClassRepresentation:
    """
    构建 class API 的分层表示。

    参数:
        raw_node: 未做局部绑定名归一化的 ClassDef，用于保留类属性原始名称。
        normalized_node: 已做局部绑定名归一化的 ClassDef，用于构建方法 BuiltTree。
        keep_api_tree: 是否保留 detail 所需 APITree。

    返回:
        BuiltClassRepresentation。
    """
    if not isinstance(raw_node, ast.ClassDef):
        raise TypeError(f"raw_node 必须是 ast.ClassDef，当前为: {type(raw_node).__name__}")
    if not isinstance(normalized_node, ast.ClassDef):
        raise TypeError(f"normalized_node 必须是 ast.ClassDef，当前为: {type(normalized_node).__name__}")

    header_tree = build_class_header_tree(raw_node, keep_api_tree=keep_api_tree)
    class_attributes = frozenset(extract_class_attribute_names(raw_node))
    methods = extract_method_trees(normalized_node, keep_api_tree=keep_api_tree)

    size = (
        header_tree.size
        + len(class_attributes)
        + sum(method_tree.size for method_tree in methods.values())
    )

    return BuiltClassRepresentation(
        header_tree=header_tree,
        class_attributes=class_attributes,
        methods=methods,
        size=size,
    )


def build_class_header_tree(
    node: ast.ClassDef,
    keep_api_tree: bool = False,
) -> BuiltTree:
    """
    构建类头部小树。

    头部范围：类名、父类、类关键字参数和类装饰器。
    """
    children: List[BuiltTree] = [
        _make_built_node(f"ClassName:{node.name}", (), keep_api_tree)
    ]

    base_children = [
        build_comparison_tree(base, keep_api_tree)
        for base in node.bases
    ]
    children.append(_make_built_node("Bases", base_children, keep_api_tree))

    keyword_children = [
        build_comparison_tree(keyword, keep_api_tree)
        for keyword in node.keywords
    ]
    children.append(_make_built_node("ClassKeywords", keyword_children, keep_api_tree))

    decorator_children = [
        build_comparison_tree(decorator, keep_api_tree)
        for decorator in node.decorator_list
    ]
    children.append(_make_built_node("Decorators", decorator_children, keep_api_tree))

    return _make_built_node("ClassHeader", children, keep_api_tree)


def extract_class_attribute_names(node: ast.ClassDef) -> Set[str]:
    """
    抽取直接定义在 class body 下的类属性名。

    说明：
        - 只处理 ClassDef.body 第一层的 Assign / AnnAssign
        - 不抽取 self.xxx，这类实例属性保留在方法树 TED 中处理
        - 不抽取方法内部局部变量
    """
    attrs: Set[str] = set()

    for stmt in node.body:
        if is_docstring_stmt(stmt):
            continue

        if isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                attrs.update(_extract_plain_assigned_names(target))

        elif isinstance(stmt, ast.AnnAssign):
            attrs.update(_extract_plain_assigned_names(stmt.target))

    return attrs


def _extract_plain_assigned_names(target: ast.AST) -> Set[str]:
    """
    从赋值目标中抽取普通 Name 形式的类属性名。
    """
    if isinstance(target, ast.Name):
        return {target.id}

    if isinstance(target, (ast.Tuple, ast.List)):
        result: Set[str] = set()
        for elt in target.elts:
            result.update(_extract_plain_assigned_names(elt))
        return result

    return set()


def extract_method_trees(
    node: ast.ClassDef,
    keep_api_tree: bool = False,
) -> Dict[str, BuiltTree]:
    """
    抽取 class body 第一层方法，并为每个方法构建原有 BuiltTree。

    函数/方法内部的构树逻辑不在这里修改，仍然完全复用 build_comparison_tree。
    """
    methods: Dict[str, BuiltTree] = {}

    for stmt in node.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods[stmt.name] = build_comparison_tree(
                stmt,
                keep_api_tree=keep_api_tree,
            )

    return methods


# =========================
# AST / APITree 构树核心
# =========================

def _make_built_node(label: str, children: Sequence[BuiltTree], keep_api_tree: bool) -> BuiltTree:
    """
    根据子节点构造一个聚合树节点。

    参数:
        label: 当前节点标签。
        children: 已构建好的子节点结果。
        keep_api_tree: 是否保留 APITree。

    返回:
        BuiltTree 结果。
    """
    zss_node = Node(label)
    for child in children:
        zss_node.addkid(child.zss_node)

    size = 1 + sum(child.size for child in children)
    api_tree = None
    if keep_api_tree:
        api_tree = APITree(label, tuple(child.api_tree for child in children if child.api_tree is not None))

    return BuiltTree(zss_node=zss_node, size=size, api_tree=api_tree)


def build_comparison_tree(node: ast.AST, keep_api_tree: bool = False) -> BuiltTree:
    """
    将 AST 一次性构造成比较用树。

    该函数一次递归同时产出：
    - zss.Node
    - 树大小 size
    - 可选 APITree

    相比旧实现，避免了：
    1. 先 AST -> APITree
    2. 再 APITree -> zss.Node
    3. 再单独遍历 APITree 求 size

    参数:
        node: AST 节点。
        keep_api_tree: 是否同时保留 APITree。

    返回:
        BuiltTree 结果。
    """
    if isinstance(node, ast.ClassDef):
        return _make_built_node(
            f"ClassDef:{node.name}",
            (
                class_header_build(node, keep_api_tree),
                decorators_build(node.decorator_list, keep_api_tree),
                class_body_build(node.body, keep_api_tree),
            ),
            keep_api_tree,
        )

    if isinstance(node, ast.FunctionDef):
        return _make_built_node(
            f"FunctionDef:{node.name}",
            (
                arguments_build(node.args, keep_api_tree),
                returns_build(node.returns, keep_api_tree),
                decorators_build(node.decorator_list, keep_api_tree),
                body_build(node.body, keep_api_tree),
            ),
            keep_api_tree,
        )

    if isinstance(node, ast.AsyncFunctionDef):
        return _make_built_node(
            f"AsyncFunctionDef:{node.name}",
            (
                arguments_build(node.args, keep_api_tree),
                returns_build(node.returns, keep_api_tree),
                decorators_build(node.decorator_list, keep_api_tree),
                body_build(node.body, keep_api_tree),
            ),
            keep_api_tree,
        )

    if isinstance(node, ast.arguments):
        children: List[BuiltTree] = []

        for arg in node.posonlyargs:
            children.append(arg_build("posonly", arg, keep_api_tree))
        for arg in node.args:
            children.append(arg_build("arg", arg, keep_api_tree))
        if node.vararg:
            children.append(arg_build("vararg", node.vararg, keep_api_tree))
        for arg in node.kwonlyargs:
            children.append(arg_build("kwonly", arg, keep_api_tree))
        if node.kwarg:
            children.append(arg_build("kwarg", node.kwarg, keep_api_tree))

        children.extend(default_values_build(node.defaults, "default", keep_api_tree))
        children.extend(default_values_build(node.kw_defaults, "kwdefault", keep_api_tree))
        return _make_built_node("arguments", children, keep_api_tree)

    if isinstance(node, ast.arg):
        children: List[BuiltTree] = []
        if node.annotation is not None:
            children.append(build_comparison_tree(node.annotation, keep_api_tree))
        return _make_built_node(f"arg:{node.arg}", children, keep_api_tree)

    if isinstance(node, ast.Name):
        return _make_built_node(f"Name:{node.id}", (), keep_api_tree)

    if isinstance(node, ast.Attribute):
        return _make_built_node(
            f"Attribute:{node.attr}",
            (build_comparison_tree(node.value, keep_api_tree),),
            keep_api_tree,
        )

    if isinstance(node, ast.Constant):
        return _make_built_node(constant_label(node.value), (), keep_api_tree)

    if isinstance(node, ast.Call):
        children = [build_comparison_tree(node.func, keep_api_tree)]
        children.extend(build_comparison_tree(arg, keep_api_tree) for arg in node.args)
        children.extend(build_comparison_tree(kw, keep_api_tree) for kw in node.keywords)
        return _make_built_node("Call", children, keep_api_tree)

    if isinstance(node, ast.keyword):
        if node.arg is None:
            return _make_built_node(
                "keyword:**",
                (build_comparison_tree(node.value, keep_api_tree),),
                keep_api_tree,
            )
        return _make_built_node(
            f"keyword:{node.arg}",
            (build_comparison_tree(node.value, keep_api_tree),),
            keep_api_tree,
        )

    if isinstance(node, ast.Return):
        if node.value is None:
            return _make_built_node("Return", (), keep_api_tree)
        return _make_built_node(
            "Return",
            (build_comparison_tree(node.value, keep_api_tree),),
            keep_api_tree,
        )

    if isinstance(node, ast.Assign):
        children = [build_comparison_tree(t, keep_api_tree) for t in node.targets]
        children.append(build_comparison_tree(node.value, keep_api_tree))
        return _make_built_node("Assign", children, keep_api_tree)

    if isinstance(node, ast.AnnAssign):
        children = [
            build_comparison_tree(node.target, keep_api_tree),
            build_comparison_tree(node.annotation, keep_api_tree),
        ]
        if node.value is not None:
            children.append(build_comparison_tree(node.value, keep_api_tree))
        return _make_built_node("AnnAssign", children, keep_api_tree)

    if isinstance(node, ast.AugAssign):
        return _make_built_node(
            f"AugAssign:{type(node.op).__name__}",
            (
                build_comparison_tree(node.target, keep_api_tree),
                build_comparison_tree(node.value, keep_api_tree),
            ),
            keep_api_tree,
        )

    if isinstance(node, ast.Expr):
        return _make_built_node(
            "Expr",
            (build_comparison_tree(node.value, keep_api_tree),),
            keep_api_tree,
        )

    if isinstance(node, ast.If):
        children = [
            build_comparison_tree(node.test, keep_api_tree),
            body_build(node.body, keep_api_tree),
        ]
        if node.orelse:
            children.append(body_build(node.orelse, keep_api_tree))
        return _make_built_node("If", children, keep_api_tree)

    if isinstance(node, ast.For):
        children = [
            build_comparison_tree(node.target, keep_api_tree),
            build_comparison_tree(node.iter, keep_api_tree),
            body_build(node.body, keep_api_tree),
        ]
        if node.orelse:
            children.append(body_build(node.orelse, keep_api_tree))
        return _make_built_node("For", children, keep_api_tree)

    if isinstance(node, ast.AsyncFor):
        children = [
            build_comparison_tree(node.target, keep_api_tree),
            build_comparison_tree(node.iter, keep_api_tree),
            body_build(node.body, keep_api_tree),
        ]
        if node.orelse:
            children.append(body_build(node.orelse, keep_api_tree))
        return _make_built_node("AsyncFor", children, keep_api_tree)

    if isinstance(node, ast.While):
        children = [
            build_comparison_tree(node.test, keep_api_tree),
            body_build(node.body, keep_api_tree),
        ]
        if node.orelse:
            children.append(body_build(node.orelse, keep_api_tree))
        return _make_built_node("While", children, keep_api_tree)

    if isinstance(node, ast.Try):
        children = [body_build(node.body, keep_api_tree)]
        children.extend(build_comparison_tree(h, keep_api_tree) for h in node.handlers)
        if node.orelse:
            children.append(body_build(node.orelse, keep_api_tree))
        if node.finalbody:
            children.append(body_build(node.finalbody, keep_api_tree))
        return _make_built_node("Try", children, keep_api_tree)

    if isinstance(node, ast.ExceptHandler):
        children: List[BuiltTree] = []
        if node.type is not None:
            children.append(build_comparison_tree(node.type, keep_api_tree))
        if node.name is not None:
            children.append(_make_built_node(f"ExceptName:{node.name}", (), keep_api_tree))
        children.append(body_build(node.body, keep_api_tree))
        return _make_built_node("ExceptHandler", children, keep_api_tree)

    if isinstance(node, ast.With):
        children = [build_comparison_tree(item, keep_api_tree) for item in node.items]
        children.append(body_build(node.body, keep_api_tree))
        return _make_built_node("With", children, keep_api_tree)

    if isinstance(node, ast.AsyncWith):
        children = [build_comparison_tree(item, keep_api_tree) for item in node.items]
        children.append(body_build(node.body, keep_api_tree))
        return _make_built_node("AsyncWith", children, keep_api_tree)

    if isinstance(node, ast.withitem):
        children = [build_comparison_tree(node.context_expr, keep_api_tree)]
        if node.optional_vars is not None:
            children.append(build_comparison_tree(node.optional_vars, keep_api_tree))
        return _make_built_node("withitem", children, keep_api_tree)

    if isinstance(node, ast.Raise):
        children: List[BuiltTree] = []
        if node.exc is not None:
            children.append(build_comparison_tree(node.exc, keep_api_tree))
        if node.cause is not None:
            children.append(build_comparison_tree(node.cause, keep_api_tree))
        return _make_built_node("Raise", children, keep_api_tree)

    if isinstance(node, ast.Assert):
        children = [build_comparison_tree(node.test, keep_api_tree)]
        if node.msg is not None:
            children.append(build_comparison_tree(node.msg, keep_api_tree))
        return _make_built_node("Assert", children, keep_api_tree)

    if isinstance(node, ast.BoolOp):
        return _make_built_node(
            f"BoolOp:{type(node.op).__name__}",
            tuple(build_comparison_tree(v, keep_api_tree) for v in node.values),
            keep_api_tree,
        )

    if isinstance(node, ast.BinOp):
        return _make_built_node(
            f"BinOp:{type(node.op).__name__}",
            (
                build_comparison_tree(node.left, keep_api_tree),
                build_comparison_tree(node.right, keep_api_tree),
            ),
            keep_api_tree,
        )

    if isinstance(node, ast.UnaryOp):
        return _make_built_node(
            f"UnaryOp:{type(node.op).__name__}",
            (build_comparison_tree(node.operand, keep_api_tree),),
            keep_api_tree,
        )

    if isinstance(node, ast.Compare):
        children = [build_comparison_tree(node.left, keep_api_tree)]
        for op, comp in zip(node.ops, node.comparators):
            children.append(_make_built_node(f"CmpOp:{type(op).__name__}", (), keep_api_tree))
            children.append(build_comparison_tree(comp, keep_api_tree))
        return _make_built_node("Compare", children, keep_api_tree)

    if isinstance(node, ast.Subscript):
        return _make_built_node(
            "Subscript",
            (
                build_comparison_tree(node.value, keep_api_tree),
                build_comparison_tree(node.slice, keep_api_tree),
            ),
            keep_api_tree,
        )

    if isinstance(node, ast.List):
        return _make_built_node(
            "List",
            tuple(build_comparison_tree(e, keep_api_tree) for e in node.elts),
            keep_api_tree,
        )

    if isinstance(node, ast.Tuple):
        return _make_built_node(
            "Tuple",
            tuple(build_comparison_tree(e, keep_api_tree) for e in node.elts),
            keep_api_tree,
        )

    if isinstance(node, ast.Set):
        return _make_built_node(
            "Set",
            tuple(build_comparison_tree(e, keep_api_tree) for e in node.elts),
            keep_api_tree,
        )

    if isinstance(node, ast.Dict):
        children: List[BuiltTree] = []
        for key, value in zip(node.keys, node.values):
            if key is None:
                children.append(
                    _make_built_node(
                        "dict_unpack",
                        (build_comparison_tree(value, keep_api_tree),),
                        keep_api_tree,
                    )
                )
            else:
                children.append(
                    _make_built_node(
                        "dict_item",
                        (
                            build_comparison_tree(key, keep_api_tree),
                            build_comparison_tree(value, keep_api_tree),
                        ),
                        keep_api_tree,
                    )
                )
        return _make_built_node("Dict", children, keep_api_tree)

    if isinstance(node, ast.ListComp):
        children = [build_comparison_tree(node.elt, keep_api_tree)]
        children.extend(build_comparison_tree(g, keep_api_tree) for g in node.generators)
        return _make_built_node("ListComp", children, keep_api_tree)

    if isinstance(node, ast.SetComp):
        children = [build_comparison_tree(node.elt, keep_api_tree)]
        children.extend(build_comparison_tree(g, keep_api_tree) for g in node.generators)
        return _make_built_node("SetComp", children, keep_api_tree)

    if isinstance(node, ast.GeneratorExp):
        children = [build_comparison_tree(node.elt, keep_api_tree)]
        children.extend(build_comparison_tree(g, keep_api_tree) for g in node.generators)
        return _make_built_node("GeneratorExp", children, keep_api_tree)

    if isinstance(node, ast.DictComp):
        children = [
            build_comparison_tree(node.key, keep_api_tree),
            build_comparison_tree(node.value, keep_api_tree),
        ]
        children.extend(build_comparison_tree(g, keep_api_tree) for g in node.generators)
        return _make_built_node("DictComp", children, keep_api_tree)

    if isinstance(node, ast.comprehension):
        children = [
            build_comparison_tree(node.target, keep_api_tree),
            build_comparison_tree(node.iter, keep_api_tree),
        ]
        children.extend(build_comparison_tree(i, keep_api_tree) for i in node.ifs)
        return _make_built_node("comprehension", children, keep_api_tree)

    if isinstance(node, ast.Lambda):
        return _make_built_node(
            "Lambda",
            (
                build_comparison_tree(node.args, keep_api_tree),
                build_comparison_tree(node.body, keep_api_tree),
            ),
            keep_api_tree,
        )

    if isinstance(node, ast.JoinedStr):
        return _make_built_node(
            "JoinedStr",
            tuple(build_comparison_tree(v, keep_api_tree) for v in node.values),
            keep_api_tree,
        )

    if isinstance(node, ast.FormattedValue):
        children = [build_comparison_tree(node.value, keep_api_tree)]
        if node.format_spec is not None:
            children.append(build_comparison_tree(node.format_spec, keep_api_tree))
        return _make_built_node("FormattedValue", children, keep_api_tree)

    if isinstance(node, ast.Import):
        return _make_built_node(
            "Import",
            tuple(_make_built_node(f"alias:{a.name}:{a.asname}", (), keep_api_tree) for a in node.names),
            keep_api_tree,
        )

    if isinstance(node, ast.ImportFrom):
        return _make_built_node(
            f"ImportFrom:{node.module}:{node.level}",
            tuple(_make_built_node(f"alias:{a.name}:{a.asname}", (), keep_api_tree) for a in node.names),
            keep_api_tree,
        )

    if isinstance(node, ast.Pass):
        return _make_built_node("Pass", (), keep_api_tree)

    if isinstance(node, ast.Break):
        return _make_built_node("Break", (), keep_api_tree)

    if isinstance(node, ast.Continue):
        return _make_built_node("Continue", (), keep_api_tree)

    if isinstance(node, ast.Delete):
        return _make_built_node(
            "Delete",
            tuple(build_comparison_tree(t, keep_api_tree) for t in node.targets),
            keep_api_tree,
        )

    if isinstance(node, ast.Slice):
        children: List[BuiltTree] = []
        if node.lower is not None:
            children.append(build_comparison_tree(node.lower, keep_api_tree))
        if node.upper is not None:
            children.append(build_comparison_tree(node.upper, keep_api_tree))
        if node.step is not None:
            children.append(build_comparison_tree(node.step, keep_api_tree))
        return _make_built_node("Slice", children, keep_api_tree)

    if isinstance(node, ast.Starred):
        return _make_built_node(
            "Starred",
            (build_comparison_tree(node.value, keep_api_tree),),
            keep_api_tree,
        )

    if isinstance(node, (ast.Load, ast.Store, ast.Del)):
        return _make_built_node("CTX", (), keep_api_tree)

    children: List[BuiltTree] = []
    for _, value in ast.iter_fields(node):
        if isinstance(value, ast.AST):
            if not isinstance(value, (ast.Load, ast.Store, ast.Del)):
                children.append(build_comparison_tree(value, keep_api_tree))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST) and not isinstance(item, (ast.Load, ast.Store, ast.Del)):
                    children.append(build_comparison_tree(item, keep_api_tree))

    return _make_built_node(type(node).__name__, children, keep_api_tree)


# =========================
# 构树辅助函数
# =========================

def class_header_build(node: ast.ClassDef, keep_api_tree: bool) -> BuiltTree:
    """
    构建类定义头部树。

    参数:
        node: ast.ClassDef 节点。
        keep_api_tree: 是否保留 APITree。

    返回:
        BuiltTree 结果。
    """
    children = [build_comparison_tree(base, keep_api_tree) for base in node.bases]
    children.extend(build_comparison_tree(kw, keep_api_tree) for kw in node.keywords)
    return _make_built_node("ClassHeader", children, keep_api_tree)


def class_body_build(body: Sequence[ast.stmt], keep_api_tree: bool) -> BuiltTree:
    """
    将类体语句列表转换为比较树。

    参数:
        body: 类体中的语句列表。
        keep_api_tree: 是否保留 APITree。

    返回:
        BuiltTree 结果。
    """
    children = [
        build_comparison_tree(stmt, keep_api_tree)
        for stmt in body
        if not is_docstring_stmt(stmt)
    ]
    return _make_built_node("ClassBody", children, keep_api_tree)


def body_build(body: Sequence[ast.stmt], keep_api_tree: bool) -> BuiltTree:
    """
    将函数体或代码块语句列表转换为比较树。

    参数:
        body: 语句列表。
        keep_api_tree: 是否保留 APITree。

    返回:
        BuiltTree 结果。
    """
    children = [
        build_comparison_tree(stmt, keep_api_tree)
        for stmt in body
        if not is_docstring_stmt(stmt)
    ]
    return _make_built_node("Body", children, keep_api_tree)


def decorators_build(decorators: Sequence[ast.expr], keep_api_tree: bool) -> BuiltTree:
    """
    将装饰器列表转换为比较树。

    参数:
        decorators: 装饰器表达式列表。
        keep_api_tree: 是否保留 APITree。

    返回:
        BuiltTree 结果。
    """
    return _make_built_node(
        "Decorators",
        tuple(build_comparison_tree(d, keep_api_tree) for d in decorators),
        keep_api_tree,
    )


def returns_build(ret: Optional[ast.expr], keep_api_tree: bool) -> BuiltTree:
    """
    将返回类型注解节点转换为比较树。

    参数:
        ret: 返回类型注解 AST 节点；如果没有则为 None。
        keep_api_tree: 是否保留 APITree。

    返回:
        BuiltTree 结果。
    """
    if ret is None:
        return _make_built_node("Returns:None", (), keep_api_tree)
    return _make_built_node("Returns", (build_comparison_tree(ret, keep_api_tree),), keep_api_tree)


def arguments_build(node: ast.arguments, keep_api_tree: bool) -> BuiltTree:
    """
    将函数参数列表 AST 转换为比较树。

    参数:
        node: ast.arguments 节点。
        keep_api_tree: 是否保留 APITree。

    返回:
        BuiltTree 结果。
    """
    children: List[BuiltTree] = []

    for arg in node.posonlyargs:
        children.append(arg_build("posonly", arg, keep_api_tree))
    for arg in node.args:
        children.append(arg_build("arg", arg, keep_api_tree))
    if node.vararg:
        children.append(arg_build("vararg", node.vararg, keep_api_tree))
    for arg in node.kwonlyargs:
        children.append(arg_build("kwonly", arg, keep_api_tree))
    if node.kwarg:
        children.append(arg_build("kwarg", node.kwarg, keep_api_tree))

    children.extend(default_values_build(node.defaults, "default", keep_api_tree))
    children.extend(default_values_build(node.kw_defaults, "kwdefault", keep_api_tree))

    return _make_built_node("arguments", children, keep_api_tree)


def arg_build(kind: str, arg: ast.arg, keep_api_tree: bool) -> BuiltTree:
    """
    将单个参数节点转换为比较树。

    参数:
        kind: 参数类别标签，例如 'arg'、'kwonly'、'vararg' 等。
        arg: 单个参数 AST 节点。
        keep_api_tree: 是否保留 APITree。

    返回:
        BuiltTree 结果。
    """
    children: List[BuiltTree] = []
    if arg.annotation is not None:
        children.append(build_comparison_tree(arg.annotation, keep_api_tree))
    return _make_built_node(f"{kind}:{arg.arg}", children, keep_api_tree)


def default_values_build(
    values: Sequence[Optional[ast.expr]],
    prefix: str,
    keep_api_tree: bool,
) -> List[BuiltTree]:
    """
    将默认值列表转换为比较树节点列表。

    参数:
        values: 默认值表达式列表，元素可能为 None。
        prefix: 节点前缀名，例如 'default' 或 'kwdefault'。
        keep_api_tree: 是否保留 APITree。

    返回:
        BuiltTree 列表。
    """
    result: List[BuiltTree] = []
    for value in values:
        if value is None:
            result.append(_make_built_node(f"{prefix}:None", (), keep_api_tree))
        else:
            result.append(
                _make_built_node(prefix, (build_comparison_tree(value, keep_api_tree),), keep_api_tree)
            )
    return result


# =========================
# 兼容旧辅助接口
# =========================

def ast_to_api_tree(node: ast.AST) -> APITree:
    """
    将 Python AST 节点转换为用于比较的轻量树结构。

    这是兼容旧接口的包装函数。

    参数:
        node: AST 节点。

    返回:
        对应的 APITree 轻量树节点。
    """
    built = build_comparison_tree(node, keep_api_tree=True)
    assert built.api_tree is not None
    return built.api_tree


def api_tree_to_zss_node(node: APITree) -> Node:
    """
    将自定义 APITree 转换为 zss.Node。

    参数:
        node: 自定义轻量树节点。

    返回:
        对应的 zss.Node 对象。
    """
    zss_node = Node(node.label)
    for child in node.children:
        zss_node.addkid(api_tree_to_zss_node(child))
    return zss_node


# =========================
# 标签与常量
# =========================

def constant_label(value: Any) -> str:
    """
    将 Python 常量值映射为粗粒度标签。

    参数:
        value: Python 常量值。

    返回:
        形如 'Const:int'、'Const:str'、'Const:None' 的字符串标签。
    """
    if value is None:
        return "Const:None"
    if isinstance(value, bool):
        return "Const:bool"
    if isinstance(value, int):
        return "Const:int"
    if isinstance(value, float):
        return "Const:float"
    if isinstance(value, complex):
        return "Const:complex"
    if isinstance(value, str):
        return "Const:str"
    if isinstance(value, bytes):
        return "Const:bytes"
    if value is Ellipsis:
        return "Const:ellipsis"
    return f"Const:{type(value).__name__}"


def label_distance(label1: str, label2: str) -> int:
    """
    定义两个节点标签之间的替换代价。

    参数:
        label1: 第一个节点标签。
        label2: 第二个节点标签。

    返回:
        一个非负整数，表示标签替换代价。
    """
    return 0 if label1 == label2 else 1


# =========================
# 辅助函数
# =========================

def tree_size(node: APITree) -> int:
    """
    计算一棵轻量树的节点总数。

    参数:
        node: 轻量树根节点。

    返回:
        整棵树的节点数。
    """
    return 1 + sum(tree_size(child) for child in node.children)
