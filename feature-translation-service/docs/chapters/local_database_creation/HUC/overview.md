# Overview



Before migrating anything to AWS, it was essential to create the HUC Database locally. I used [Pandas](https://pandas.pydata.org/) to work with this large amount of data as efficiently as possible. Below will detail the procedure for generating the HUC database. I will save the exact details for the [Code Explained](code_explained.md) chapter at the end of this section.

# Creation Procedure

Navigate to the _/HUC/_ directory of the cloned repository using:

```
cd feature-translation-service/HUC/
```

You will see several files used to create this dataset, however the only one that you'll need to know is called **_create_HUC_dataset.py_**.

In order to run this program, you'll need to specify **three** parameters: the input directory (containing the unzipped HUC data from the USGS website we downloaded in the last section) the output directory, and a maximum number of vertices for simplified polygons in the dataset (more on that in the coming paragraphs).

The input directory, unless you've changed it manually, will always be **"HUC_Data/"**. The output directory can be wherever you prefer (at the end of this you'll only have a single .csv file in that output directory). If your output directory has not already been created, the script will go ahead and create it for you.

Due to some of the limitations of CMR (and for the sake of ease of use), we've decided to simplify polygons using two techniques that users will be able to choose from (in addition to being pointed _directly_ toward a raw unsimplified shapefile in the feature-translation-service [S3 Bucket](https://s3.console.aws.amazon.com/s3/buckets/podaac-dev-feature-translation-service/?region=us-west-2&tab=overview)). One of these algorithms allows us to specify a maximum number of vertices associated with simplified polygons in the database. The maximum number of vertices is essentially just a measure of how _much_ you want to simplify your data. Choosing a large number means simplifying _less_, while choosing a small number will means simplifying _more_. I typically keep this value at 150, however anything in the range of 100 to 400 would probably be standard here. I'll go more in depth in the [Code Explained](code_explained.md) section about this.

- -i [input directory]
- -o [output directory]
- -v [maximum number of vertices in polygon]

# Run the Code

For example, you might run:

```
python create_HUC_dataset.py -i "HUC_Data/" -o "Database/" -v 150
```

```
python create_HUC_dataset.py -i "HUC_Data/" -o "path/to/Desktop/folder/" -v 250
```

Running this code will generate a HUC database for **all** HUC data included in the input directory. You will see a .csv named "HUC_data.csv" appear in the output directory you specified through the command line when the program has finished.

This .csv file can then be directly uploaded to AWS through the many techniques. I will go into all AWS-related tasks in the [Migrating to AWS](../../migrating_to_aws/tutorial/overview.md) section later.
