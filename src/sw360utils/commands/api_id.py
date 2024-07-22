# SPDX-License-Identifier: MIT
# Copyright (c) Helio Chissini de Castro <heliocastro@gmail.com>

from __future__ import annotations

from typing import Any

import click
from rich.pretty import pprint

from sw360utils import logging, settings
from sw360utils.core.cmdgroup import cli
from sw360utils.core.utils import sw360_api_delete, sw360_api_get, sw360_api_post


@click.group()
def api_id() -> None:
    pass


def list_credentials() -> Any:
    response = sw360_api_get()

    logging.info(response.status_code)
    if response.status_code == 200:
        data: Any = response.json()
        return data
    else:
        logging.error(f"Error code: {response.status_code}")
        return []


@click.command(name="list")
def api_list_credentials() -> None:
    data = list_credentials()
    pprint(data)


@click.command(name="create")
@click.argument("api_id")
def api_create(api_id: str) -> None:
    if not settings.USER or not settings.PASSWORD:
        logging.error("User and Password not provided.")
        return
    data = {
        "description": api_id,
        "authorities": ["BASIC"],
        "scope": ["READ", "WRITE"],
        "access_token_validity": 31536000,
        "refresh_token_validity": 31536000,
    }

    response = sw360_api_post(data)

    logging.info(response.status_code)
    if response.status_code == 200:
        data = response.json()
        pprint(data)
    else:
        logging.error("Cant connect to SW360 instance.")


@click.command(name="delete")
@click.argument("client_id", required=False)
@click.option("--all-ids", is_flag=True)
def api_delete(all_ids: bool, client_id: str) -> None:
    if not client_id:
        logging.error("No Client ID defined.")
        return
    ids: list[str] = []
    if client_id:
        ids.append(client_id)

    if all_ids:
        ids.clear()
        for credential in api_list_credentials():
            ids.append(credential["client_id"])

    for credential_id in ids:
        response = sw360_api_delete(endpoint=f"authorization/client-management/{credential_id}")
        pprint(response)


api_id.add_command(api_create)
api_id.add_command(api_delete)
api_id.add_command(api_list_credentials)
cli.add_command(api_id)
