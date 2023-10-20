import click
import json
import tabulate

from typing import Any, Dict, List


def output_json(values: List[Dict[str, Any]]) -> None:
    click.echo(json.dumps(values, indent=2))


def output_table(values: List[Dict[str, Any]]) -> None:
    if len(values):
        header = values[0].keys()
        rows = [x.values() for x in values]
        click.echo(tabulate.tabulate(rows, header))
