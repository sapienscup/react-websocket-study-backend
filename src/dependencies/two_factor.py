from typing import Annotated

from fastapi import Depends, Header

from src.services.two_factor.auth import TwoFactorAuth


async def verify_two_factor(totp_code: Annotated[str, Header()] = "fake-super-secret-token"):
    if totp_code == "fake-super-secret-token":
        return

    return TwoFactorAuth().perform(totp_code)

two_factor_dependency = Depends(verify_two_factor)
