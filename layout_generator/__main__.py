"""
Generate layout dataset from command line interface.

Example: python -m layout_generator --config config.yml
"""

from layout_generator.generator import generate_from_cli
# from layout_generator.print_cli import generate_from_cli

if __name__ == "__main__":
    generate_from_cli()
    