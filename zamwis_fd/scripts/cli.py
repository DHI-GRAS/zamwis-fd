import datetime
import logging

import click

from zamwis_fd import chain

logging.basicConfig(format='%(module)s - %(message)s', level=logging.INFO)


@click.command()
@click.argument('outdir', type=click.Path(exists=True))
@click.option(
    '--startdate', help='Download query start date YYYYMMDD (default: a year ago)')
@click.option(
    '--enddate', help='Download query end date YYYYMMDD (default: today)')
@click.option(
    '--download/--no-download', default=True,
    help='Attempt to download new files (default: True)')
@click.option(
    '--update-longterm-stats/--no-update-longterm-stats', default=True,
    help='Update longterm statistics (default: True)')
@click.option(
    '--split/--no-split', default=True,
    help='Split downloaded data into GeoTIFF for PostGIS import (default: True)')
def main(startdate, enddate, **kwargs):
    """Download and process NDVI, SWI10, and TRMM for ZAMWIS database"""

    if enddate is None:
        enddate = datetime.datetime.now()

    if startdate is None:
        startdate = enddate - datetime.timedelta(days=365)

    chain.main(startdate=startdate, enddate=enddate, **kwargs)
