from setuptools import setup, find_packages

setup(
    name='zamwis_fd',
    version='0.1',
    description='ZAMWIS Floods and Droughts Toolbox Workflow',
    author='Jonas Solvsteen',
    author_email='josl@dhi-gras.com',
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
    [console_scripts]
    zamwis_fd=zamwis_fd.scripts.cli:main
    """,
    install_requires=[
        'click',
        'flooddrought', 'gdal>=1.11',
        'numpy', 'scipy', 'pandas',
        'xarray', 'netCDF4'])
