from django.template import Engine
from django.test.utils import TestTemplateLoader
import inspect


def main():
    templates_dict = {
        'test_template.html': 'Hello, {{ name }}!'
    }

    engine = Engine()

    loader = TestTemplateLoader(engine, templates_dict)

    print("-----getsource_output-----")
    print(inspect.getsource(type(loader)))


if __name__ == "__main__":
    main()
