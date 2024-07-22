# SPDX-License-Identifier: MIT
# Copyright (c) Helio Chissini de Castro <heliocastro@gmail.com>

from __future__ import annotations

import click
import yaml
from rich.pretty import pprint

from sw360utils import settings
from sw360utils.commands.api_id import list_credentials
from sw360utils.core.cmdgroup import cli
from sw360utils.core.utils import sw360_api_get


@click.group()
def credentials() -> None:
    pass


@click.command(name="ort")
@click.argument("client_id")
def config_ort(client_id: str) -> None:
    for cred in list_credentials():
        if cred["client_id"] == client_id:
            params = {
                "grant_type": "password",
                "username": settings.USER,
                "password": settings.PASSWORD,
            }
            auth = (cred["client_id"], cred["client_secret"])
            response = sw360_api_get(
                endpoint="authorization/oauth/token",
                params=params,
                auth=auth,
            )

            data = response.json()
    
            ort_config = {
                "type": "SW360",
                "options": {
                    "restUrl": f"{settings.HOST}/resource/api",
                    "authUrl": f"{settings.HOST}/resource/api/authorization/client-management",
                },
                "secrets": {
                    "username": settings.USER,
                    "password": settings.PASSWORD,
                    "clientId": cred["client_id"],
                    "clientPassword": cred["client_secret"],
                    "token": data["access_token"],
                },
            }

            print(yaml.dump(data=ort_config, sort_keys=False))


credentials.add_command(config_ort)
cli.add_command(credentials)
cli.add_command(credentials)
