import os

import flooddrought as fd

def update_products(outdir, startdate='', enddate='', extent=''):

    commonkw = dict(
            startdate=startdate, enddate=enddate, extent=extent,
            split_yearly=True)

    outfiles = {}
    for product in ['NDVI', 'SWI', 'TRMM']:
        outfiles[product] = os.path.join(outdir, product, (product.lower() + '.nc'))

    # downloads
    fd.ingestion.download_ndvi.download(outfiles['NDVI'], product_ID=0, **commonkw)
    fd.ingestion.download_swi.download(outfiles['SWI'], product='SWI', **commonkw)
    fd.ingestion.download_trmm.download(outfiles['TRMM'], **commonkw)

    # update long-term stats
    for product in ['NDVI', 'SWI']:
        fd.indices.update_stats.update(outfiles[product])

    # update indices
    fd.indices.calc_ndvi.calculate(outfiles['NDVI'], extend_mean=1)
    fd.indices.calc_swi.calculate(outfiles['SWI'], extend_mean=1)

    # update SPI stats
    spi_stats_dir = os.path.join(os.path.dirname(outfiles['TRMM'], 'spi_stats'))
    if not os.path.isdir(spi_stats_dir):
        fd.indices.save_spi_stats.save(outfiles['TRMM'], statsdir=spi_stats_dir)

    # update SPI
    fd.indices.calc_rain.calculate(
            outfiles['TRMM'],
            spi_stats_dir=spi_stats_dir,
            load_into_memory=True)
