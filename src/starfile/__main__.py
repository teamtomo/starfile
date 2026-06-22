"""Command-line interface for STAR file reading and inspection."""

try:
    import click
    from IPython.terminal.embed import InteractiveShellEmbed
except ImportError:
    deps = False
else:
    deps = True


if deps:

    @click.command()  # type: ignore[misc]
    @click.argument("path", type=click.Path(exists=True, dir_okay=False, readable=True))  # type: ignore[misc]
    @click.option("--read_n_blocks", type=int)  # type: ignore[misc]
    @click.option("--always_dict", is_flag=True)  # type: ignore[misc]
    def cli(path: str, read_n_blocks: int | None, always_dict: bool) -> None:
        """Read a star file and open an ipython console to inspect contents."""
        from pathlib import Path

        from .functions import read

        _ = read(Path(path), read_n_blocks, always_dict)

        banner = """=== Starfile ===
    - access your data with `data`
    - write it out with `write(...)`
    - read more with `read(...)`
        """
        sh = InteractiveShellEmbed.instance(banner2=banner)
        sh()

else:

    def cli() -> None:
        """Print installation instructions."""
        print(
            "To use the command line utility, install with "
            "`pip install starfile[cli]`"
        )
