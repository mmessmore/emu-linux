#!/usr/bin/env python3

import errno
import os
import sys

import click
import yaml
from sh import sudo


try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


@click.command()
@click.option("-c", "--config-file", type=click.File('r'),
              default="config.yaml")
def cli(config_file):
    config = yaml.load(config_file, Loader=Loader)
    partition(config)


def partition(config):
    for disk in config['disks']:
        add_label(disk["source"], disk["table"])


def add_label(device, ltype):
    if not os.path.exists(device):
        error(f"device: {device} does not exist", exit=errno.ENOENT)
    command("parted", device, "mklabel", ltype)


def command(*args, require=True):
    try:
        sudo(*args)
    except sh.ErrorReturnCode as e:
        if require:
            error(f"Command failed: {e.full_cmd}")
            click.secho("STDOUT", fg="green")
            click.echo(e.stdout)
            click.secho("STDERR", fg="red")
            click.echo(e.stderr, file=sys.stderr)
            sys.exit(e.exit_code)
        return e.exit_code
    return 0


def error(msg, exit=-1):
    click.secho(f"Error: {msg}", fg="red")
    if exit >= 0:
        sys.exit(exit)


if __name__ == '__main__':
    cli()
