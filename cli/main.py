import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import cli.commands

from nubia import Nubia

if __name__ == "__main__":
    shell = Nubia(
        name="CLI Sucden",
        command_pkgs=cli.commands)

    sys.exit(shell.run())
