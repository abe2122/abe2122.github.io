# Downloading the Data

Here we will download the HUC data from the [USGS Watershed Boundary Dataset](https://water.usgs.gov/GIS/huc.html) FTP service. This dataset is broken into 22 distinct regions (and 22 associated ZIP files). I have chosen to use shapefile data instead of GDB data as I felt it was easier to work with and extract information from. Also, I will point you toward resources that provided example SWOT data for me during the testing of the SWOT portion of this service.

***
***


## Downloading USGS HUC Data

I have provided a file **_download\_data.py_** that extracts _all_ ZIP files and places their contents within a local directory called _HUC\_Data/_ inside the cloned repository.

Navigate to the file _download\_data.py_ found in the HUC directory of the cloned repository with:

```
cd feature-translation-service/HUC/
```

and run:

```
python download_data.py
```

This may take a while as the dataset is quite large. Once the program has finished, you will see the new subdirectory _HUC\_Data/_ with 22 folders named:

* WBD_01_HU2_Shape
* WBD_02_HU2_Shape
* ...
* WBD_22_HU2_Shape

***

If, for some reason you do not see this, try directly connecting to the [FTP Service](ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Hydrography/WBD/HU2/Shape/) or navigate [here](https://water.usgs.gov/GIS/huc.html) and the link for the dataset will be at the _very_ bottom of the page.

***
***

## Downloading Example SWOT Data

I obtained example SWOT data through the help of Mike Gangl. He contacted Elizabeth Altenau, a postdoctoral scholar at The University of North Carolina at Chapel Hill, who has been working toward building example SWOT data in the _SWORD_ dataset. The database contained 30m point resolutions of only North America, thus it is not in the final SWOT line and 200m point formats. Nonetheless, it has been a great tool to prototype the Feature Translation Service on. In order to obtain this data, you should either contact Mike, or go to Elizabeth directly. Their emails can be found below:

Mike Gangl (michael.e.gangl@jpl.nasa.gov) <br/>
Elizabeth Altenau (ealtenau@unc.edu)

***

Next, we will go over creating the HUC and SWOT dataset from the downloaded data.
