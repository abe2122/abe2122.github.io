# Requirements

**Note**: These installation steps are _only_ required if you plan on updating the contents of the HUC database. If you'd simply like to use the final Feature Translation Service, skip to the examples [here](../examples/overview.md).


***
---

## Clone the Repository & Install Dependencies

Clone the Feature Translation Service repository from our associated [Feature-Translation-Service BitBucket](https://git.earthdata.nasa.gov/projects/POCUMULUS/repos/feature-translation-service/) using:

```
git clone https://git.earthdata.nasa.gov/scm/pocumulus/feature-translation-service.git
```

Navigate to the installation directory:

```
cd feature-translation-service/
```

There will be a _requirements.txt_ file in this directory that lists all of the dependencies for this service. Use the following command to install these packages.

```
pip install -r requirements.txt
```

For reference, I used the following versions of each package:
* pandas := 0.24.2
* geopandas := 0.5.0
* numpy := 1.16.4
* shapely := 1.6.4.post2
* visvalingamwyatt := 0.1.2
* tqdm := 4.32.2

***

If necessary, the next step will walk you through both where to find the example _SWOT_ data used in this service and how to download the associated data for the _HUC_ portion from USGS.
