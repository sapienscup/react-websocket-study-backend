from fastapi import Depends


def fake():
    pass


get_database_session_dependency = Depends(fake)
