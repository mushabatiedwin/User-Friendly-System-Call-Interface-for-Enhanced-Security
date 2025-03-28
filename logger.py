from loguru import logger
import datetime

def log_system_call(username, command, output):
    with open("system_calls.log", "a") as log_file:
        log_file.write(f"[{datetime.datetime.now()}] {username} executed '{command}' -> {output}\n")


logger.add("system_calls.log", format="{time} {level} {message}", level="INFO", rotation="10 MB")

def log_system_call(username, command, output):
    logger.info(f"User: {username} | Command: {command} | Output: {output}")
