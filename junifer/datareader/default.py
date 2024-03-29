# Authors: Federico Raimondo <f.raimondo@fz-juelich.de>
# License: AGPL

from pathlib import Path

import nibabel as nib
import pandas as pd

from ..utils.logging import logger
from ..markers.base import PipelineStepMixin

# Map each filenanm end to a kind
_extensions = {
    '.nii': 'NIFTI',
    '.nii.gz': 'NIFTI',
    '.csv': 'CSV',
    '.tsv': 'TSV'

}

# Map each kind to a function and arguments
_readers = {}
_readers['NIFTI'] = dict(func=nib.load, params=None)
_readers['CSV'] = dict(func=pd.read_csv, params=None)
_readers['TSV'] = dict(func=pd.read_csv, params={'sep': '\t'})


class DefaultDataReader(PipelineStepMixin):

    def validate_input(self, input):
        # Nothing to validate, any input is fine
        pass

    def get_output_kind(self, input):
        # It will output the same kind of data as the input
        return input

    def fit_transform(self, input, params=None):
        # For each kind of data, try to read it
        out = {}
        if params is None:
            params = {}
        for kind in input.keys():
            t_path = input[kind]
            t_params = params.get(kind, {})
            if not isinstance(t_path, Path):
                t_path = Path(t_path)
            out[kind] = {'path': t_path}
            fread = None

            fname = t_path.name.lower()
            for ext, ftype in _extensions.items():
                if fname.endswith(ext):
                    logger.info(f'Reading {ftype} file {t_path.as_posix()}')
                    reader_func = _readers[ftype]['func']
                    reader_params = _readers[ftype]['params']
                    if reader_params is not None:
                        t_params.update(reader_params)
                    logger.debug(f'Calling {reader_func} with {t_params}')
                    fread = reader_func(t_path, **t_params)
                    break
            if fread is None:
                logger.info(
                    f'Unknown file type {t_path.as_posix()}, skipping reading')
            out[kind]['data'] = fread
        return out
