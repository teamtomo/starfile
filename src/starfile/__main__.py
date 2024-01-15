try:
    from IPython.terminal.embed import InteractiveShellEmbed
    import click
except ImportError:
    deps = False
else:
    deps = True


if deps:
    @click.command()
    @click.argument('path', type=click.Path(exists=True, dir_okay=False, readable=True))
    @click.option('--read_n_blocks', type=int)
    @click.option('--always_dict', is_flag=True)
    def cli(path, read_n_blocks, always_dict):
        """
        Read a star file and open an ipython console to interactively inspect its contents
        """
        # imports here will be available in the embedded shell
        from .functions import read, write

        star = read(path, read_n_blocks, always_dict)

        banner = '''=== Starfile ===
    - access your data with `star`
    - write it out with `write(...)`
    - read more with `read(...)`
        '''
        # sh.instance() needed due to reggression in ipython
        # https://github.com/ipython/ipython/issues/13966#issuecomment-1696137868
        sh = InteractiveShellEmbed.instance(banner2=banner)
        sh()
else:
    def cli():
        print('To use the command line utility, install with `pip install starfile[cli]`')
