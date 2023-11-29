import logging
import time

from cassandra.cqlengine.connection import register_connection, set_default_connection

from src.infra.cass.conn import CassConn

logging.basicConfig()
logger = logging.getLogger()


async def fake_middleware(request, call_next):
    logger.info(request)
    logger.info(call_next)

    with CassConn().perform() as context:
        register_connection(str(context), session=context)
        set_default_connection(str(context))
        return await call_next(request)


def cassandra_middleware(crud_action):
    def wrapper():
        start_time = time.time()

        with CassConn().perform() as context:
            register_connection(str(context), session=context)
            set_default_connection(str(context))
            crud_action()

        end_time = time.time()

        msg = f"[{crud_action.__name__}]\ntotal time: {str(end_time - start_time)}\n"
        logger.info(msg)

    return wrapper
