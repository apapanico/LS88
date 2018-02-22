# Test execution of notebooks

# TODO
#  + Research programmatic execution of notebooks for raising exceptions


from pathlib import Path
import json
import hashlib

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError

VERBOSE = False

ROOT = Path(__file__).resolve().parents[1]
DIRSKIP = [ROOT / 'tests', ROOT / 'data']

NB_TEST_CACHE = ROOT / 'tests' / '.nb_test_cache'

if NB_TEST_CACHE.exists():
    with open(NB_TEST_CACHE) as fp:
        nb_test_cache = {}
        lines = fp.read().splitlines()
        for line in lines:
            k, v = line.split(':')
            nb_test_cache[k] = v
else:
    nb_test_cache = {}


def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data.encode('utf-8'))
    return md5.digest().hex()


def test_notebooks():
    notebooks_to_test = list(ROOT.glob('**/*.ipynb'))
    for nb_f in notebooks_to_test:
        # Skip directories
        if any(skip in nb_f.parents for skip in DIRSKIP):
            if VERBOSE:
                print(f"skipping (skipped dir) {nb_f}")
            continue

        # Skip checkpoints
        if nb_f.match('*checkpoint*'):
            if VERBOSE:
                print(f"skipping (checkpoint) {nb_f}")
            continue

        # Hash and check if cached
        with open(nb_f) as fp:
            nb_hash = md5_for_file(fp)

        if nb_hash == nb_test_cache.get(str(nb_f)):
            if VERBOSE:
                print(f"skipping (cached test) {nb_f}")
            continue

        # Open into notebook node format
        with open(nb_f) as f:
            nb = nbformat.read(f, as_version=4)

        # Check if not intended to be executable
        if not nb['metadata'].get('is_executable', True):
            if VERBOSE:
                print(f"skipping (not executable) {nb_f}")
            continue

        # Execute
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        try:
            if VERBOSE:
                print(f"testing {nb_f}")
            ep.preprocess(nb, {'metadata': {'path': str(nb_f.parent)}})
        except CellExecutionError as e:
            msg = 'Error executing the notebook "%s".\n\n' % nb_f
            print(msg)
            raise e
        # Store to hash cache
        nb_test_cache[str(nb_f)] = nb_hash

    with open(NB_TEST_CACHE, 'w') as fp:
        if VERBOSE:
            print(f"storing hash cache")
        for k in nb_test_cache:
            fp.write(k + ":" + nb_test_cache[k] + "\n")
