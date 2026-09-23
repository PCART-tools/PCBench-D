def _compare_docs(old_func, new_func):
    old_doc = inspect.getdoc(old_func)
    new_doc = inspect.getdoc(new_func)
    index = new_doc.index('\n\n') + 2
    assert_equal(new_doc[index:], old_doc)
