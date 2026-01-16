import queue
import threading

from loguru import logger


class AsyncLogger:
    def __init__(self):
        self.log_queue = queue.Queue()
        self.is_running = True
        self.log_thread = threading.Thread(target=self.log_worker, daemon=True)
        self.log_thread.start()

    def log_worker(self):
        while self.is_running:
            level, message = self.log_queue.get()

            match level:
                case "INFO":
                    logger.info(message)
                case "DEBUG":
                    logger.debug(message)
                case "ERROR":
                    logger.error(message)
                case "WARNING":
                    logger.warning(message)
                case "SUCCESS":
                    logger.success(message)

            self.log_queue.task_done()

    def async_log(self, level, message):
        self.log_queue.put((level, message))

    def stop(self):
        self.is_running = False
        self.log_thread.join()
