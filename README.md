# zamwis_fd

ZAMWIS data download and preparation

This is a collection of commands of the Floods and Droughts Toolbox that produce data for the ZAMWIS database.

## Installation

You need to download and install the [Floods and Droughts Toolbox](https://github.com/DHI-GRAS/F_and_D_toolbox).

Please note the section on [configuration](https://github.com/DHI-GRAS/flooddrought#configuration), which
shows how to enter your Earthdata and Vito user credentials.

## Usage

The bat files activate the `fd` Anaconda environment created during the Floods and Droughts Toolbox installation
and rely on the `flooddrought` command-line utility.

For each product, the data is downloaded, processed (for derived products), and the data exported as GeoTIFF.
