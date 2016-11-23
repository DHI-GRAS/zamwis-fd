import os
import glob
import shutil
import logging
import tempfile

from flooddrought.ingestion import download_ndvi
from flooddrought.ingestion import download_swi
from flooddrought.ingestion import download_trmm

from flooddrought.indices import update_stats
from flooddrought.indices import calc_ndvi
from flooddrought.indices import calc_swi

from flooddrought.indices import save_spi_stats
from flooddrought.indices import calc_rain

from flooddrought.tools import utils as fdutils
from flooddrought.tools import gdal_utils as gu

from . import split_netcdf

logger = logging.getLogger('zamwis.workflow')


def _split_to_gtiff(outfiles, splitdir, extents,
        firstyear=None, lastyear=None):
    """Help function for GeoTIFF export"""
    # define file patterns
    to_split = {
            'NDVI': ['ndvi_????.nc', os.path.join('indices', '*_anomaly_????.nc')],
            'SWI': ['swi_????.nc', os.path.join('indices', '*_deviation_????.nc')],
            'TRMM': [
                'trmm_????.nc',
                os.path.join('indices', '*_1_month_????.nc'),
                os.path.join('indices', '*_3_month_????.nc'),
                os.path.join('indices', '*_6_month_????.nc')]}

    # loop through products
    for product in outfiles:
        # loop through patterns for each product
        for pattern in to_split[product]:
            productdir = os.path.dirname(outfiles[product])
            fn_pattern = os.path.join(productdir, pattern)
            infiles = sorted(glob.glob(fn_pattern))
            if not infiles:
                logger.warn('No files found for pattern \'{}\'.'.format(fn_pattern))
                continue
            # define output dir
            outdir = os.path.join(splitdir, product, os.path.basename(infiles[0])[:-8])
            try:
                os.makedirs(outdir)
            except OSError:
                pass
            tempdir = tempfile.mkdtemp()
            try:
                # re-process only latest year of nc files
                try:
                    # try sub-setting infiles
                    infiles = fdutils.filter_yearly_files(infiles, firstyear, lastyear)
                except (AttributeError, TypeError, ValueError) as err:
                    # use full list
                    logger.warn('Splitting all available netCDF data ({}).'.format(str(err)))
                    pass
                # split
                tempfiles = split_netcdf.main_multifile(infiles, tempdir, unscale=True, fname_fmt='%Y%m%d0000.tif')

                # make sure that the extent perfectly matches requested
                for fname in tempfiles:
                    outfile = os.path.join(outdir, os.path.basename(fname))
                    gu.warp(fname, outfile, r='bilinear', extent=extents[product])
            finally:
                shutil.rmtree(tempdir)


def update_products(outdir, startdate='', enddate='', split=False):
    """Update data products

    Parameters
    ----------
    outdir : str
        path to output directory
    startdate, enddate : str YYYYMMDD
        date range for download and GeoTIFF export
    split : bool
        whether to export the data as single-date GeoTIFF
    """
    commonkw = dict(
            startdate=startdate, enddate=enddate,
            split_yearly=True)

    extents = {
            'NDVI': '18.35,36.55,-20.5,-8.95',
            'SWI': '18.3,36.5,-20.4,-8.9',
            'TRMM': '18.25,36.5,-20.25,-8.75'}

    outfiles = {}
    for product in ['NDVI', 'SWI', 'TRMM']:
        product_outdir = os.path.join(outdir, product)
        try:
            os.mkdir(product_outdir)
        except OSError:
            pass
        outfiles[product] = os.path.join(product_outdir, (product.upper() + '.nc'))

    # downloads
    download_ndvi.download(outfiles['NDVI'], product_ID=0, extent=extents['NDVI'], **commonkw)
    download_swi.download(outfiles['SWI'], product='SWI10', extent=extents['SWI'], **commonkw)
    download_trmm.download(outfiles['TRMM'], extent=extents['TRMM'], **commonkw)

    for product, calc in [('NDVI', calc_ndvi), ('SWI', calc_swi)]:
        # update long-term stats
        try:
            update_stats.update(outfiles[product])
        except ValueError:
            logger.warn('No files found for product \'{}\'. Skipping.'.format(product))
            continue

        # update indices
        calc.calculate(outfiles[product], extend_mean=1)

    # update SPI stats
    spi_stats_dir = os.path.join(os.path.dirname(outfiles['TRMM']), 'spi_stats')
    if not os.path.isdir(spi_stats_dir):
        save_spi_stats.save(outfiles['TRMM'], spi_stats_dir=spi_stats_dir)

    # update SPI
    calc_rain.calculate(
            outfiles['TRMM'],
            spi_stats_dir=spi_stats_dir,
            load_into_memory=True)

    # export to GeoTIFF
    if split:
        firstyear = int(startdate[:4]) if startdate else None
        lastyear = int(enddate[:4]) if enddate else None
        splitdir = os.path.join(outdir, 'postgis_export')
        _split_to_gtiff(outfiles, splitdir=splitdir, extents=extents,
                firstyear=firstyear, lastyear=lastyear)
