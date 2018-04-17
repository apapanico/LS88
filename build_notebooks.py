from pathlib import Path
import logging
import argparse

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
parser.add_argument('--template', dest='tpl',
                    help='Notebook Jinja template')

# ROOT = Path('.').resolve()
ROOT = Path(__file__).parent.resolve()
NB_DIRS = ['Demos', 'HW']
DEFAULT_TPL = 'assets/templates/notebook.tpl'


def load_notebook(nbf):
    with open(nbf) as f:
        nb = nbformat.read(f, as_version=4)
    return nb


def nb_to_html(nbf, name, tpl, extout=True):
    nbf_path = str(nbf.parent)
    resources = {
        'output_files_dir': f'img/{name}',
        'metadata': {'path': nbf_path}
    }
    logger.info(f"Resources: {resources}")

    # Open into notebook node format
    nb = load_notebook(nbf)

    # Check if not intended to be executable
    if not nb['metadata'].get('is_executable', True):
        logger.info(f"skipping (not executable) {nbf}")
        return

    if nb.cells[0]['metadata'].get('toc', False):
        nb.cells.pop(0)

    logger.info(f"executing {nbf}")

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
    writer.build_directory = nbf_path
    writer.write(body, resources, notebook_name=name)


def build_nb(nbdir, limit=None, tpl=None, extout=True):
    tpl = tpl or DEFAULT_TPL
    logger.info(f"Using template {tpl}")
    if extout:
        logger.info(f"Extracting output")

    notebooks = [
        nbf
        for nbf in nbdir.glob('**/*.ipynb')
        if not nbf.match('*checkpoint*')
    ]
    if limit is not None:
        notebooks = notebooks[:limit]
    for nbf in notebooks:
        name = nbf.stem.replace(' - ', '_').replace(' ', '_').lower()
        nb_to_html(nbf, name, tpl, extout=extout)


def main():
    args = parser.parse_args()
    extout = args.extout
    tpl = args.tpl
    if args.test is not None:
        nbdir = Path(args.test)
        build_nb(nbdir, limit=1, tpl=tpl, extout=extout)
    else:
        for d in NB_DIRS:
            build_nb(ROOT / d, tpl=tpl, extout=extout)


if __name__ == "__main__":
    main()
