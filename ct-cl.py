import sys
import click
from mixcr import MiXCR


@click.command()
@click.option('--file1', help='FASTQ file 1.')
@click.option('--file2', help='FASTQ file 2.')
@click.option('--molecule', default='IGH', help='Molecule.')
@click.option('--out', help='Output directory.')
def cmd(file1, file2, molecule, out):
    if file1 is None:
        sys.exit("f1 is required.")
    if file2 is None:
        sys.exit("f2 is required.")
    if out is None:
        sys.exit("out is required.")
    mx = MiXCR(file1=file1, file2=file2, molecule=molecule, output_directory=out)
    mx.run()


if __name__ == "__main__":
    cmd()
