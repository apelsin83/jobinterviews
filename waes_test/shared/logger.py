import logging

def setup_logger(logger_name, log_file, level=logging.INFO):
    # init logging into file
    log = logging.getLogger(logger_name)
    log.setLevel(level)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    file_handler = logging.FileHandler(log_file, mode='aw')
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
