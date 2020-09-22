import sys

from sh import sudo
from sh import ErrorReturnCode
from click import echo, secho


def sudo_commandex(*args):
    try:
        res = sudo(*args)
    except ErrorReturnCode as e:
        secho(f"ERROR: Command failed: {e.full_cmd}")
        echo("\nSTDOUT")
        echo(e.stdout)
        echo("\nSTDERR")
        echo(e.stderr)
        sys.exit(e.exit_code)
    return res
