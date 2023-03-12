from .movies import api as movies_ns
from .directors import api as directors_ns
from .genres import api as genres_ns
from .favorites import api as favorites_ns

__all__ = [
    'movies_ns',
    'directors_ns',
    'genres_ns',
    'favorites_ns'
]

