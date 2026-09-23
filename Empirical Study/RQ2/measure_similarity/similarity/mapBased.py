import ast
import re
import textwrap
import warnings
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any


# =========================
# Graph data structures
# =========================
_API_DEF_RE = re.compile(r"(?:async\s+def|def|class)\b")
@dataclass
class GNode:
    """
    功能：
        图节点。

    参数说明：
        id:
            节点唯一编号。

        kind:
            节点类型，例如 ENTRY / CALL / RETURN。

        attrs:
            节点附加属性，用于表达简化语义标签。
    """
    id: int
    kind: str
    attrs: Dict[str, object] = field(default_factory=dict)


@dataclass
class Graph:
    """
    功能：
        简化 PDG 图结构。

    参数说明：
        nodes:
            图中的节点列表。

        edges:
            图中的边列表，格式为 (src, dst, etype)。
    """
    nodes: List[GNode] = field(default_factory=list)
    edges: List[Tuple[int, int, str]] = field(default_factory=list)

    def add_node(self, kind: str, **attrs) -> int:
        """
        功能：
            向图中添加一个节点。

        参数说明：
            kind:
                节点类型。

            **attrs:
                节点附加属性。

        返回：
            新节点的 id。
        """
        nid = len(self.nodes)
        self.nodes.append(GNode(nid, kind, attrs))
        return nid

    def add_edge(self, src: int, dst: int, etype: str) -> None:
        """
        功能：
            向图中添加一条边。

        参数说明：
            src:
                源节点 id。

            dst:
                目标节点 id。

            etype:
                边类型，例如 control / data。
        """
        self.edges.append((src, dst, etype))

    def out_edges(self, nid: int, etype: Optional[str] = None) -> List[Tuple[int, int, str]]:
        """
        功能：
            获取某个节点的出边。

        参数说明：
            nid:
                节点 id。

            etype:
                可选的边类型过滤条件。

        返回：
            满足条件的出边列表。
        """
        if etype is None:
            return [e for e in self.edges if e[0] == nid]
        return [e for e in self.edges if e[0] == nid and e[2] == etype]

    def in_edges(self, nid: int, etype: Optional[str] = None) -> List[Tuple[int, int, str]]:
        """
        功能：
            获取某个节点的入边。

        参数说明：
            nid:
                节点 id。

            etype:
                可选的边类型过滤条件。

        返回：
            满足条件的入边列表。
        """
        if etype is None:
            return [e for e in self.edges if e[1] == nid]
        return [e for e in self.edges if e[1] == nid and e[2] == etype]


# =========================
# AST utilities
# =========================

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


def _parse_api(src: str, source_name: str = "<unknown>") -> ast.AST:
    """
    功能：
        解析输入 API 源码，并做基础格式化处理。

    处理内容：
        - 去除公共前缀缩进
        - 去除首尾空白
        - 去除模块级 docstring
        - 要求源码中只包含一个顶层 API 定义
        - 局部忽略 invalid escape sequence 这类 SyntaxWarning，
          避免第三方/历史源码中的字符串写法污染日志

    参数说明：
        src:
            API 源码字符串。

        source_name:
            源码名称或路径，仅用于在解析报错时提供更可定位的信息。

    返回：
        顶层 AST 节点，可能是 ClassDef / FunctionDef / AsyncFunctionDef。

    异常：
        ValueError:
            当源码不只包含一个顶层定义，或顶层对象不是 class/function/method 时抛出。
    """
    src = normalize_source(src)

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=r".*invalid escape sequence.*",
            category=SyntaxWarning,
        )
        try:
            mod = ast.parse(src, filename=source_name)
        except SyntaxError:
            from .py2_to_py3_converter import convert_py2_to_py3
            try:
                py3_src = convert_py2_to_py3(src)
                mod = ast.parse(py3_src, filename=source_name)
            except Exception as e:
                raise SyntaxError(f"AST 解析失败且尝试 Py2 转译也失败: {e}")

    body = list(mod.body)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(getattr(body[0], "value", None), ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]

    if len(body) != 1:
        raise ValueError("输入源码应只包含一个顶层 API（一个 class 或一个 function/method）")

    node = body[0]
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        raise ValueError("顶层对象必须是 class / function / method 源码")
    return node


def _is_class_api(node: ast.AST) -> bool:
    """
    功能：
        判断顶层 API 是否为类定义。

    参数说明：
        node:
            顶层 AST 节点。

    返回：
        如果是 ClassDef 返回 True，否则返回 False。
    """
    return isinstance(node, ast.ClassDef)


def _safe_name(x) -> str:
    """
    功能：
        将对象安全转换为字符串名称。

    参数说明：
        x:
            任意对象。

    返回：
        如果 x 是字符串则原样返回，否则返回 'unknown'。
    """
    return x if isinstance(x, str) else "unknown"


def _callee_name(expr: ast.AST) -> str:
    """
    功能：
        提取调用表达式的末端调用名。

    例如：
        foo() -> foo
        self.repo.get() -> get

    参数说明：
        expr:
            调用目标表达式。

    返回：
        调用名；若无法识别则返回 'unknown'。
    """
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        return expr.attr
    if isinstance(expr, ast.Call):
        return _callee_name(expr.func)
    return "unknown"


def _base_kind(expr: ast.AST) -> str:
    """
    功能：
        粗略判断调用基对象类别。

    参数说明：
        expr:
            表达式节点。

    返回：
        'self' / 'name' / 'unknown'。
    """
    if isinstance(expr, ast.Name):
        if expr.id == "self":
            return "self"
        return "name"
    if isinstance(expr, ast.Attribute):
        return _base_kind(expr.value)
    return "unknown"


def _attr_depth(expr: ast.AST) -> int:
    """
    功能：
        计算属性访问链深度。

    例如：
        self.repo.get 的深度约为 2。

    参数说明：
        expr:
            表达式节点。

    返回：
        属性链深度。
    """
    depth = 0
    cur = expr
    while isinstance(cur, ast.Attribute):
        depth += 1
        cur = cur.value
    return depth


def _const_bucket(v) -> str:
    """
    功能：
        将常量值归入粗粒度桶，降低字面量差异敏感度。

    参数说明：
        v:
            常量值。

    返回：
        常量桶标签字符串。
    """
    if v is None:
        return "none"
    if v is True or v is False:
        return "bool"
    if isinstance(v, int):
        if v in (0, 1):
            return str(v)
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, str):
        if v == "":
            return "empty_str"
        if len(v) <= 12:
            return "short_str"
        return "str"
    return type(v).__name__


def _expr_shape(expr: ast.AST) -> str:
    """
    功能：
        提取表达式的粗粒度形状标签。

    参数说明：
        expr:
            表达式节点。

    返回：
        形状标签字符串。
    """
    if expr is None:
        return "none"
    if isinstance(expr, ast.Call):
        return "call"
    if isinstance(expr, ast.Constant):
        return f"const:{_const_bucket(expr.value)}"
    if isinstance(expr, ast.Name):
        return "name"
    if isinstance(expr, ast.Attribute):
        return "attr"
    if isinstance(expr, ast.Compare):
        return "compare"
    if isinstance(expr, ast.BoolOp):
        return "boolop"
    if isinstance(expr, ast.BinOp):
        return "binop"
    if isinstance(expr, ast.UnaryOp):
        return "unary"
    if isinstance(expr, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
        return "comprehension"
    if isinstance(expr, (ast.List, ast.Tuple, ast.Set, ast.Dict)):
        return "container"
    return type(expr).__name__.lower()


class ReadWriteCollector(ast.NodeVisitor):
    """
    功能：
        收集局部 def-use 所需的读写变量信息。

    属性：
        reads:
            被读取的变量名集合。

        writes:
            被写入的变量名集合。
    """
    def __init__(self):
        """
        功能：
            初始化读写变量收集器。
        """
        self.reads: Set[str] = set()
        self.writes: Set[str] = set()

    def visit_Name(self, node: ast.Name):
        """
        功能：
            处理 Name 节点，区分读与写。

        参数说明：
            node:
                ast.Name 节点。
        """
        if isinstance(node.ctx, ast.Load):
            self.reads.add(node.id)
        elif isinstance(node.ctx, (ast.Store, ast.Del)):
            self.writes.add(node.id)

    def visit_Attribute(self, node: ast.Attribute):
        """
        功能：
            处理属性访问节点。

        这里只递归 base，不把属性名本身当作精确变量。

        参数说明：
            node:
                ast.Attribute 节点。
        """
        self.visit(node.value)

    def visit_Subscript(self, node: ast.Subscript):
        """
        功能：
            处理下标访问节点。

        参数说明：
            node:
                ast.Subscript 节点。
        """
        self.visit(node.value)
        self.visit(node.slice)

    def visit_Lambda(self, node: ast.Lambda):
        """
        功能：
            处理 Lambda 表达式。

        参数说明：
            node:
                ast.Lambda 节点。
        """
        self.visit(node.body)

    def visit_comprehension(self, node: ast.comprehension):
        """
        功能：
            处理推导式生成器子句。

        参数说明：
            node:
                ast.comprehension 节点。
        """
        self.visit(node.iter)
        for if_ in node.ifs:
            self.visit(if_)
        self.visit(node.target)

    def generic_visit(self, node):
        """
        功能：
            默认递归访问。

        参数说明：
            node:
                任意 AST 节点。
        """
        super().generic_visit(node)


def _collect_reads_writes(node: ast.AST) -> Tuple[Set[str], Set[str]]:
    """
    功能：
        收集一个 AST 子树中的读写变量集合。

    参数说明：
        node:
            AST 子树根节点。

    返回：
        (reads, writes)。
    """
    c = ReadWriteCollector()
    c.visit(node)
    return c.reads, c.writes


def _normalize_local_names(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> Dict[str, str]:
    """
    功能：
        对函数内部的参数和局部变量进行归一化命名。

    规则：
        - self 保留为 self
        - 参数映射为 arg0, arg1, ...
        - 局部写入变量映射为 v0, v1, ...

    参数说明：
        fn:
            函数或异步函数 AST 节点。

    返回：
        原变量名到归一化名称的映射字典。
    """
    mapping: Dict[str, str] = {}
    arg_index = 0

    def reg_arg(name: str):
        nonlocal arg_index
        if name == "self":
            mapping[name] = "self"
        elif name not in mapping:
            mapping[name] = f"arg{arg_index}"
            arg_index += 1

    args = fn.args
    for a in list(args.posonlyargs) + list(args.args) + list(args.kwonlyargs):
        reg_arg(a.arg)
    if args.vararg:
        reg_arg(args.vararg.arg)
    if args.kwarg:
        reg_arg(args.kwarg.arg)

    class Writer(ast.NodeVisitor):
        """
        功能：
            扫描局部写入变量，用于分配归一化局部变量名。
        """
        def __init__(self):
            """
            功能：
                初始化局部变量编号器。
            """
            self.local_index = 0

        def visit_Name(self, node: ast.Name):
            """
            功能：
                处理写入型 Name 节点。

            参数说明：
                node:
                    ast.Name 节点。
            """
            if isinstance(node.ctx, ast.Store) and node.id not in mapping:
                mapping[node.id] = f"v{self.local_index}"
                self.local_index += 1

    Writer().visit(fn)
    return mapping


def _map_var(name: str, mapping: Dict[str, str]) -> str:
    """
    功能：
        使用归一化映射转换变量名。

    参数说明：
        name:
            原变量名。

        mapping:
            变量名映射表。

    返回：
        归一化后的变量名；若不存在映射则返回原名。
    """
    return mapping.get(name, name)


# =========================
# simplified PDG builder
# =========================

class PDGBuilder:
    """
    功能：
        从函数 AST 构建 simplified PDG。

    边界：
        - 过程内
        - 语句级
        - 局部 def-use
        - 保留 control/data 两类边
        - 忽略跨过程与动态语义
    """
    def __init__(self, fn: ast.FunctionDef | ast.AsyncFunctionDef):
        """
        功能：
            初始化 PDG 构建器。

        参数说明：
            fn:
                函数或异步函数 AST 节点。
        """
        self.fn = fn
        self.var_map = _normalize_local_names(fn)
        self.g = Graph()
        self.last_def: Dict[str, int] = {}
        self.entry = self.g.add_node("ENTRY", is_async=isinstance(fn, ast.AsyncFunctionDef))
        self.exit = self.g.add_node("EXIT")

    def build(self) -> Graph:
        """
        功能：
            构建函数的 simplified PDG。

        返回：
            构建完成的 Graph 对象。
        """
        arg_list = (
            list(self.fn.args.posonlyargs)
            + list(self.fn.args.args)
            + list(self.fn.args.kwonlyargs)
        )
        if self.fn.args.vararg:
            arg_list.append(self.fn.args.vararg)
        if self.fn.args.kwarg:
            arg_list.append(self.fn.args.kwarg)

        for i, a in enumerate(arg_list):
            name = _map_var(a.arg, self.var_map)
            nid = self.g.add_node("PARAM", name=name, pos=i)
            self.g.add_edge(self.entry, nid, "control")
            self.last_def[name] = nid

        self._visit_block(self.fn.body, controller=self.entry)

        for n in self.g.nodes:
            if n.kind == "RETURN":
                self.g.add_edge(n.id, self.exit, "control")
        return self.g

    def _add_data_edges_from_expr(self, expr: Optional[ast.AST], to_nid: int):
        """
        功能：
            从表达式中抽取读取变量，并为其添加到目标节点的数据依赖边。

        参数说明：
            expr:
                表达式 AST。

            to_nid:
                目标节点 id。
        """
        if expr is None:
            return
        reads, _ = _collect_reads_writes(expr)
        for r in reads:
            rr = _map_var(r, self.var_map)
            if rr in self.last_def:
                self.g.add_edge(self.last_def[rr], to_nid, "data")

    def _define_targets(self, targets: List[ast.AST], nid: int):
        """
        功能：
            将赋值目标记录为最新定义点。

        参数说明：
            targets:
                赋值目标列表。

            nid:
                当前定义所在节点 id。
        """
        for t in targets:
            _, writes = _collect_reads_writes(t)
            for w in writes:
                ww = _map_var(w, self.var_map)
                self.last_def[ww] = nid

    def _visit_block(self, stmts: List[ast.stmt], controller: int):
        """
        功能：
            处理一个语句块。

        参数说明：
            stmts:
                语句列表。

            controller:
                当前控制节点 id。
        """
        for stmt in stmts:
            self._visit_stmt(stmt, controller)

    def _visit_stmt(self, stmt: ast.stmt, controller: int):
        """
        功能：
            处理单条语句并将其转换为 simplified PDG 节点和边。

        参数说明：
            stmt:
                单条语句 AST 节点。

            controller:
                当前控制节点 id。
        """
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            nid = self.g.add_node("NESTED_DEF", kind_name=type(stmt).__name__)
            self.g.add_edge(controller, nid, "control")
            return

        if isinstance(stmt, ast.Assign):
            value = stmt.value
            if isinstance(value, ast.Call):
                call_nid = self.g.add_node(
                    "CALL",
                    callee=_callee_name(value.func),
                    base_kind=_base_kind(value.func),
                    attr_depth=_attr_depth(value.func),
                    argc=len(value.args) + len(value.keywords),
                )
                self.g.add_edge(controller, call_nid, "control")
                self._add_data_edges_from_expr(value, call_nid)

                assign_nid = self.g.add_node(
                    "ASSIGN",
                    expr_shape="call",
                    targets=len(stmt.targets),
                )
                self.g.add_edge(controller, assign_nid, "control")
                self.g.add_edge(call_nid, assign_nid, "data")
                self._define_targets(stmt.targets, assign_nid)
            else:
                nid = self.g.add_node("ASSIGN", expr_shape=_expr_shape(value), targets=len(stmt.targets))
                self.g.add_edge(controller, nid, "control")
                self._add_data_edges_from_expr(value, nid)
                self._define_targets(stmt.targets, nid)
            return

        if isinstance(stmt, ast.AnnAssign):
            nid = self.g.add_node("ASSIGN", expr_shape=_expr_shape(stmt.value))
            self.g.add_edge(controller, nid, "control")
            self._add_data_edges_from_expr(stmt.value, nid)
            self._define_targets([stmt.target], nid)
            return

        if isinstance(stmt, ast.AugAssign):
            nid = self.g.add_node("ASSIGN", expr_shape="augassign", op=type(stmt.op).__name__)
            self.g.add_edge(controller, nid, "control")
            self._add_data_edges_from_expr(stmt.value, nid)
            self._add_data_edges_from_expr(stmt.target, nid)
            self._define_targets([stmt.target], nid)
            return

        if isinstance(stmt, ast.Expr):
            value = stmt.value
            if isinstance(value, ast.Call):
                nid = self.g.add_node(
                    "CALL",
                    callee=_callee_name(value.func),
                    base_kind=_base_kind(value.func),
                    attr_depth=_attr_depth(value.func),
                    argc=len(value.args) + len(value.keywords),
                )
            else:
                nid = self.g.add_node("EXPR", expr_shape=_expr_shape(value))
            self.g.add_edge(controller, nid, "control")
            self._add_data_edges_from_expr(value, nid)
            return

        if isinstance(stmt, ast.Return):
            nid = self.g.add_node("RETURN", expr_shape=_expr_shape(stmt.value))
            self.g.add_edge(controller, nid, "control")
            self._add_data_edges_from_expr(stmt.value, nid)
            return

        if isinstance(stmt, ast.If):
            nid = self.g.add_node("IF", test_shape=_expr_shape(stmt.test))
            self.g.add_edge(controller, nid, "control")
            self._add_data_edges_from_expr(stmt.test, nid)
            self._visit_block(stmt.body, controller=nid)
            self._visit_block(stmt.orelse, controller=nid)
            return

        if isinstance(stmt, (ast.For, ast.AsyncFor)):
            nid = self.g.add_node("LOOP", loop_kind="for", is_async=isinstance(stmt, ast.AsyncFor))
            self.g.add_edge(controller, nid, "control")
            self._add_data_edges_from_expr(stmt.iter, nid)
            self._define_targets([stmt.target], nid)
            self._visit_block(stmt.body, controller=nid)
            self._visit_block(stmt.orelse, controller=nid)
            return

        if isinstance(stmt, ast.While):
            nid = self.g.add_node("LOOP", loop_kind="while")
            self.g.add_edge(controller, nid, "control")
            self._add_data_edges_from_expr(stmt.test, nid)
            self._visit_block(stmt.body, controller=nid)
            self._visit_block(stmt.orelse, controller=nid)
            return

        if isinstance(stmt, ast.Try):
            try_nid = self.g.add_node("TRY", handlers=len(stmt.handlers), has_finally=bool(stmt.finalbody))
            self.g.add_edge(controller, try_nid, "control")
            self._visit_block(stmt.body, controller=try_nid)

            for h in stmt.handlers:
                ex_name = _safe_name(h.type.id) if isinstance(h.type, ast.Name) else (
                    _safe_name(h.type.attr) if isinstance(h.type, ast.Attribute) else "unknown"
                )
                h_nid = self.g.add_node("EXCEPT", ex_type=ex_name)
                self.g.add_edge(try_nid, h_nid, "control")
                self._visit_block(h.body, controller=h_nid)

            if stmt.finalbody:
                fin_nid = self.g.add_node("FINALLY")
                self.g.add_edge(try_nid, fin_nid, "control")
                self._visit_block(stmt.finalbody, controller=fin_nid)

            self._visit_block(stmt.orelse, controller=try_nid)
            return

        if isinstance(stmt, ast.Raise):
            nid = self.g.add_node("RAISE", expr_shape=_expr_shape(stmt.exc))
            self.g.add_edge(controller, nid, "control")
            self._add_data_edges_from_expr(stmt.exc, nid)
            return

        if isinstance(stmt, ast.With):
            nid = self.g.add_node("WITH", items=len(stmt.items))
            self.g.add_edge(controller, nid, "control")
            for item in stmt.items:
                self._add_data_edges_from_expr(item.context_expr, nid)
                if item.optional_vars is not None:
                    self._define_targets([item.optional_vars], nid)
            self._visit_block(stmt.body, controller=nid)
            return

        if isinstance(stmt, ast.Assert):
            nid = self.g.add_node("ASSERT", test_shape=_expr_shape(stmt.test))
            self.g.add_edge(controller, nid, "control")
            self._add_data_edges_from_expr(stmt.test, nid)
            self._add_data_edges_from_expr(stmt.msg, nid)
            return

        if isinstance(stmt, (ast.Import, ast.ImportFrom, ast.Pass, ast.Break, ast.Continue)):
            nid = self.g.add_node(type(stmt).__name__.upper())
            self.g.add_edge(controller, nid, "control")
            return

        nid = self.g.add_node("STMT", stmt_type=type(stmt).__name__)
        self.g.add_edge(controller, nid, "control")


def _build_pdg_for_function(src: str) -> Graph:
    """
    功能：
        从函数/方法源码构建 simplified PDG。

    参数说明：
        src:
            函数或方法源码字符串。

    返回：
        对应的 simplified PDG 图。

    异常：
        ValueError:
            当输入不是函数/方法源码时抛出。
    """
    node = _parse_api(src)
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        raise ValueError("该函数仅用于 function/method 源码")
    return PDGBuilder(node).build()


def _build_pdg_for_function_node(node: ast.FunctionDef | ast.AsyncFunctionDef) -> Graph:
    """
    功能：
        从函数/方法 AST 节点构建 simplified PDG。

    参数说明：
        node:
            函数或异步函数 AST 节点。

    返回：
        对应的 simplified PDG 图。
    """
    return PDGBuilder(node).build()


# =========================
# Class summary builder
# =========================

@dataclass
class ClassSummary:
    """
    功能：
        类的摘要表示。

    参数说明：
        name:
            类名。

        fields:
            类字段集合。

        method_graphs:
            方法名到方法 PDG 的映射。

        method_kinds:
            方法名到方法类别的映射。
    """
    name: str
    fields: Set[str]
    method_graphs: Dict[str, Graph]
    method_kinds: Dict[str, str]


def _class_method_kind(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """
    功能：
        判断类方法类别。

    参数说明：
        fn:
            方法 AST 节点。

    返回：
        'instance' / 'static' / 'class' / 'async'。
    """
    names = set()
    for d in fn.decorator_list:
        if isinstance(d, ast.Name):
            names.add(d.id)
        elif isinstance(d, ast.Attribute):
            names.add(d.attr)
    if "staticmethod" in names:
        return "static"
    if "classmethod" in names:
        return "class"
    if isinstance(fn, ast.AsyncFunctionDef):
        return "async"
    return "instance"


def _build_class_summary(src: str) -> ClassSummary:
    """
    功能：
        从类源码构建类摘要。

    参数说明：
        src:
            类源码字符串。

    返回：
        ClassSummary 对象。

    异常：
        ValueError:
            当输入不是类源码时抛出。
    """
    node = _parse_api(src)
    if not isinstance(node, ast.ClassDef):
        raise ValueError("该函数仅用于 class 源码")
    return _build_class_summary_from_node(node)


def _build_class_summary_from_node(node: ast.ClassDef) -> ClassSummary:
    """
    功能：
        从类 AST 节点构建类摘要。

    参数说明：
        node:
            类定义 AST 节点。

    返回：
        ClassSummary 对象。
    """
    fields: Set[str] = set()
    method_graphs: Dict[str, Graph] = {}
    method_kinds: Dict[str, str] = {}

    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            method_kinds[item.name] = _class_method_kind(item)
            method_graphs[item.name] = _build_pdg_for_function_node(item)

            class SelfFieldWriter(ast.NodeVisitor):
                """
                功能：
                    收集 self.xxx 写入字段。
                """
                def visit_Attribute(self, n: ast.Attribute):
                    """
                    功能：
                        处理属性写入节点。

                    参数说明：
                        n:
                            ast.Attribute 节点。
                    """
                    if isinstance(n.ctx, ast.Store) and isinstance(n.value, ast.Name) and n.value.id == "self":
                        fields.add(n.attr)
                    self.generic_visit(n)

            SelfFieldWriter().visit(item)

        elif isinstance(item, ast.Assign):
            for t in item.targets:
                if isinstance(t, ast.Name):
                    fields.add(t.id)
        elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            fields.add(item.target.id)

    return ClassSummary(node.name, fields, method_graphs, method_kinds)


# =========================
# Approximate TGraph Edit Distance
# =========================

def _node_substitution_cost(a: GNode, b: GNode) -> float:
    """
    功能：
        计算两个节点的替换代价。

    参数说明：
        a:
            图节点 a。

        b:
            图节点 b。

    返回：
        范围约为 [0, 1] 的替换代价，越小表示越相似。
    """
    if a.kind != b.kind:
        return 1.0

    ka = a.attrs
    kb = b.attrs
    keys = set(ka) | set(kb)
    if not keys:
        return 0.0

    attr_costs = []
    for k in keys:
        va = ka.get(k)
        vb = kb.get(k)
        if va == vb:
            attr_costs.append(0.0)
        elif va is None or vb is None:
            attr_costs.append(0.5)
        else:
            attr_costs.append(0.35)

    cost = sum(attr_costs) / max(1, len(attr_costs))
    return min(cost, 1.0)


def _node_delete_cost(n: GNode) -> float:
    """
    功能：
        计算节点删除代价。

    参数说明：
        n:
            图节点。

    返回：
        删除代价。
    """
    important = {"ENTRY", "EXIT", "RETURN", "IF", "LOOP", "TRY", "EXCEPT", "RAISE", "CALL"}
    return 1.0 if n.kind in important else 0.7


def _edge_delete_cost(etype: str) -> float:
    """
    功能：
        计算边删除代价。

    参数说明：
        etype:
            边类型。

    返回：
        删除代价。
    """
    return 1.0 if etype == "control" else 0.8


def _greedy_node_matching(g1: Graph, g2: Graph) -> Dict[int, int]:
    """
    功能：
        采用贪心策略为两个图建立节点匹配。

    参数说明：
        g1:
            图 1。

        g2:
            图 2。

    返回：
        g1 节点 id 到 g2 节点 id 的匹配字典。
    """
    unmatched2 = set(n.id for n in g2.nodes)
    match: Dict[int, int] = {}

    for n1 in g1.nodes:
        candidates = [n2 for n2 in g2.nodes if n2.id in unmatched2 and n2.kind == n1.kind]
        if not candidates:
            continue
        best = min(candidates, key=lambda n2: _node_substitution_cost(n1, n2))
        if _node_substitution_cost(n1, best) < 0.95:
            match[n1.id] = best.id
            unmatched2.remove(best.id)

    return match


def _approx_tged_distance(g1: Graph, g2: Graph) -> float:
    """
    功能：
        计算两个图的近似 TGraph Edit Distance。

    参数说明：
        g1:
            图 1。

        g2:
            图 2。

    返回：
        图编辑距离，越小表示越相似。
    """
    match = _greedy_node_matching(g1, g2)

    node_cost = 0.0
    matched2 = set(match.values())
    for n1 in g1.nodes:
        if n1.id in match:
            n2 = g2.nodes[match[n1.id]]
            node_cost += _node_substitution_cost(n1, n2)
        else:
            node_cost += _node_delete_cost(n1)

    for n2 in g2.nodes:
        if n2.id not in matched2:
            node_cost += _node_delete_cost(n2)

    mapped_edges2 = set()
    edge_cost = 0.0
    for s1, t1, e1 in g1.edges:
        if s1 in match and t1 in match:
            mapped = (match[s1], match[t1], e1)
            if mapped in g2.edges:
                mapped_edges2.add(mapped)
            else:
                edge_cost += _edge_delete_cost(e1)
        else:
            edge_cost += _edge_delete_cost(e1)

    for e2 in g2.edges:
        if e2 not in mapped_edges2:
            edge_cost += _edge_delete_cost(e2[2])

    return node_cost + edge_cost


def _graph_similarity(g1: Graph, g2: Graph) -> float:
    """
    功能：
        将图编辑距离归一化为相似度分数。

    参数说明：
        g1:
            图 1。

        g2:
            图 2。

    返回：
        [0, 1] 区间内的相似度分数，越大表示越相似。
    """
    dist = _approx_tged_distance(g1, g2)

    norm = (
        sum(_node_delete_cost(n) for n in g1.nodes)
        + sum(_node_delete_cost(n) for n in g2.nodes)
        + sum(_edge_delete_cost(e[2]) for e in g1.edges)
        + sum(_edge_delete_cost(e[2]) for e in g2.edges)
    )
    if norm == 0:
        return 1.0

    sim = 1.0 - (dist / norm)
    return max(0.0, min(1.0, sim))


# =========================
# Class similarity
# =========================

def _jaccard(a: Set[str], b: Set[str]) -> float:
    """
    功能：
        计算两个集合的 Jaccard 相似度。

    参数说明：
        a:
            集合 a。

        b:
            集合 b。

    返回：
        [0, 1] 区间内的 Jaccard 相似度。
    """
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def _best_bipartite_method_score(c1: ClassSummary, c2: ClassSummary) -> float:
    """
    功能：
        对两个类的方法集合做贪心匹配，并聚合方法相似度。

    参数说明：
        c1:
            类摘要 1。

        c2:
            类摘要 2。

    返回：
        类方法层面的聚合相似度。
    """
    names1 = list(c1.method_graphs.keys())
    names2 = list(c2.method_graphs.keys())
    if not names1 and not names2:
        return 1.0
    if not names1 or not names2:
        return 0.0

    pair_scores: List[Tuple[float, str, str]] = []
    for m1 in names1:
        for m2 in names2:
            s_graph = _graph_similarity(c1.method_graphs[m1], c2.method_graphs[m2])
            s_name = 1.0 if m1 == m2 else 0.0
            s_kind = 1.0 if c1.method_kinds[m1] == c2.method_kinds[m2] else 0.0
            score = 0.75 * s_graph + 0.15 * s_name + 0.10 * s_kind
            pair_scores.append((score, m1, m2))

    pair_scores.sort(reverse=True)
    used1, used2 = set(), set()
    chosen = []
    for score, m1, m2 in pair_scores:
        if m1 in used1 or m2 in used2:
            continue
        used1.add(m1)
        used2.add(m2)
        chosen.append(score)

    penalty_slots = max(len(names1), len(names2))
    return sum(chosen) / penalty_slots if penalty_slots else 1.0


def _class_similarity_from_summary(c1: ClassSummary, c2: ClassSummary) -> float:
    """
    功能：
        基于两个类摘要计算类 API 相似度。

    参数说明：
        c1:
            类摘要 1。

        c2:
            类摘要 2。

    返回：
        [0, 1] 区间内的类相似度。
    """
    s_fields = _jaccard(c1.fields, c2.fields)
    s_methods = _best_bipartite_method_score(c1, c2)
    s_name = 1.0 if c1.name == c2.name else 0.0

    score = 0.15 * s_name + 0.25 * s_fields + 0.60 * s_methods
    return max(0.0, min(1.0, score))


def _class_similarity(src1: str, src2: str) -> float:
    """
    功能：
        计算两个类 API 的相似度。

    参数说明：
        src1:
            类源码 1。

        src2:
            类源码 2。

    返回：
        [0, 1] 区间内的类相似度。
    """
    c1 = _build_class_summary(src1)
    c2 = _build_class_summary(src2)
    return _class_similarity_from_summary(c1, c2)


# =========================
# Representation builder
# =========================

def build_representation(api_src: str) -> Dict[str, Any]:
    """
    功能：
        将 API 源码预处理并编译为可复用表示。

    说明：
        - 若输入是函数/方法，则构建函数 PDG 表示
        - 若输入是类，则构建类摘要表示
        - 返回结果供 similarity_from_representation 直接复用
        - 这样 query / candidate 都只需要编译一次

    参数说明：
        api_src:
            API 源码字符串。

    返回：
        表示字典，格式为：
        {
            "algorithm": "mapBased",
            "api_kind": "class" 或 "function",
            "normalized_source": ...,
            "representation": ...,
            "meta": {...}
        }
    """
    normalized_source = normalize_source(api_src)
    node = _parse_api(normalized_source)
    is_class = _is_class_api(node)

    if is_class:
        assert isinstance(node, ast.ClassDef)
        rep = _build_class_summary_from_node(node)
        return {
            "algorithm": "mapBased",
            "api_kind": "class",
            "normalized_source": normalized_source,
            "representation": rep,
            "meta": {
                "class_name": rep.name,
                "field_count": len(rep.fields),
                "method_count": len(rep.method_graphs),
            },
        }

    assert isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    rep = _build_pdg_for_function_node(node)
    return {
        "algorithm": "mapBased",
        "api_kind": "function",
        "normalized_source": normalized_source,
        "representation": rep,
        "meta": {
            "node_count": len(rep.nodes),
            "edge_count": len(rep.edges),
            "is_async": isinstance(node, ast.AsyncFunctionDef),
        },
    }


def similarity_from_representation(
    repr_a: Dict[str, Any],
    repr_b: Dict[str, Any],
) -> float:
    """
    功能：
        基于两段已编译表示计算 mapBased 相似度。

    说明：
        此函数不再重新 parse、建图或建类摘要，
        而是直接复用 build_representation 的结果。

    参数说明：
        repr_a:
            第一段 API 的已编译表示。

        repr_b:
            第二段 API 的已编译表示。

    返回：
        [0, 1] 区间内的相似度分数。

    异常：
        TypeError:
            当输入表示格式不合法时抛出。

        ValueError:
            当表示不是 mapBased，或两个输入 API 类型不一致时抛出。
    """
    if not isinstance(repr_a, dict) or not isinstance(repr_b, dict):
        raise TypeError("repr_a 和 repr_b 都必须是 dict 类型的表示对象")

    if repr_a.get("algorithm") != "mapBased":
        raise ValueError(f"repr_a 不是 mapBased 表示：{repr_a.get('algorithm')}")
    if repr_b.get("algorithm") != "mapBased":
        raise ValueError(f"repr_b 不是 mapBased 表示：{repr_b.get('algorithm')}")

    kind_a = repr_a.get("api_kind")
    kind_b = repr_b.get("api_kind")
    if kind_a != kind_b:
        raise ValueError("输入保证应为相同 API 类型，但这里检测到一个是类，一个不是类")

    rep_a = repr_a.get("representation")
    rep_b = repr_b.get("representation")

    if kind_a == "class":
        if not isinstance(rep_a, ClassSummary) or not isinstance(rep_b, ClassSummary):
            raise TypeError("class 表示中的 representation 必须是 ClassSummary")
        return _class_similarity_from_summary(rep_a, rep_b)

    if not isinstance(rep_a, Graph) or not isinstance(rep_b, Graph):
        raise TypeError("function 表示中的 representation 必须是 Graph")
    return _graph_similarity(rep_a, rep_b)


# =========================
# Public API
# =========================

def similarity(api_src_a: str, api_src_b: str) -> float:
    """
    功能：
        计算两个 API 源码字符串的相似度。

    说明：
        - 输入必须同类型：要么都是类，要么都不是类
        - 非类对象按函数/方法处理，使用 simplified PDG + 近似 TGED
        - 类对象按类摘要 + 方法级相似度聚合处理
        - 该旧接口内部已改为 build + compare 两阶段流程
        - 在正常使用下，输出应与旧版本保持一致

    参数说明：
        api_src_a:
            API 源码字符串 1。

        api_src_b:
            API 源码字符串 2。

    返回：
        [0, 1] 区间内的相似度分数。

    异常：
        ValueError:
            当两个输入 API 类型不一致时抛出。
    """
    repr_a = build_representation(api_src_a)
    repr_b = build_representation(api_src_b)
    return similarity_from_representation(repr_a, repr_b)
