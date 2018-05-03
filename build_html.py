from pathlib import Path
import argparse

import yaml
from jinja2 import Environment, Template, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
CONTENT_LOAD = ['navbar', 'body_content']
CONTEXT_FILE = 'build.yml'


parser = argparse.ArgumentParser(description='Build Jupyter Notebooks to HTML.')
parser.add_argument('--test', action='store_true', help='Test')
# parser.add_argument('--home', help='Home directory')


def load_contexts(context_file=CONTEXT_FILE):
    contexts = yaml.load_all(open(context_file, 'r').read())
    base_context = next(contexts)
    return base_context, contexts


def main():
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    base_context, contexts = load_contexts()

    for context in contexts:
        context.update(base_context)
        # context['home'] = args.home or context['home']
        if args.test:
            context['filename'] = context['filename'].replace(
                '.html', '_test.html')
        context['path'] = ROOT / context['path']
        tpl = env.get_template(context['template'])

        for k in CONTENT_LOAD:
            context[k] = open(context[k], 'r').read()

        tpl_tmp = Template(tpl.render(context))
        s = tpl_tmp.render(context)

        output_f = context['path'] / context['filename']
        with open(output_f, 'w') as fp:
            fp.write(s)


if __name__ == "__main__":
    main()
