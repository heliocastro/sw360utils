# SPDX-License-Identifier: MIT
# Copyright (c) Helio Chissini de Castro <heliocastro@gmail.com>

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SW360_", case_sensitive=True, env_file=".env")

    HOST: str = "http://localhost:8080"
    USER: str | None = None
    PASSWORD: str | None = None
    COUCHDB_USER: str = "admin"
    COUCHDB_PASSWORD: str = "password"
    COUCHDB_HOST: str = "http://localhost:5984"
