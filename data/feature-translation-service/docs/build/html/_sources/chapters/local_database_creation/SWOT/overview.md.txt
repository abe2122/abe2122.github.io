# Overview

Creating the SWOT database locally was very similar to that of the [HUC database creation](../HUC/overview.md) earlier. Similarly, I used [Pandas](https://pandas.pydata.org/) to efficiently work with the data, and [GeoPandas](http://geopandas.org/) for some nice geospatial functions. In this section, I'll go over how to use the _SWORD_ database provided by Elizabeth Altenau. I'll also show how to run the code to generate our SWOT database from this and go more into the code I've written in the [Code Explained](code_explained.md) section.

**Important:** I found [this](https://swot.jpl.nasa.gov/meetings_by_folder.htm?id=1031) resource useful in learning about the format of SWOT Feature IDs and the SWOT mission as a whole.

# Creation Procedure

Navigate to the _/SWOT/_ directory of the cloned repository using:

```
cd feature-translation-service/SWOT/
```

Here you will see a **_create_swot_dataset.py_** file. Running this code requires that you have **two** input parameters: the input directory (containing the SWORD database) and the output directory where the final database (.csv file) will be written to.

- -i [input directory]
- -o [output directory]

**Important**: I was given a ZIP file named **_NA_MergedDB_v02_** that contained a single shapefile (and its necessary counterparts) that defined the entire SWORD database. In order to not make any assumptions about the structure of future SWOT data, I simply extracted this ZIP file and placed the resulting folder in a directory I created called **_SWOT_Data/_**. Thus, the directory structure looks as follows:

feature-translation-service/ </br>
|------ SWOT/ </br>
|------------ SWOT_Data/ </br>
|------------------ NA_MergedDB_v02/ </br>
|------------------------ NA_MergedDB_v02.shp </br>
|------------------------ NA_MergedDB_v02.dbf </br>
|------------------------ NA_MergedDB_v02.shx </br>
|------------------------ NA_MergedDB_v02.prj </br>
|------------------------ NA_MergedDB_v02.nc </br>

This way, any future SWOT shapefile information can be directly put into the _SWOT_Data/_ folder similarly to that of the _NA_MergedDB_v02_ data.

Once you've extracted the SWORD database (or other databases) as shown above, you can run the code below.

# Run the Code

As an example, you might run:

```
python create_SWOT_dataset.py -i "SWOT_Data/" -o "Database/"
```

```
python create_SWOT_dataset.py -i "SWOT_Data/" -o "path/to/Desktop/folder/"
```

Running this code will generate a SWOT database for **all** SWOT data included in the input directory. You will see a .csv named "SWOT_data.csv" appear in the output directory you specified through the command line when the program has finished.

This .csv file can then be directly uploaded to AWS through the many techniques. I will go into all AWS-related tasks in the [Migrating to AWS](../../migrating_to_aws/tutorial/overview.md) section later.
