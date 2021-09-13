try:
    from IPython.terminal.embed import InteractiveShellEmbed
    import click
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:
    deps = False
else:
    deps = True


if deps:
    from .functions import read, write

    @click.command()
    @click.argument('path', type=click.Path(exists=True, dir_okay=False, readable=True))
    @click.option('--read_n_blocks', type=int)
    @click.option('--always_dict', is_flag=True)
    def cli(path, read_n_blocks, always_dict):
        """
        Read a star file and open an ipython console to interactively inspect its contents
        """
        star = read(path, read_n_blocks, always_dict)

        banner = '''=== Starfile ===
    - access your data with `star`
    - write it out with `write(...)`
        '''
        sh = InteractiveShellEmbed(banner2=banner)
        sh.push('star')
        sh()
else:
    def cli():
        print('To use the command line utility, install with `pip install starfile[cli]`')
