from pathlib import Path
import logging
import argparse

import nbformat
from nbconvert import HTMLExporter
from traitlets.config import Config
from nbconvert.writers import FilesWriter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('build_notebooks')


# ROOT = Path('.').resolve()
ROOT = Path(__file__).parent.resolve()
NB_DIRS = ['Demos', 'HW']
# DOCS = ROOT / 'docs'
# BUILD_DIRECTORY = DOCS / 'content'
NOTEBOOK_TPL = 'assets/templates/notebook.tpl'


def load_notebook(nbf):
    with open(nbf) as f:
        nb = nbformat.read(f, as_version=4)
    return nb


def nb_to_html(nbf, name, tpl=NOTEBOOK_TPL):
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
    c = Config()
    c.HTMLExporter.template_file = tpl
    c.HTMLExporter.preprocessors = [
        'nbconvert.preprocessors.ExecutePreprocessor',
        'nbconvert.preprocessors.ExtractOutputPreprocessor'
    ]
    html_exporter = HTMLExporter(config=c)
    (body, resources) = html_exporter.from_notebook_node(nb, resources)

    writer = FilesWriter()
    writer.build_directory = nbf_path
    writer.write(body, resources, notebook_name=name)


def build_nb(nbdir, limit=None):
    notebooks = [
        nbf
        for nbf in nbdir.glob('**/*.ipynb')
        if not nbf.match('*checkpoint*')
    ]
    if limit is not None:
        notebooks = notebooks[:limit]
    for nbf in notebooks:
        name = nbf.stem.replace(' - ', '_').replace(' ', '_').lower()
        nb_to_html(nbf, name)


TEST_NBDIR = "Demos/pythag"
parser = argparse.ArgumentParser(description='Build Jupyter Notebooks to HTML.')
parser.add_argument('--test', action='store_const', const=TEST_NBDIR,
                    help='Default Notebook to test')


def main():
    args = parser.parse_args()
    if args.test is not None:
        nbdir = Path(args.test)
        build_nb(nbdir, limit=1)
    else:
        for d in NB_DIRS:
            build_nb(ROOT / d)


if __name__ == "__main__":
    main()
