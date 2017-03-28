import datetime
import logging
import click

from . import workflow

logging.basicConfig(format='%(module)s - %(message)s', level=logging.INFO)

@click.command()
@click.argument('outdir', type=click.Path(exists=True))
@click.option('--startdate', help='Download query start date YYYYMMDD (default: a year ago)')
@click.option('--enddate', help='Download query end date YYYYMMDD (default: today)')
@click.option('--download/--no-download', default=True, help='Attempt to download new files (default: True)')
@click.option('--update-longterm-stats/--no-update-longterm-stats', default=True, help='Update longterm statistics (default: True)')
@click.option('--split/--nosplit', default=True, help='Split downloaded data into GeoTIFF for PostGIS import (default: True)')
def main(outdir, startdate=None, enddate=None, split=True):
    """Download and process NDVI, SWI10, and TRMM for ZAMWIS database"""

    if enddate is None:
        enddate = datetime.datetime.now().strftime('%Y%m%d')

    if startdate is None:
        startdate = datetime.datetime.strptime(enddate, '%Y%m%d') - datetime.timedelta(days=365)
        startdate = startdate.strftime('%Y%m%d')

    workflow.update_products(outdir=outdir, startdate=startdate, enddate=enddate, split=split)

if __name__ == '__main__':

    main()
