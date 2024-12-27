import logging
import os
from os.path import split, join, normpath, abspath
from sys import stdout

use_file_handler = True
use_terminal_handler = False

if not os.path.exists("../../src/logging/"):
    os.makedirs("../../src/logging/")

unit_tests_log_file_name = "../logging/unit_tests_log.txt"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# file handler
if use_file_handler:
    file_log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s', "%Y-%m-%d %H:%M:%S")
    dirname, filename = split(abspath(__file__))
    unit_tests_log_path = normpath(join(dirname, unit_tests_log_file_name))
    file_log_handler = logging.FileHandler(unit_tests_log_path, mode='w')
    file_log_handler.setFormatter(file_log_formatter)
    logger.addHandler(file_log_handler)

# terminal handler
if use_terminal_handler:
    terminal_log_formatter = logging.Formatter('%(message)s')
    terminal_log_handler = logging.StreamHandler(stdout)
    terminal_log_handler.setFormatter(terminal_log_formatter)
    logger.addHandler(terminal_log_handler)
