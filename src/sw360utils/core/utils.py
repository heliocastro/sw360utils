# SPDX-License-Identifier: MIT
# Copyright (c) Helio Chissini de Castro <heliocastro@gmail.com>

from __future__ import annotations

import sys
from typing import Any

import requests

from sw360utils import logging, settings

headers: dict[str, str] = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def sw360_api_post(data: dict[str, Any], endpoint: str = "authorization/client-management") -> requests.Response:
    if not settings.USER or not settings.PASSWORD:
        logging.error("User and Password not provided.")
        sys.exit(1)

    response = requests.post(
        f"{settings.HOST}/{endpoint}",
        headers=headers,
        auth=(settings.USER, settings.PASSWORD),
        json=data,
        timeout=3600,
    )

    return response


def sw360_api_get(
    endpoint: str = "authorization/client-management",
    params: dict[str, Any] | None = None,
    auth: tuple[Any, Any] = (settings.USER, settings.PASSWORD),
) -> requests.Response:
    if not settings.USER or not settings.PASSWORD:
        logging.error("User and Password not provided.")
        sys.exit(1)

    response = requests.get(
        f"{settings.HOST}/{endpoint}",
        headers=headers,
        auth=auth,
        params=params,
        timeout=3600,
    )

    return response


def sw360_api_delete(endpoint: str = "authorization/client-management") -> requests.Response:
    if not settings.USER or not settings.PASSWORD:
        logging.error("User and Password not provided.")
        sys.exit(1)

    response = requests.delete(
        f"{settings.HOST}/{endpoint}",
        headers=headers,
        auth=(settings.USER, settings.PASSWORD),
        timeout=3600,
    )

    return response
