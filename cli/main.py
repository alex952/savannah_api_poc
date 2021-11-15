import sys
sys.path.append("/Users/alex952/sucden/sucden_poc")

import cli.commands

from nubia import Nubia, Options

if __name__ == "__main__":
    shell = Nubia(
        name="CLI Sucden",
        command_pkgs=cli.commands)

    sys.exit(shell.run())
