import os
import re
import glob
import shutil
import logging
import tempfile
import datetime

from flooddrought.ingestion import download_ndvi
from flooddrought.ingestion import download_swi
from flooddrought.ingestion import download_trmm

from flooddrought.indices import update_stats
from flooddrought.indices import calc_ndvi
from flooddrought.indices import calc_swi

from flooddrought.indices import save_spi_stats
from flooddrought.indices import calc_rain

from . import split_netcdf

from flooddrought.tools import gdal_utils as gu

logger = logging.getLogger('zamwis.workflow')


def _find_latest_year_splitfiles(outdir):
    pattern = os.path.join(outdir, '*.tif')
    tiffiles = sorted(glob.glob(pattern))
    if not tiffiles:
        raise ValueError('No existing tif files found.')
    else:
        return datetime.datetime.strptime(os.path.basename(tiffiles[-1])[:8], '%Y%m%d').year


def find_year_in_fname(fname):
    return int(re.match(r'(.*_)(\d{4})(\.nc)', os.path.basename(fname)).group(2))


def filter_ncfiles_year(ncfiles, latest_year):
    return [fname for fname in ncfiles if find_year_in_fname(fname) >= latest_year]


def _split_to_gtiff(outfiles, splitdir, extents):

    to_split = {
            'NDVI': ['ndvi_????.nc', os.path.join('indices', '*_anomaly_????.nc')],
            'SWI': ['swi_????.nc', os.path.join('indices', '*_deviation_????.nc')],
            'TRMM': [
                'trmm_????.nc',
                os.path.join('indices', '*_1_month_????.nc'),
                os.path.join('indices', '*_3_month_????.nc'),
                os.path.join('indices', '*_6_month_????.nc')]}

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
                    latest_year = _find_latest_year_splitfiles(outdir)
                    infiles = filter_ncfiles_year(infiles, latest_year)
                except (AttributeError, TypeError, ValueError) as err:
                    # use full list
                    logger.warn('Splitting all available netCDF data ({}).'.format(str(err)))
                    pass
                # split
                tempfiles = split_netcdf.main_multifile(infiles, tempdir, unscale=True, fname_fmt='%Y%m%d0000.tif')

                for fname in tempfiles:
                    outfile = os.path.join(outdir, os.path.basename(fname))
                    gu.warp(fname, outfile, r='bilinear', extent=extents[product])
            finally:
                shutil.rmtree(tempdir)


def update_products(outdir, startdate='', enddate='', split=False):

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
        outfiles[product] = os.path.join(product_outdir, (product.lower() + '.nc'))

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

    if split:
        splitdir = os.path.join(outdir, 'postgis_export')
        _split_to_gtiff(outfiles, splitdir=splitdir, extents=extents)
