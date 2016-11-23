import os.path
import logging
import numpy as np
from scipy.io import netcdf

from graspy import gdal_utils as gu
import netcdf_utils

logger = logging.getLogger(__name__)

def _get_minmax(data):
    return np.min(data), np.max(data)

def _get_scaled_nodata(ds):
    # take scale value from first variable that has one
    new_nodata = False
    for varn, datavar in ds.variables.iteritems():
        try:
            new_nodata = datavar._FillValue * datavar.scale_factor
            logger.info('Using scale_factor '
                    'from variable \'{}\''.format(varn))
            break
        except AttributeError:
            continue
    return new_nodata

def main_multifile(infiles, *args, **kwargs):
    "Multi-file wrapper for main function"
    # make sure ncfnames is iterable
    if not isinstance(infiles, list):
        infiles = [infiles]
    outfiles = []
    for infile in infiles:
        out = main(infile, *args, **kwargs)
        outfiles += out
    return outfiles

def main(infile, outdir, fname_fmt='%Y%m%d.tif',
         startdate=None, enddate=None,
         unscale=False, skip_existing=False):
    """Extract all time slices from netCDF file naming them after date

    Parameters
    ----------
    ncfname : str
        path to netCDF file
    outdir : str
        output directory
    fname_fmt : str
        format string for datetime.datetime.strftime()
        that generates the target file name
        e.g. '%Y%m%d.tif' will give '20160101.tif'
    startdate, enddate : datetime.datetime
        start and end date
    unscale : bool
        apply GDAL's -unscale option
        and also fix the nodata value
    skip_existing : bool
        skip existing files
        if False, existing files will be overwritten
    """
    # set common parameters
    _common_extra = []

    # get time data
    with netcdf.netcdf_file(infile, 'r') as ds:
        timevar = ds.variables['time']
        timedata = np.atleast_1d(netcdf_utils.num2date(timevar.data, timevar))

        # unscale
        if unscale:
            if '-unscale' not in _common_extra:
                _common_extra += ['-unscale']
            # fixing nodata value (gdal_translate defficiency)
            new_nodata = _get_scaled_nodata(ds)
            if new_nodata is not None:
                _common_extra += ['-a_nodata', str(new_nodata)]

    # export time slices to tif files
    outfiles = []
    for i, date in enumerate(timedata):
        if ((startdate is not None and date < startdate) or
                (enddate is not None and date > enddate)):
            continue

        # set specific parameters
        fname = date.strftime(fname_fmt)
        outfile = os.path.join(outdir, fname)
        extra = _common_extra + ['-b', str(i+1)]

        # skip existing
        if skip_existing and os.path.exists(outfile):
            continue

        # run gdal_translate with parameters
        logger.info("Time slice {:%Y-%m-%d} to file {}".format(date, fname))
        gu.translate(infile, outfile, extra=extra)
        outfiles.append(outfile)
    return outfiles
