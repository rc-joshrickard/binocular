"""Command-line interface."""
import fire

from .binocular import Binocular


def main():
    """Main entry point for the command line interface of Binocular."""
    fire.Fire(Binocular)


if __name__ == "__main__":
    main()
