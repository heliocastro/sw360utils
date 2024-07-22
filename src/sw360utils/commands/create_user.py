# SPDX-License-Identifier: MIT
# Copyright (c) Helio Chissini de Castro <heliocastro@gmail.com>

from __future__ import annotations

import click
import requests
from requests.auth import HTTPBasicAuth

from sw360utils import logging, settings
from sw360utils.core.cmdgroup import cli

user_client_data: dict[str, str] = {
    "type": "user",
    "email": "test.client@sw360.org",
    "userGroup": "USER",
    "externalid": "z1234567",
    "fullname": "Test Client",
    "givenname": "Test",
    "lastname": "Client",
    "department": "DEPARTMENT",
    "wantsMailNotification": "true",
    "deactivated": "false",
    "issetBitfield": "1",
}


@click.command()
@click.option("--email", "-e", default="user@sw360.org")
@click.option("--admin", "-a", is_flag=True, default=False)
@click.option("--login", "-l", default="user")
def create_user(email: str, login: str, admin: bool) -> None:
    data = user_client_data

    data["email"] = email
    data["userGroup"] = "ADMIN" if admin else "USER"
    logging.info(data)

    response = requests.put(
        f"{settings.COUCHDB_HOST}/sw360oauthclients/e82d846d5cf00995f944651c23001f91",
        json=data,
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth(settings.COUCHDB_USER, settings.COUCHDB_PASSWORD),
        timeout=60,
    )

    if response.status_code == 200:
        logging.info("Users created successfully.")
    else:
        logging.error(f"Error occurred while creating Users: {response.json().get('error')}")


cli.add_command(create_user)
