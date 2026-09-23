import ast
from typing import Optional, Tuple
from urllib.parse import urlparse, urlunparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


_session = None


def get_session() -> requests.Session:
    """
    功能：
        创建并复用全局 requests.Session，挂载重试策略。

    参数：
        无

    返回：
        配置好重试机制的 Session 对象
    """
    global _session
    if _session is not None:
        return _session

    session = requests.Session()

    retry = Retry(
        total=5,                 # 总重试次数
        connect=5,               # 连接失败重试次数
        read=5,                  # 读取失败重试次数
        backoff_factor=1.0,      # 指数退避: 1s, 2s, 4s, 8s...
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(["GET"]),
        raise_on_status=False,
    )

    adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # 可选：统一请求头
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; api-source-fetcher/1.0)"
    })

    _session = session
    return _session


def github_blob_to_raw(url: str) -> str:
    """
    功能：
        将 GitHub 的 blob 链接转换为 raw 资源链接。

    参数：
        url: 形如
             https://github.com/owner/repo/blob/version/path/to/file.py

    返回：
        对应的 raw 链接字符串
    """
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")

    # 期望格式: owner / repo / blob / version / path...
    if len(parts) < 5 or parts[2] != "blob":
        raise ValueError(f"不是合法的 GitHub blob 链接: {url}")

    owner = parts[0]
    repo = parts[1]
    version = parts[3]
    file_parts = parts[4:]

    raw_path = f"/{owner}/{repo}/{version}/" + "/".join(file_parts)
    raw_url = urlunparse(("https", "raw.githubusercontent.com", raw_path, "", "", ""))
    return raw_url


def _strip_fragment(url: str) -> str:
    """
    功能：
        删除 URL 末尾 # 开头的片段信息。

    参数：
        url: 原始 url

    返回：
        去掉 fragment 后的 url
    """
    return url.split("#", 1)[0]


def _parse_fqn(fqn: str, api_type: int) -> Tuple[int, str, Optional[str], str]:
    """
    功能：
        解析 fqn，得到分段数、展示名、类名、API名。

    参数：
        fqn: 全限定名
        api_type: 1 函数, 2 类, 3 方法

    返回：
        (count, display_name, class_name, api_name)
        - count: fqn 的分段数
        - display_name:
            type=1/2 时为最后一段
            type=3 时为最后两段拼接，例如 ClassName.method_name
        - class_name:
            仅 type=3 时有值
        - api_name:
            实际要匹配的函数名/类名/方法名
    """
    parts = fqn.split(".")
    count = len(parts)

    if api_type == 1:
        return count, parts[-1], None, parts[-1]
    elif api_type == 2:
        return count, parts[-1], None, parts[-1]
    elif api_type == 3:
        if len(parts) < 2:
            raise ValueError(f"方法类型的 fqn 至少需要两段: {fqn}")
        class_name = parts[-2]
        method_name = parts[-1]
        return count, f"{class_name}.{method_name}", class_name, method_name
    else:
        raise ValueError(f"不支持的 type: {api_type}")


def _replace_version_in_github_url(url: str, fqn_count: int, version: str, api_type: int = 1) -> str:
    """
    功能：
        按规则替换 GitHub URL 中的版本段：
        1. 对于 api_type=3（方法类型），优先尝试替换倒数第 count 段
        2. 对于其他类型，优先尝试替换倒数第 count+1 段
        3. 如果替换位置明显不合理，则兜底替换 blob 后面的版本段

    参数：
        url: 去掉 fragment 后的 GitHub blob 链接
        fqn_count: fqn 分段数
        version: 目标版本字符串
        api_type: API 类型，1 函数, 2 类, 3 方法

    返回：
        替换后的目标版本链接
    """
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")

    if not parts:
        raise ValueError(f"URL path 为空: {url}")

    if api_type == 3:
        target_idx = len(parts) - fqn_count
    else:
        target_idx = len(parts) - (fqn_count + 1)

    def looks_like_bad_version_position(idx: int) -> bool:
        if idx < 0 or idx >= len(parts):
            return True
        bad_tokens = {"blob", "tree", "raw", "github.com", "raw.githubusercontent.com"}
        return parts[idx] in bad_tokens

    if looks_like_bad_version_position(target_idx):
        if "blob" in parts:
            blob_idx = parts.index("blob")
            if blob_idx + 1 >= len(parts):
                raise ValueError(f"GitHub blob 链接缺少版本段: {url}")
            target_idx = blob_idx + 1
        else:
            raise ValueError(f"无法定位版本段: {url}")

    new_parts = parts[:]
    new_parts[target_idx] = version

    new_path = "/" + "/".join(new_parts)
    new_url = urlunparse(
        (parsed.scheme, parsed.netloc, new_path, parsed.params, parsed.query, "")
    )
    return new_url


def _fetch_code_from_github_blob(url: str, timeout: int = 20) -> str:
    """
    功能：
        将 GitHub blob 链接转为 raw 链接并爬取源码，使用 Session 和重试机制。

    参数：
        url: GitHub blob 链接
        timeout: 请求超时时间

    返回：
        文件源码字符串
    """
    raw_url = github_blob_to_raw(url)
    session = get_session()
    resp = session.get(raw_url, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def _node_start_lineno(node: ast.AST) -> int:
    """
    功能：
        获取节点源码的起始行号。
        如果有装饰器，起始行号取第一个装饰器的行号。

    参数：
        node: AST 节点

    返回：
        起始行号，1-based
    """
    lineno = node.lineno
    decorator_list = getattr(node, "decorator_list", None)
    if decorator_list:
        lineno = min(d.lineno for d in decorator_list)
    return lineno


def _extract_source_segment(code: str, node: ast.AST) -> str:
    """
    功能：
        从原始 code 中提取 AST 节点对应的源码。

    参数：
        code: 完整源码
        node: AST 节点

    返回：
        该节点的源码字符串
    """
    if hasattr(node, "end_lineno") and node.end_lineno is not None:
        lines = code.splitlines(keepends=True)
        start = _node_start_lineno(node) - 1
        end = node.end_lineno
        return "".join(lines[start:end])

    segment = ast.get_source_segment(code, node)
    if segment is None:
        raise ValueError("无法从 AST 节点提取源码片段")
    return segment


def _find_top_level_function(tree: ast.Module, name: str):
    """
    功能：
        查找模块顶层同名函数。

    参数：
        tree: AST 模块树
        name: 函数名

    返回：
        对应节点，找不到返回 None
    """
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
    return None


def _find_class(tree: ast.Module, name: str):
    """
    功能：
        查找模块中的同名类。

    参数：
        tree: AST 模块树
        name: 类名

    返回：
        对应节点，找不到返回 None
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    return None


def _find_method_in_class(class_node: ast.ClassDef, method_name: str):
    """
    功能：
        在类中查找同名方法。

    参数：
        class_node: 类节点
        method_name: 方法名

    返回：
        对应节点，找不到返回 None
    """
    for node in class_node.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == method_name:
            return node
    return None


def _find_top_level_function_py2(tree, name: str):
    """
    功能：
        (Python 2 兜底) 查找模块顶层同名函数。

    参数：
        tree: parso 模块树
        name: 函数名

    返回：
        对应节点，找不到返回 None
    """
    if not hasattr(tree, 'children'):
        return None
    for node in tree.children:
        if getattr(node, 'type', '') == 'funcdef' and getattr(node.name, 'value', '') == name:
            return node
        if getattr(node, 'type', '') == 'decorated' and hasattr(node, 'children'):
            for child in node.children:
                if getattr(child, 'type', '') == 'funcdef' and getattr(child.name, 'value', '') == name:
                    return node
                if hasattr(child, 'children'):
                    for grandchild in child.children:
                        if getattr(grandchild, 'type', '') == 'funcdef' and getattr(grandchild.name, 'value', '') == name:
                            return node
    return None


def _find_class_py2(tree, name: str):
    """
    功能：
        (Python 2 兜底) 查找模块中的同名类。

    参数：
        tree: parso 模块树
        name: 类名

    返回：
        对应节点，找不到返回 None
    """
    def walk_parso(node):
        yield node
        if hasattr(node, 'children'):
            for child in node.children:
                for n in walk_parso(child):
                    yield n

    for node in walk_parso(tree):
        if getattr(node, 'type', '') == 'classdef' and getattr(node.name, 'value', '') == name:
            return node
    return None


def _find_method_in_class_py2(class_node, method_name: str):
    """
    功能：
        (Python 2 兜底) 在类中查找同名方法。

    参数：
        class_node: parso 类节点
        method_name: 方法名

    返回：
        对应节点，找不到返回 None
    """
    def walk_parso(node):
        yield node
        if hasattr(node, 'children'):
            for child in node.children:
                for n in walk_parso(child):
                    yield n

    for node in walk_parso(class_node):
        if getattr(node, 'type', '') == 'funcdef' and getattr(node.name, 'value', '') == method_name:
            return node
    return None


def get_api_source_by_url_fqn_version_type(
    url: str,
    fqn: str,
    version: str,
    api_type: int,
    timeout: int = 20,
) -> str:
    """
    功能：
        根据 url、fqn、version、type：
        1. 去掉 url 中的 # 行号片段
        2. 解析 fqn，得到 count 和 API 名称
        3. 生成目标版本的 GitHub 链接
        4. 拉取目标版本源码
        5. AST 解析并提取同名 API 的源码。遇到 Python 2 语法不兼容时，使用 parso 兜底解析。

    参数：
        url: 原始 GitHub blob 链接，可能带 #Lxx-Lyy
        fqn: API 全限定名
        version: 目标版本
        api_type: 1 函数, 2 类, 3 方法
        timeout: 网络请求超时时间

    返回：
        目标 API 的源码字符串
    """
    clean_url = _strip_fragment(url)
    count, display_name, class_name, api_name = _parse_fqn(fqn, api_type)
    target_url = _replace_version_in_github_url(clean_url, count, version, api_type)
    code = _fetch_code_from_github_blob(target_url, timeout=timeout)
    
    try:
        tree = ast.parse(code)
        is_py2 = False
    except SyntaxError:
        try:
            import parso
        except ImportError:
            raise ImportError("遇到不兼容的 Python 2 语法，请先执行 `pip install parso` 安装兜底解析库。")
        tree = parso.parse(code, version="2.7")
        is_py2 = True

    if is_py2:
        if api_type == 1:
            node = _find_top_level_function_py2(tree, api_name)
            if node is None:
                raise ValueError(f"未找到同名函数(Py2): {display_name}")
            return node.get_code()

        elif api_type == 2:
            node = _find_class_py2(tree, api_name)
            if node is None:
                raise ValueError(f"未找到同名类(Py2): {display_name}")
            return node.get_code()

        elif api_type == 3:
            if class_name is None:
                raise ValueError("方法类型缺少类名")
            class_node = _find_class_py2(tree, class_name)
            if class_node is None:
                raise ValueError(f"未找到所属类(Py2): {class_name}")

            method_node = _find_method_in_class_py2(class_node, api_name)
            if method_node is None:
                raise ValueError(f"在类 {class_name} 中未找到同名方法(Py2): {api_name}")

            return method_node.get_code()

        else:
            raise ValueError(f"不支持的 type: {api_type}")
    else:
        if api_type == 1:
            node = _find_top_level_function(tree, api_name)
            if node is None:
                raise ValueError(f"未找到同名函数: {display_name}")
            return _extract_source_segment(code, node)

        elif api_type == 2:
            node = _find_class(tree, api_name)
            if node is None:
                raise ValueError(f"未找到同名类: {display_name}")
            return _extract_source_segment(code, node)

        elif api_type == 3:
            if class_name is None:
                raise ValueError("方法类型缺少类名")
            class_node = _find_class(tree, class_name)
            if class_node is None:
                raise ValueError(f"未找到所属类: {class_name}")

            method_node = _find_method_in_class(class_node, api_name)
            if method_node is None:
                raise ValueError(f"在类 {class_name} 中未找到同名方法: {api_name}")

            return _extract_source_segment(code, method_node)

        else:
            raise ValueError(f"不支持的 type: {api_type}")
