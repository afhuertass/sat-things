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
    import folium
    import json
    import geopandas as gpd
    import datetime
    return datetime, folium, gpd, json, mo, xr


@app.cell
def _():
    import openeo as eo
    return (eo,)


@app.cell
def _(gpd, mo):
    df = gpd.read_file("data/Colombia_departamentos_municipios_poblacion-topov2/MGN_ANM_DPTOS.geojson")

    deps = ["CUNDINAMARCA" , "BOGOTÁ, D.C."]
    cundi = df[ df["DPTO_CNMBR"].isin(deps) ]

    cundi = cundi.to_geo_dict()

    department = mo.ui.dropdown(options = df["DPTO_CNMBR"].unique() )
    department
    return department, df


@app.cell
def _(department, df):
    department.value

    selected_df = df[ df[ "DPTO_CNMBR"] == department.value ]
    return (selected_df,)


@app.cell
def _(folium, json, selected_df):
    def read_json(filename: str) -> dict:
        with open(filename) as input:
            field = json.load(input)
        return field
    aoi = selected_df.to_geo_dict()
    #aoi = read_json("data/Colombia_departamentos_municipios_poblacion-topov2/MGN_ANM_DPTOS.geojson")
    # 4.6458778276651955, -74.107015224911 
    m = folium.Map([ 4.64, -74.10], zoom_start=7)
    folium.GeoJson(aoi).add_to(m)
    m
    return (aoi,)


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
    temporal_extend = ["2025-01-01" , "2025-01-30"]
    bands = ["B04", "B08", "B03" , "B11", "B12"]
    #5.2718, -73.4430
    return bands, col_id, temporal_extend


@app.cell
def _(bands):
    bands
    return


@app.cell
def _(aoi, bands, col_id, connection, temporal_extend):

    cube =connection.load_collection(collection_id=col_id, 
                                     temporal_extent=temporal_extend, 
                                     bands=bands
                                    ).filter_spatial(aoi)
    return (cube,)


@app.cell
def _():



    from openeo.extra.spectral_indices import compute_indices
    return (compute_indices,)


@app.cell
def _(compute_indices, cube):
    #max = cube.reduce_dimension(reducer="mean", dimension="t")
    indices = compute_indices(
        cube,
        indices=["NBAI"]
    ).reduce_dimension(reducer="mean", dimension="t")
    return (indices,)


@app.cell
def _(datetime, department, indices):
    ct = datetime.datetime.now()
    ts = ct.timestamp()

    filename = department.value + "_" + str(ts)
    print(filename)
    indices.download( filename +'.tiff')
    indices.download( filename + '.nc')
    return (filename,)


@app.cell
def _(filename):
    filename
    return


@app.cell
def _(filename, xr):

    ds_indices = xr.open_dataset( filename + ".nc" )

    data = ds_indices[["NBAI"]].to_array(dim="bands")
    x_size = ds_indices["x"].shape[0]
    y_size = ds_indices["y"].shape[0]

    return data, x_size, y_size


@app.cell
def _(data):
    nu_data = data.to_numpy()
    return (nu_data,)


@app.cell
def _(nu_data, x_size, y_size):
    nu_data_reshaped = nu_data.reshape((y_size, x_size))
    return (nu_data_reshaped,)


@app.cell
def _(nu_data_reshaped):
    import numpy as np

    nu2 = np.nan_to_num( nu_data_reshaped , nan=0)
    return (nu2,)


@app.cell
def _(nu2):
    import matplotlib.pyplot as plt

    plt.imshow( nu2 )
    plt.colorbar()
    plt.title("Normalized Urban Build up Index")
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
