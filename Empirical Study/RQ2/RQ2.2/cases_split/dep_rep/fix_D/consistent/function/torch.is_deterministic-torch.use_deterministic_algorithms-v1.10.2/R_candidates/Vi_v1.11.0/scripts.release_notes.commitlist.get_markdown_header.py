def get_markdown_header(category):
    header = f"""
# Release Notes worksheet {category}

The main goal of this process is to rephrase all the commit messages below to make them clear and easy to read by the end user. You should follow the following instructions to do so:

* **Please cleanup, and format commit titles to be readable by the general pytorch user.** [Detailed intructions here](https://fb.quip.com/OCRoAbEvrRD9#HdaACARZZvo)
* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Please drop any commits that are not user-facing.
* If anything is from another domain, leave it in the UNTOPICED section at the end and I'll come and take care of it.

The categories below are as follows:

* BC breaking: All commits that are BC-breaking. These are the most important commits. If any pre-sorted commit is actually BC-breaking, do move it to this section. Each commit should contain a paragraph explaining the rational behind the change as well as an example for how to update user code (guidelines here: https://quip.com/OCRoAbEvrRD9)
* Deprecations: All commits introducing deprecation. Each commit should include a small example explaining what should be done to update user code.
* new_features: All commits introducing a new feature (new functions, new submodule, new supported platform etc)
* improvements: All commits providing improvements to existing feature should be here (new backend for a function, new argument, better numerical stability)
* bug fixes: All commits that fix bugs and behaviors that do not match the documentation
* performance: All commits that are added mainly for performance (we separate this from improvements above to make it easier for users to look for it)
* documentation: All commits that add/update documentation
* Developers: All commits that are not end-user facing but still impact people that compile from source, develop into pytorch, extend pytorch, etc
"""

    return [header, ]
