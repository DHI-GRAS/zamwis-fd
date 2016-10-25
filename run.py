import os
import sys
import logging

fddir = os.path.join(
        os.path.expanduser('~'), 'Documents', 'GitHub',
        'F_and_D_Toolbox', 'scripts', 'F_and_D_Toolbox')
sys.path.append(fddir)
import workflow

logging.basicConfig(format='%(module)s - %(message)s', level=logging.DEBUG)

kwargs = dict(
        startdate='20160101', enddate='20160131',
        outdir=r'C:\Users\josl\Sample_Data\ZAMWIS',
        extent='18.3,36.6,-20.5,-8.9',
        split=True)

workflow.update_products(**kwargs)
