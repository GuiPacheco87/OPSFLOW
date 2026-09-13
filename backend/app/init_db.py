from .database import Base,engine
from . import models  # noqa: F401
Base.metadata.create_all(engine)

