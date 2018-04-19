from pathlib import Path
import logging
import argparse
import json
import hashlib

import nbformat
from nbconvert import HTMLExporter
from traitlets.config import Config
from nbconvert.writers import FilesWriter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('build_notebooks')


TEST_NBDIR = "Demos/pythag"
parser = argparse.ArgumentParser(description='Build Jupyter Notebooks to HTML.')
parser.add_argument('--test', action='store_const', const=TEST_NBDIR,
                    help='Default Notebook to test')
parser.add_argument('--extract-output', action='store_true', dest='extout',
                    help='Extract figures from notebooks')
parser.add_argument('--do-not-use-contentdir', action='store_false',
                    dest='no_use_contentdir',
                    help='Use content/ to store html notebooks')
parser.add_argument('--template', dest='tpl',
                    help='Notebook Jinja template')

# ROOT = Path('.').resolve()
ROOT = Path(__file__).parent
NB_DIRS = ['Demos', 'HW']
DEFAULT_TPL = 'assets/templates/notebook.tpl'
CONTENT_DIR = ROOT / 'content'


NB_BUILD_CACHE = ROOT / '.nb_build_cache'

if NB_BUILD_CACHE.exists():
    with open(NB_BUILD_CACHE) as fp:
        nb_build_cache = json.load(fp)
else:
    nb_build_cache = {}


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


def nb_to_html(nb, name, tpl, path, build_dir, extout=True):
    resources = {
        'output_files_dir': f'img/{name}',
        'metadata': {'path': path}
    }
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
    writer.build_directory = build_dir
    writer.write(body, resources, notebook_name=name)


def build_nb(notebooks, limit=None, tpl=None, extout=True, use_contentdir=True):
    tpl = tpl or DEFAULT_TPL
    logger.info(f"Using template {tpl}")
    if extout:
        logger.info(f"Extracting output")
    for nbf in notebooks:
        name = nbf.stem.replace(' - ', '_').replace(' ', '_').lower()

        nbf_path = nbf.resolve().parent
        if use_contentdir:
            build_path = (CONTENT_DIR / nbf.parent).relative_to(ROOT)
        else:
            build_path = nbf_path

        # Open into notebook node format
        nb = load_notebook(nbf)

        if is_notebook_cached(nbf):
            logger.info(f"skipping (cached test) {name}")
            continue

        # Check if not intended to be executable
        if not nb['metadata'].get('is_executable', True):
            logger.info(f"skipping (not executable) {name}")
            continue

        nb_to_html(nb, name, tpl, str(nbf_path), str(build_path), extout=extout)
        cache_notebook(nbf)


def main():
    args = parser.parse_args()
    extout = args.extout
    tpl = args.tpl
    contentdir = args.no_use_contentdir

    if args.test is not None:
        nbdir = ROOT / Path(args.test)
        notebooks = [
            (nbdir, nbf.relative_to(nbdir))
            for nbf in nbdir.glob('**/*.ipynb')
            if not nbf.match('*checkpoint*')
        ][:1]
    else:
        notebooks = []
        for nbdir in NB_DIRS:
            nbdir = ROOT / nbdir
            notebooks.extend([
                nbf.relative_to(ROOT)
                for nbf in nbdir.glob('**/*.ipynb')
                if not nbf.match('*checkpoint*')
            ])

    build_nb(notebooks, tpl=tpl, extout=extout, use_contentdir=contentdir)

    with open(NB_BUILD_CACHE, 'w') as fp:
        logger.info("storing hash cache")
        json.dump(nb_build_cache, fp)


if __name__ == "__main__":
    main()
