from typing import Annotated

from fastapi import Depends, Header, HTTPException


async def verify_token(x_token: Annotated[str, Header()] = "fake-super-secret-token"):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


get_token_header_dependency = Depends(verify_token)
