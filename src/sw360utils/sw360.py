# SPDX-License-Identifier: MIT
# Copyright (c) Helio Chissini de Castro <heliocastro@gmail.com>
from __future__ import annotations

import logging
import sys
from typing import Any

import click
import requests
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.logging import RichHandler
from rich.pretty import pprint


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SW360_", case_sensitive=True, env_file=".env")

    HOST: str = "http://localhost:8080"
    USER: str | None = None
    PASSWORD: str | None = None


class SW360Utils:
    def __init__(self) -> None:
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        settings: Settings = Settings()

        msgformat = "%(message)s"
        logging.basicConfig(
            level="NOTSET",
            format=msgformat,
            datefmt="[%X]",
            handlers=[RichHandler()],
        )
        self.log = logging.getLogger("rich")

        self.host: str = settings.HOST

        if not settings.USER:
            self.log.error("Missing user !")
            sys.exit(1)
        self.user: str = settings.USER

        if not settings.PASSWORD:
            self.log.error("Missing password !")
            sys.exit(1)
        self.password: str = settings.PASSWORD

    def list_credentials(self) -> Any:
        response = requests.get(
            f"{self.host}/authorization/client-management",
            headers=self.headers,
            auth=(self.user, self.password),
            timeout=3600,
        )

        self.log.info(response.status_code)
        if response.status_code == 200:
            data: Any = response.json()
            pprint(data)
        else:
            self.log.error("Cant connect")
            return
        return data

    def delete_credentials(self, client_id: str | None = None, all_credentials: bool = False) -> None:
        ids: list[str] = []
        if client_id:
            ids.append(client_id)

        if all_credentials:
            ids.clear()
            for credential in self.list_credentials():
                ids.append(credential["client_id"])

        for credential_id in ids:
            response = requests.delete(
                f"{self.host}/authorization/client-management/{credential_id}",
                headers=self.headers,
                auth=(self.user, self.password),
                timeout=3600,
            )
            print(f"Deleted id {id} with status {response.status_code}")

    def create_api_id(self, api_id: str) -> None:
        data = {
            "description": api_id,
            "authorities": ["BASIC"],
            "scope": ["READ", "WRITE"],
            "access_token_validity": 31536000,
            "refresh_token_validity": 31536000,
        }

        response = requests.post(
            f"{self.host}/authorization/client-management",
            headers=self.headers,
            auth=(self.user, self.password),
            json=data,
            timeout=3600,
        )

        self.log.info(response.status_code)
        if response.status_code == 200:
            data = response.json()
            pprint(data)
        else:
            self.log.error("Cant connect")

    def get_token(self, api_id: str) -> None:
        for credentials in self.list_credentials():
            if credentials["description"] == api_id:
                params = {
                    "grant_type": "password",
                    "username": self.user,
                    "password": self.password,
                }
                auth = (credentials["client_id"], credentials["client_secret"])
                logging.debug(auth)
                logging.debug(params)
                response = requests.get(
                    f"{self.host}/authorization/oauth/token",
                    headers=self.headers,
                    auth=auth,
                    params=params,
                    timeout=3600,
                )

                data = response.json()
                ort_config = {
                    "type": "SW360",
                    "options": {
                        "restUrl": f"{self.host}/resource/api",
                        "authUrl": f"{self.host}/resource/api/authorization/client-management",
                    },
                    "secrets": {
                        "username": self.user,
                        "password": self.password,
                        "clientId": credentials["client_id"],
                        "clientPassword": credentials["client_secret"],
                        "token": data["access_token"],
                    },
                }

                print(yaml.dump(data=ort_config, sort_keys=False))


@click.group()
def cli() -> None:
    pass


@click.command()
@click.argument("api_id", default="PLATOSS")
def create_api_id(api_id: str) -> None:
    SW360Utils().create_api_id(api_id)


@click.command()
def list_credentials() -> None:
    SW360Utils().list_credentials()


@click.command()
@click.argument("api_id", default="PLATOSS")
def get_token(api_id: str) -> None:
    SW360Utils().get_token(api_id)


@click.command()
@click.option("--all", default=False, type=bool, is_flag=True)
@click.option("--client_id", type=str, default=None)
def delete_credentials(all_credentials: bool, client_id: str | None = None) -> None:
    SW360Utils().delete_credentials(client_id, all_credentials)


cli.add_command(create_api_id)
cli.add_command(list_credentials)
cli.add_command(get_token)
cli.add_command(delete_credentials)

if __name__ == "__main__":
    cli()
