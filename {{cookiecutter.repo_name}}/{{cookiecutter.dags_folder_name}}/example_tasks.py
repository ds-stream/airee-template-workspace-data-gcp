import time
import logging


def sleep_task(sec: int, **context):
    logging.info("Wait 10s")
    for i in range(sec):
        time.sleep(1)
        logging.info(f"{i+1}s passed")
