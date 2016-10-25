import workflow

kwargs = dict(
        startdate='20160101', enddate='20160131',
        outdir=r'C:\Users\josl\Sample_Data\ZAMWIS',
        extent='18.3,36.6,-20.5,-8.9')

workflow.update_products(**kwargs)
