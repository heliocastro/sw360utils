from __future__ import annotations

from sw360utils.core.cmdgroup import cli


def main() -> None:
    from sw360utils import commands  # noqa: F401

    cli()


if __name__ == "__main__":
    main()
