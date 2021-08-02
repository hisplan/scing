import sys
import subprocess
import logging
from scing.error import raise_error


logger = logging.getLogger()


def run_command(cmd: list, cwd: str = None):

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd
    )

    stdout, stderr = process.communicate()

    return process.returncode, stdout, stderr


def run_command2(cmd: list, cwd: str = None):
    "run a command and return (stdout, stderr, exit code)"

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, shell=False
    )

    for line in iter(process.stdout.readline, b""):
        line = line.decode(sys.stdout.encoding).rstrip() + "\r"
        logger.info(line)

    process.communicate()

    return process.returncode


def run_shell(cmd):
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )

    stdout, stderr = process.communicate()

    stdout = stdout.decode().strip()
    stderr = stderr.decode().strip()

    return process.returncode, stdout, stderr


def get_shell_variable(path_config: str, var_name: str) -> str:

    exit_code, value, _ = run_shell(
        f"bash -c 'source {path_config}; echo ${var_name}'",
    )

    if exit_code != 0:
        raise_error(f"Unable to read config={path_config}' var={var_name}...")

    return value
