# Querying the SWOT Dataset

As input to the query, we _require_ either a "SWOT Feature ID". As of now, this identifier is built using information in the SWORD database of example SWOT data. More information on how this Feature ID is generated can be found in the associated Jupyter notebook _Create SWOT Database.ipynb_. In the future, there will be a standardized way of generating SWOT Feature IDs, thus it will require updating our present SWOT database.

Furthermore, at this moment, CMR does not support OR'ing multiple spatial parameters. This is necessary to the success of querying CMR for SWOT data, thus it is actively being looked into by developers at CMR. For questions/updates regarding this, a good contact is Lewis McGibbney (lewis.j.mcgibbney@jpl.nasa.gov). For now, you can extract information from the API call returns a string that might look as follows:

```
"point=-121.9770366732242,39.18799113833964&point=-121.9767090807306,39.18785702031573"
```

which can directly be used to query CMR (see the first example below), however this isn't technically the correct query as these results are AND'd together rather than OR'd. To remedy this, I've included a single line in the Lambda function:

```
TO_JSON = False     # Modify to "True" once CMR JSON POST support is available.
```

that can be changed to "True" once support for this feature has been integrated, and this will automatically format results appropriately. For example, the above list of points will become:

```
{
  "condition":
  {
    "or":
    [
      {"point": [-121.9770366732242,39.18799113833964]},
      {"point": [-121.9767090807306,39.18785702031573]}
    ]
  }
}
```

which appropriately OR's geometries. This can then be queried via:

```
curl -XPOST -H "Content-Type: application/json" https://cmr.earthdata.nasa.gov/search/collections -d @data.json
```

where _data.json_ is the above response.

***

Optionally, you can include a parameter "exact = True" that tells us you want to search for _exactly_ the Feature ID you've entered. You may also include "exact=False" to search for _partial_ matches, however it defaults to this search option automatically.  

Below are some examples I've put together to display how you can interact with the SWOT portion of the Feature Translation Service.

Querying an _exact_ SWOT Feature ID:

```python
import requests
import json


###################

# Mimicing a user querying exact matches with SWOT Feature ID "7541140001000000"

SWOT_FEATURE_ID = "7541140001000000"
EXACT = True

###################

# Query Feature Translation Service and parse JSON response
r = requests.get("https://g6zl7z2x7j.execute-api.us-west-2.amazonaws.com/prod/swot/{}?exact={}".format(SWOT_FEATURE_ID, EXACT))

# Load response from FTS
response = json.loads(r.text)

# Print all elements in HUC database that exactly match HUC "180500030105"
print(json.dumps(response, indent = 4))
```

<details><summary>Click to expand output:</summary>
<p>

```
{
    "status": "200 OK",
    "hits": 1,
    "time": "1.09 ms.",
    "search on": {
        "parameter": "SWOT Feature ID",
        "exact": true
    },
    "results": {
        "7541140001000000": "point=-83.62575151546879,9.252305471126416"
    }
}
```

</p>
</details>

<br/>

***

Querying by _partial_ SWOT Feature ID:

```python
###################

# Mimicing a user querying partial matches with SWOT Feature ID "75411400010000"

SWOT_FEATURE_ID = "75411400010000"
EXACT = False

###################

# Query Feature Translation Service and parse JSON response
r = requests.get("https://g6zl7z2x7j.execute-api.us-west-2.amazonaws.com/prod/swot/{}?exact={}".format(SWOT_FEATURE_ID, EXACT))

# Load response from FTS
response = json.loads(r.text)

# Print all elements in HUC database that exactly match HUC "180500030105"
print(json.dumps(response, indent = 4))
```

<details><summary>Click to expand output:</summary>
<p>

```
{
    "status": "200 OK",
    "hits": 10,
    "time": "1.613 ms.",
    "search on": {
        "parameter": "SWOT Feature ID",
        "exact": false
    },
    "results": {
        "75411400010000": "point=-83.62575151546879,9.252305471126416&point=-83.62575352733344,9.252576533363468&point=-83.62564640094489,9.252848395107943&point=-83.62553927444125,9.253120256862395&point=-83.62543214782254,9.253392118626815&point=-83.62527045178793,9.253664380130763&point=-83.62510875554258,9.253936641627057&point=-83.62489208736692,9.254155090331341&point=-83.62467461434254,9.254265113998752&point=-83.62440257170697,9.25437553719889"
    }
}
```

</p>
</details>

<br/>

***

Finally, we can use this output from the Feature Translation Service to query CMR for us. This can be seen below:

Query CMR via SWOT Feature ID string:

```python
from bs4 import BeautifulSoup
import requests
import json


###################

# Mimicing a user querying exact matches with SWOT Feature ID "75411400010000"

COLLECTION_ID = "C1522341104-NSIDC_ECS" # SMAP/Sentinel-1 L2 Radiometer/Radar 30-Second Scene 3 km EASE-Grid Soil Moisture V002
SWOT_FEATURE_ID = "75411400010000"
EXACT = False

###################

# Query Feature Translation Service and parse JSON response
r = requests.get("https://g6zl7z2x7j.execute-api.us-west-2.amazonaws.com/prod/swot/{}?exact={}".format(SWOT_FEATURE_ID, EXACT))

# Load response from FTS
response = json.loads(r.text)

geo_list = response['results'][SWOT_FEATURE_ID]
#print(geo_list)

# Query CMR
# --------- #

#cmr_response = requests.get("https://cmr.earthdata.nasa.gov/search/granules.json?{}&echo_collection_id=C1522341104-NSIDC_ECS&pretty=True".format(polygon))
cmr_response = requests.get("https://cmr.earthdata.nasa.gov/search/granules?{}&echo_collection_id={}&pretty=True".format(geo_list, COLLECTION_ID))

# --------- #

# Make it look nice
soup = BeautifulSoup(cmr_response.text, features = 'lxml')
print(soup.prettify())
```

<details><summary>Click to expand output:</summary>
<p>

```
<?xml version="1.0" encoding="UTF-8"?>
<html>
 <body>
  <results>
   <hits>
    287
   </hits>
   <took>
    102
   </took>
   <references>
    <reference>
     <name>
      SC:SPL2SMAP_S.002:142143638
     </name>
     <id>
      G1568764227-NSIDC_ECS
     </id>
     <location>
      https://cmr.earthdata.nasa.gov:443/search/concepts/G1568764227-NSIDC_ECS/6
     </location>
     <revision-id>
      6
     </revision-id>
    </reference>
    <reference>
     <name>
      SC:SPL2SMAP_S.002:135678909
     </name>
     <id>
      G1542789106-NSIDC_ECS
     </id>
     <location>
      https://cmr.earthdata.nasa.gov:443/search/concepts/G1542789106-NSIDC_ECS/8
     </location>
     <revision-id>
      8
     </revision-id>
    </reference>
    <reference>
     <name>
      SC:SPL2SMAP_S.002:135678915
     </name>
     <id>
      G1542789112-NSIDC_ECS
     </id>
     <location>
      https://cmr.earthdata.nasa.gov:443/search/concepts/G1542789112-NSIDC_ECS/8
     </location>
     <revision-id>
      8
     </revision-id>
    </reference>
    <reference>
     <name>
      SC:SPL2SMAP_S.002:135811869
     </name>
     <id>
      G1544249045-NSIDC_ECS
     </id>
     <location>
      https://cmr.earthdata.nasa.gov:443/search/concepts/G1544249045-NSIDC_ECS/6
     </location>
     <revision-id>
      6
     </revision-id>
    </reference>
    <reference>
     <name>
      SC:SPL2SMAP_S.002:135811942
     </name>
     <id>
      G1544249076-NSIDC_ECS
     </id>
     <location>
      https://cmr.earthdata.nasa.gov:443/search/concepts/G1544249076-NSIDC_ECS/6
     </location>
     <revision-id>
      6
     </revision-id>
    </reference>
    <reference>
     <name>
      SC:SPL2SMAP_S.002:140560057
     </name>
     <id>
      G1559612355-NSIDC_ECS
     </id>
     <location>
      https://cmr.earthdata.nasa.gov:443/search/concepts/G1559612355-NSIDC_ECS/6
     </location>
     <revision-id>
      6
     </revision-id>
    </reference>
    <reference>
     <name>
      SC:SPL2SMAP_S.002:140560049
     </name>
     <id>
      G1559612351-NSIDC_ECS
     </id>
     <location>
      https://cmr.earthdata.nasa.gov:443/search/concepts/G1559612351-NSIDC_ECS/6
     </location>
     <revision-id>
      6
     </revision-id>
    </reference>
    <reference>
     <name>
      SC:SPL2SMAP_S.002:141401314
     </name>
     <id>
      G1565102054-NSIDC_ECS
     </id>
     <location>
      https://cmr.earthdata.nasa.gov:443/search/concepts/G1565102054-NSIDC_ECS/6
     </location>
     <revision-id>
      6
     </revision-id>
    </reference>
    <reference>
     <name>
      SC:SPL2SMAP_S.002:141401155
     </name>
     <id>
      G1565101436-NSIDC_ECS
     </id>
     <location>
      https://cmr.earthdata.nasa.gov:443/search/concepts/G1565101436-NSIDC_ECS/6
     </location>
     <revision-id>
      6
     </revision-id>
    </reference>
    <reference>
     <name>
      SC:SPL2SMAP_S.002:138547962
     </name>
     <id>
      G1549592327-NSIDC_ECS
     </id>
     <location>
      https://cmr.earthdata.nasa.gov:443/search/concepts/G1549592327-NSIDC_ECS/6
     </location>
     <revision-id>
      6
     </revision-id>
    </reference>
   </references>
  </results>
 </body>
</html>
```

</p>
</details>

<br/>

**Important:** Again, this example above is technically incorrect as it AND's queries instead of OR's. That said, once CMR JSON support is available, you can access the JSON via the **same** _geo_list_ variable in the above code.

***

Most importantly, once CMR JSON POST'ing is supported, you can use the following code to create the JSON and POST it:

```python
from bs4 import BeautifulSoup
import requests
import json


###################

# Mimicing a user querying exact matches with SWOT Feature ID "75411400010000"

COLLECTION_ID = "C1522341104-NSIDC_ECS" # SMAP/Sentinel-1 L2 Radiometer/Radar 30-Second Scene 3 km EASE-Grid Soil Moisture V002
SWOT_FEATURE_ID = "75411400010000"
EXACT = False

###################

# Query Feature Translation Service and parse JSON response
r = requests.get("https://g6zl7z2x7j.execute-api.us-west-2.amazonaws.com/prod/swot/{}?exact={}".format(SWOT_FEATURE_ID, EXACT))

# Load response from FTS
response = json.loads(r.text)
json_response = response['results'][SWOT_FEATURE_ID]
#print(json_response)

# Query CMR
# --------- #

#cmr_response = requests.post("https://cmr.earthdata.nasa.gov/search/granules?echo_collection_id={}&pretty=True".format(COLLECTION_ID), data = json_response)
cmr_response = requests.post("https://cmr.earthdata.nasa.gov/search/granules?echo_collection_id={}&pretty=True".format(COLLECTION_ID), data = json_response)

# --------- #

# Make it look nice
soup = BeautifulSoup(cmr_response.text, features = 'lxml')
print(soup.prettify())
```

As of now, this throws an error, however once POST'ing is supported, this should query via JSON response.

***

So you can see that querying by _SWOT Feature ID_ is nearly identical to querying by _HUC_ or _Region_ identifiers.
