from pathlib import Path
import logging
import argparse
import json
import hashlib

from jinja2 import Template
import nbformat
from nbconvert import HTMLExporter
from traitlets.config import Config
from nbconvert.writers import FilesWriter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('build_notebooks')

# ROOT = Path('.').resolve()
ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / 'content'
HTML_DIR = ROOT / 'html'
NB_DIRS = ['Demos', 'HW']
DEFAULT_TPL = 'templates/notebook.tpl'

HOME_LOCAL = str(ROOT.resolve())
HOME_REMOTE = '/LS88'
NAVBAR_DEFAULT = 'html/nav_content.html'
TEST_NB = "content/Demos/esv/Shot Location Demo (DS).ipynb"
NB_BUILD_CACHE = ROOT / '.nb_build_cache'


if NB_BUILD_CACHE.exists():
    with open(NB_BUILD_CACHE) as fp:
        nb_build_cache = json.load(fp)
else:
    nb_build_cache = {}


parser = argparse.ArgumentParser(description='Build Jupyter Notebooks to HTML.')
parser.add_argument('--test', action='store_const', const=TEST_NB,
                    help='Default Notebook to test')
parser.add_argument('--force', action='store_true',
                    help='Force notebook build')
parser.add_argument('--extract-output', action='store_true', dest='extout',
                    help='Extract figures from notebooks')
parser.add_argument('--do-not-use-htmldir', action='store_false',
                    dest='no_use_htmldir',
                    help='Use html/ to store html notebooks')
parser.add_argument('--template', dest='tpl',
                    help='Notebook Jinja template')
parser.add_argument('--local-home', action='store_const', const=HOME_LOCAL,
                    default=HOME_REMOTE, help='Home directory')
parser.add_argument('--navbar', default=NAVBAR_DEFAULT, help='Home directory')


def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data.encode('utf-8'))
    return md5.digest().hex()


def load_notebook(nbf):
    with open(nbf) as f:
        nb = nbformat.read(f, as_version=4)
    return nb


def is_notebook_cached(nbf):
    # Hash and check if cached
    with open(nbf) as fp:
        nb_hash = md5_for_file(fp)
    return (nb_hash == nb_build_cache.get(str(nbf)))


def cache_notebook(nbf):
    # Hash and check if cached
    with open(nbf) as fp:
        nb_hash = md5_for_file(fp)

    nb_build_cache[str(nbf)] = nb_hash


def nb_to_html(nb, name, tpl, path, build_dir, context, extout=True):
    resources = {
        'output_files_dir': f'img/{name}',
        'metadata': {'path': path},
        'build_directory': build_dir.lower()
    }
    resources['context'] = context
    logger.info(f"Resources: {resources}")

    if nb.cells[0]['metadata'].get('toc', False):
        nb.cells.pop(0)

    logger.info(f"executing {name}")

    preprocessors = ['nbconvert.preprocessors.ExecutePreprocessor']
    if extout:
        preprocessors.append(
            'nbconvert.preprocessors.ExtractOutputPreprocessor'
        )
    c = Config()
    c.HTMLExporter.template_file = tpl
    c.HTMLExporter.preprocessors = preprocessors
    html_exporter = HTMLExporter(config=c)
    (body, resources) = html_exporter.from_notebook_node(nb, resources)

    writer = FilesWriter()
    writer.build_directory = build_dir.lower()
    writer.write(body, resources, notebook_name=name)


def build_nb(notebooks, context={}, limit=None, tpl=None, extout=True,
             use_htmldir=True, force=False):
    tpl = tpl or DEFAULT_TPL
    logger.info(f"Using template {tpl}")
    if extout:
        logger.info(f"Extracting output")
    for nbf in notebooks:
        name = nbf.stem.replace(' - ', '_').replace(' ', '_').lower()

        nbf_path = nbf.resolve().parent
        if use_htmldir:
            build_path = HTML_DIR / \
                nbf.parent.resolve().relative_to(CONTENT_DIR)
        else:
            build_path = nbf_path

        # Open into notebook node format
        nb = load_notebook(nbf)

        if not force and is_notebook_cached(nbf):
            logger.info(f"skipping (cached build) {name}")
            continue

        # Check if not intended to be executable
        if not nb['metadata'].get('is_executable', True):
            logger.info(f"skipping (not executable) {name}")
            continue

        nb_to_html(nb, name, tpl, str(nbf_path), str(build_path),
                   context, extout=extout)
        cache_notebook(nbf)


def main():
    args = parser.parse_args()
    extout = args.extout
    tpl = args.tpl
    htmldir = args.no_use_htmldir
    force = args.force

    navbar_tpl = Template(open(args.navbar, 'r').read())
    navbar_str = navbar_tpl.render(home=args.local_home)
    context = {
        'home': args.local_home,
        'navbar': navbar_str
    }

    if args.test is not None:
        notebooks = [Path(TEST_NB)]
    else:
        notebooks = []
        for nbdir in NB_DIRS:
            nbdir = CONTENT_DIR / nbdir
            notebooks.extend([
                nbf
                for nbf in nbdir.glob('**/*.ipynb')
                if not nbf.match('*checkpoint*')
            ])

    build_nb(notebooks, context=context, tpl=tpl, extout=extout,
             use_htmldir=htmldir, force=force)

    with open(NB_BUILD_CACHE, 'w') as fp:
        logger.info("storing hash cache")
        json.dump(nb_build_cache, fp)


if __name__ == "__main__":
    main()
