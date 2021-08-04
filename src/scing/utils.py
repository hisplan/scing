import os
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


def download_from_github(
    name: str,
    version: str,
    download_url: str,
    path_base_dest: str,
    git_auth_token: str,
    skip_exists: bool = True,
):
    os.makedirs(path_base_dest, exist_ok=True)

    path_dest = os.path.join(path_base_dest, f"{name}-{version}.tgz")

    # skip if file exists and skip_exists=true
    if os.path.exists(path_dest) and skip_exists == True:
        return path_dest

    cmd = [
        "curl",
        "-L",
        "-o",
        path_dest,
        "-H",
        f"Authorization: token {git_auth_token}",
        download_url,
    ]

    logger.info(" ".join(cmd))

    exit_code = run_command2(cmd)

    if exit_code != 0:
        raise_error("curl failed!")

    return path_dest


def extract_targzip(name: str, version: str, targzip: str, path_base_dest: str):

    path_dest = os.path.join(path_base_dest, f"{name}-{version}")

    os.makedirs(path_dest, exist_ok=True)

    cmd = ["tar", "xzf", targzip, "-C", path_dest, "--strip-components", "1"]

    exit_code, stdout, stderr = run_command(cmd)

    if exit_code != 0:
        raise_error("tar xzf failed!")

    stdout = stdout.decode()
    stderr = stderr.decode()

    if stdout:
        logger.info(stdout)

    if stderr:
        logger.error(stderr)

    return path_dest
