# SPDX-License-Identifier: MIT
# Copyright (c) Helio Chissini de Castro <heliocastro@gmail.com>

from __future__ import annotations

import logging as pylogging

from rich.logging import RichHandler

from sw360utils.core.settings import Settings

msgformat = "%(message)s"
pylogging.basicConfig(
    level="NOTSET",
    format=msgformat,
    datefmt="[%X]",
    handlers=[RichHandler()],
)
logging: pylogging.Logger = pylogging.getLogger("rich")

settings: Settings = Settings()
