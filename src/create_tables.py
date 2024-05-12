from database import Base, engine, session_factory
from users.models import *
with session_factory() as session:
    Base.metadata.create_all(bind=engine)
    session.commit()
