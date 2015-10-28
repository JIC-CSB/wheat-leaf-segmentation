import os.path

from jicbioimage.core.image import DataManager
from jicbioimage.core.io import FileBackend

HERE = os.path.dirname(os.path.realpath(__file__))

def get_microscopy_collection(input_file):
    """Return microscopy collection from input file."""
    data_dir = os.path.abspath(os.path.join(HERE, "..", "data"))
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    backend_dir = os.path.join(data_dir, 'unpacked')
    file_backend = FileBackend(backend_dir)
    data_manager = DataManager(file_backend)
    microscopy_collection = data_manager.load(input_file)
    return microscopy_collection
