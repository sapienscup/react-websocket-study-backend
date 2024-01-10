import logging

logging.basicConfig()
logger = logging.getLogger()


async def fake_middleware(request, call_next):
    logger.info(request)
    logger.info(call_next)
    return await call_next(request)
