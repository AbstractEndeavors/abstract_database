from .config import *
from .functions import *
from .image import *
from .legacy import *
from .metadata import *
from .solana import *
from .tables import *
from .templates import *
from .time import *
from .rows import *
from .toggle import *
from .build import *
def select_one(query, *args):
    rows = select_rows(query, *args)
    return get_rows(rows)
