import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import polars as pl

    from netCDF4 import Dataset
    from matplotlib import gridspec
    import xarray as xr
    return (xr,)


@app.cell
def _():
    import openeo as eo
    return (eo,)


@app.cell
def _(eo):
    connection = eo.connect(url="openeo.dataspace.copernicus.eu").authenticate_oidc()
    return (connection,)


@app.cell
def _(connection):
    connection.list_collection_ids()
    return


@app.cell
def _(connection):
    connection.describe_collection("SENTINEL2_L1C")
    return


@app.cell
def _():
    col_id = "SENTINEL2_L1C"
    extend =  {     
          "west": 5.2718,
          "south": -73.4430,
          "east": 5.3618,
          "north": -73.3528
    }

    # 5.340944972850219, -73.35883836455443
    # 5.289309019811285, -73.42567189328439

    # 4.474902329429305, -74.28620393996874
    #4.778559097331294, -73.87964080289271
    extend =  {
          "west": 4.47,
          "south": -74.28,
          "east": 4.77,
          "north": -73.87,
      }
    #extend = {"west": 5.15, "south": 51.20, "east": 5.25, "north": 51.35}
    temporal_extend = ["2025-01-01" , "2025-11-17"]
    bands = ["B04", "B08", "B03" , "B11", "B12"]
    #5.2718, -73.4430
    return bands, col_id, extend, temporal_extend


@app.cell
def _(bands):
    bands
    return


@app.cell
def _(bands, col_id, connection, extend, temporal_extend):

    cube =connection.load_collection(collection_id=col_id, 
                                     spatial_extent= extend , 
                                     temporal_extent=temporal_extend, 
                                     bands=bands
                                    )
    return (cube,)


@app.cell
def _():



    from openeo.extra.spectral_indices import compute_indices
    return (compute_indices,)


@app.cell
def _():
    import rasterio
    import matplotlib.pyplot as plt

    img2 = rasterio.open("tibana.tiff").read()
    plt.imshow(img2[0])
    plt.colorbar()
    plt.show()
    return (plt,)


@app.cell
def _(compute_indices, cube):
    max = cube.max_time()
    indices = compute_indices(
        max,
        indices=["NBAI"]
    )

    return (indices,)


@app.cell
def _(indices):
    indices.download('tibana.tiff')
    indices.download('tibana.nc')
    return


@app.cell
def _():
    return


@app.cell
def _(xr):

    ds_indices = xr.open_dataset("tibana.nc" )

    data = ds_indices[["NBAI"]].to_array(dim="bands")
    data
    return (data,)


@app.cell
def _(data):
    nu_data = data.to_numpy()
    return (nu_data,)


@app.cell
def _(nu_data):
    nu_data_reshaped = nu_data.reshape((4599, 1044))
    return (nu_data_reshaped,)


@app.cell
def _(nu_data_reshaped):
    import numpy as np

    nu2 = np.nan_to_num( nu_data_reshaped , nan=0.0)
    return (nu2,)


@app.cell
def _(nu2, plt):


    plt.imshow( nu2, vmin=0, vmax = 0.1)
    plt.colorbar()
    plt.show()
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
