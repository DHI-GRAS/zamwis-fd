# zamwis_fd

ZAMWIS Floods and Droughts workflow

This is a wrapper for a number of Floods and Droughts tools that downloads NDVI, SWI, TRMM and SPI and prepares them for the ZAMWIS database.

### Installation

The package and its dependencies are best installed via the Anaconda Python distribution. Please see instructions on how to install Anaconda on the (Floods and Droughts Toolbox README)[https://github.com/DHI-GRAS/F_and_D_toolbox]. 

The Floods and Droughts Python package [`flooddrought`](https://github.com/DHI-GRAS/F_and_D_toolbox) must be installed or available in the Python path.

[`graspy`](https://github.com/DHI-GRAS/graspy) must be installed.

Then run `install_or_update.bat` (which runs `python setup.py install`).


### Usage

The installation above should register a command-line tool:

    zamwis_fd --help

```
Usage: zamwis_fd [OPTIONS] OUTDIR

  Download and process NDVI, SWI10, and TRMM for ZAMWIS database

Options:
  --startdate TEXT     Download query start date YYYYMMDD (default: a year
                       ago)
  --enddate TEXT       Download query end date YYYYMMDD (default: today)
  --split / --nosplit  Split downloaded data into GeoTIFF for PostGIS import
                       (default: True)
  --help               Show this message and exit.
```

By default, it downloads all missing data since a year before today and saves it in the catalogue specified by `OUTDIR`, e.g.

    zamwis_fd C:\ZAMSWIS_DATA

The download range can be limited with the `--startdate` and `--enddate` parameters, e.g.

    zamwis_fd --startdate 20161101 C:\ZAMWIS_DATA

to get only the data since 1st November 2016.

By default, **all the existing netCDF data in the specified date range** (not just the latest download) is split into GeoTIFF for import into the ZAMWIS postgis database (disable with `--nosplit`). This process can be very time consuming, so it might be a good idea to set `--startdate` to a more recent date, if possible.
