"""Logger helper file
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import multiprocessing
import os
import socket
import traceback
from ctypes import c_int
from logging import LoggerAdapter
from logging import _nameToLevel
from logging.handlers import QueueHandler
from logging.handlers import TimedRotatingFileHandler

_extra_dict = {
    "IP": socket.gethostbyname(socket.gethostname()),
    "HOST": socket.gethostname(),
    "KEYWORD": ""
}

worker_info_log_template = "status=%s\tid=%s\tcost=%.4f\tinfo=%s"
worker_err_log_template = ("code=%s\tstatus=%s\tid=%s\tcost=%.4f\terr=%s\t"
                           "trace=%s")
rpc_info_log_template = "status=%s\tid=%s\trequest=%s\tresponse=%s\tcost=%.4f"
rpc_err_log_template = ("code=%s\tstatus=%s\tid=%s\trequest=%s\tresponse=%s\t"
                        "cost=%.4f\terr=%s\ttrace=%s")
debug_log_template = "debug_info\t%s=%s"
LOG_TRUNCATE_LENGTH = 100

# use the default date format, '%Y-%m-%d %H:%M:%S', '%s,%03d'
_formatter = logging.Formatter(
    "%(IP)s -- [%(asctime)s] [%(name)s] [%(filename)s(%(lineno)d)] "
    "[%(levelname)s] #%(KEYWORD)s# %(message)s")

# add the "DEBUG" element for debug.
_levels_to_record = ("DEBUG", "INFO", "WARNING", "ERROR")


class NotSetupError(Exception):
    pass


class PhoenixLogAdapter(LoggerAdapter):

    _mutex = multiprocessing.Lock()
    _is_set_up = multiprocessing.Value(c_int, 0)
    _queue = None
    _listener_process = None
    _handlers = list()

    @classmethod
    def _get_hierarchical_handlers(cls, log_dir="", file_name=""):
        # create the log_dir
        if log_dir and not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        handlers = list()
        if file_name:
            for level in _levels_to_record:
                log_file_path = "{}/{}.log.{}".format(
                    log_dir, file_name, level)
                log_handler = TimedRotatingFileHandler(
                    log_file_path, backupCount=180, encoding="utf-8",
                    when='midnight')
                log_handler.suffix = "%Y-%m-%d"
                log_handler.setLevel(_nameToLevel[level])
                log_handler.setFormatter(_formatter)
                handlers.append(log_handler)
        # add console output in debug mode
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(_formatter)
        handlers.append(console_handler)
        return handlers

    @classmethod
    def _get_logger_with_handlers(cls, logger_name, handlers):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        if logger.hasHandlers():
            return logger
        for handler in handlers:
            logger.addHandler(handler)
        return logger

    @classmethod
    def listener_process(cls, file_name, log_dir):
        handlers = cls._get_hierarchical_handlers(file_name, log_dir)
        logger_lp = cls._get_logger_with_handlers("listener_process", handlers)
        while True:
            try:
                record = cls._queue.get()
                # We send this as a sentinel to tell the listener to quit.
                if record is None:
                    break
                logger = cls._get_logger_with_handlers(record.name, handlers)
                logger.handle(record)
                # No level or filter logic applied - just do it!
            except Exception as e:
                logger_lp.error(worker_err_log_template % (
                    "31000", "logger_process_resolve_record_error",
                    "listener_process", -1, str(e), traceback.format_exc()))

    @classmethod
    def setup(cls, file_name="", log_dir="", multiprocess=True):
        """Setup the LoggerAdapter
        :param file_name: file to store the logs
        :param log_dir: the dir to put the log file.
        :param multiprocess: is the logger run in multiprocessing env or not.
        :return:

        Note:
            1, 当使用多进程时，请确保先在主进程中调用一下 setup
                否则会有两个后果:
                一，listener_process 可能无法赋值；
                二，子进程退出时导致 listener_process 退出.
        """
        with cls._mutex:
            if cls._is_set_up.value > 0:
                cls._is_set_up.value += 1
                return

            if multiprocess:
                cls._queue = multiprocessing.Manager().Queue(-1)
                # listen process for log processing.
                listener = multiprocessing.Process(
                    target=cls.listener_process, args=(file_name, log_dir))
                listener.start()
                cls._listener_process = listener
                # setup the handler
                log_handler = QueueHandler(cls._queue)
                log_handler.setLevel(logging.DEBUG)
                log_handler.setFormatter(_formatter)
                cls._handlers.append(log_handler)
            else:
                cls._handlers.extend(
                    cls._get_hierarchical_handlers(file_name, log_dir))
            cls._is_set_up.value = 1

    @classmethod
    def getLogger(cls, logger_name):
        """Get Logger
        :param logger_name:     logger name (file name as well)
        :return: an PhoenixLogAdapter
        """
        with cls._mutex:
            if cls._is_set_up.value == 0:
                raise NotSetupError("Should complete the setup first.")
            logger = cls._get_logger_with_handlers(logger_name, cls._handlers)
            logger_adapter = PhoenixLogAdapter(logger, _extra_dict)
            return logger_adapter

    @classmethod
    def exit(cls):
        """Exit the logger, clean the queue and listener process.

        Note:
        For non multi-processing situation, no need to call this method.

        For the multi-processing situation, need to call this method, or the
        main process would not exit.
        Because the queue and listener process is shared between processes,
        so make sure the last processing to call the exit.

        :return:
        """
        with cls._mutex:
            cls._is_set_up.value -= 1
            if cls._is_set_up.value > 0:
                return
            if cls._listener_process:
                cls._queue.put_nowait(None)
                cls._listener_process.join()
                cls._listener_process = None
                cls._queue = None
            cls._handlers.clear()
            cls._is_set_up.value = 0

    def process(self, msg, kwargs):
        if "extra" not in kwargs:
            kwargs["extra"] = self.extra
        else:
            user_extra = kwargs["extra"]
            for (k, v) in self.extra.items():
                if k not in user_extra:
                    user_extra[k] = v
            kwargs["extra"] = user_extra
        return msg, kwargs
