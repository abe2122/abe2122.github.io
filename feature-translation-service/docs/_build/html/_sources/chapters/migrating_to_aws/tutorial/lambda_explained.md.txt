# Lambda Explained
***

Now I'll go over my Lambda function found below:

<details><summary><span style="color:blue">Click here for my Lambda code!</span></summary>
<p>


```python
import sys
import json
import logging
import rds_config
import pymysql
import time

rds_host  = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
port = 3306

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name,
                           passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

###################


def return_json(cur, identifier, name, exact, time):

    results = cur.fetchall()

    data = {}
    if len(results) == 0:
        data['error'] = "404: Results with the specified {} were not found.".format(identifier + " " + name)
        return data
    else:

        if len(results) > 100:
            data['error'] = "413: Your query has returned " + str(len(results)) + " results (> 100). If you're searching a specific " + identifier + \
                            ", use the parameter 'exact=True'. Otherwise, refine your search to return less results, or head here: https://water.usgs.gov/GIS/huc.html to download mass HUC data."

            return data


        data['status'] = "200 OK"
        data['hits'] = len(results)
        data['time'] = str(time) + " ms."
        data['search on'] = {"parameter": identifier, "exact": exact}
        data['results'] = {}

        if identifier == "HUC":
            for elem in results:
                data['results'][elem[0]] = {
                                            "Region Name":elem[1],
                                            "Bounding Box": elem[4],
                                            "Convex Hull Polygon":elem[2],
                                            "Visvalingam Polygon":elem[3],
                                            "USGS Polygon": {
                                                             "Object URL": "https://podaac-feature-translation-service.s3-us-west-2.amazonaws.com/{}.zip".format(elem[0]),
                                                             "Source":"ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Hydrography/WBD/HU2/Shape/WBD_{}_HU2_Shape.zip".format(elem[0][:2])
                                                            }
                                            }
        else:
            for elem in results:
                data['results'][elem[1]] = {
                                            "HUC":elem[0],
                                            "Bounding Box": elem[4],
                                            "Convex Hull Polygon":elem[2],
                                            "Visvalingam Polygon":elem[3],
                                            "USGS Polygon": {
                                                             "Object URL": "https://podaac-feature-translation-service.s3-us-west-2.amazonaws.com/{}.zip".format(elem[0]),
                                                             "Source":"ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Hydrography/WBD/HU2/Shape/WBD_{}_HU2_Shape.zip".format(elem[0][:2])
                                                            }
                                            }

    return data


def lambda_handler(event, context):
   """
   This function queries the HUC database for relavant results
   """
    with conn.cursor() as cur:

		# Start a timer to measure query time.
        start = time.time()

		# Entered if the user queries by HUC
        if "HUC" in event['body']:
            if "exact" in event['body']:

            	# User queries an exact HUC
                if event['body']['exact'].lower() == "true":
                    cur.execute("select * from huc_table where `HUC` = %s", event['body']['HUC'])
                    exact = True
                # User queries partial HUC
                else:
                    cur.execute("select * from huc_table where `HUC` LIKE %s ORDER BY CHAR_LENGTH(HUC) ASC", event['body']['HUC'] + "%")
                    exact = False
            # Default to "partial" case when user doesn't specific and "exact" value.
            else:
                cur.execute("select * from huc_table where `HUC` LIKE %s ORDER BY CHAR_LENGTH(HUC) ASC", event['body']['HUC'] + "%")
                exact = False

            end = time.time()
            return return_json(cur, "HUC", event['body']['HUC'], exact, round((end - start) * 1000, 3))

		# Similar process for region
        elif "region" in event['body']:
        	# Handle spaces in request
            region = " ".join(event['body']['region'].split("%20"))

            if "exact" in event['body']:
                # User queries exact region
                if event['body']['exact'].lower() == "true":
                    cur.execute("select * from fts_table where `Region` = %s", region)
                    exact = True
                # User queries partial region match
                else:
                    cur.execute("select * from fts_table where `Region` LIKE %s ORDER BY CHAR_LENGTH(HUC) ASC", region + "%")
                    exact = False
            else:
                cur.execute("select * from fts_table where `Region` LIKE %s ORDER BY CHAR_LENGTH(HUC) ASC", region + "%")
                exact = False

            end = time.time()
            return return_json(cur, "region", region, exact, round((end - start) * 1000, 3))

        else:
        	# Return 400 error assuming path is incorrect.
            data = {}
            data['error'] = "400: The specified URL is invalid (does not exist)."
            return data
```

</p>
</details>

 <br/>

This code can really be broken down into three main sections. First we have:

```python
import sys
import json
import logging
import rds_config
import pymysql
import time

rds_host  = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
port = 3306

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name,
                           passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")
```

The _rds_config_ lines gather information from the associated _rds_config.py_ file uploaded to AWS. Then, outside of the _lambda_handler()_ function, we connect to the database. This is so a new connection isn't made _every_ time the Lambda function is called. The success (or failure) is then logged.

***

The next section deals with accessing the HUC database we've uploaded previously. This can be seen below:

```python
def lambda_handler(event, context):
    """
    This function queries the HUC database for relavant results
    """
    with conn.cursor() as cur:

		# Start a timer to measure query time.
        start = time.time()

		# Entered if the user queries by HUC
        if "HUC" in event['body']:
            if "exact" in event['body']:

            	# User queries an exact HUC
                if event['body']['exact'].lower() == "true":
                    cur.execute("select * from huc_table where `HUC` = %s", event['body']['HUC'])
                    exact = True
                # User queries partial HUC
                else:
                    cur.execute("select * from huc_table where `HUC` LIKE %s ORDER BY CHAR_LENGTH(HUC) ASC", event['body']['HUC'] + "%")
                    exact = False
            # Default to "partial" case when user doesn't specific and "exact" value.
            else:
                cur.execute("select * from huc_table where `HUC` LIKE %s ORDER BY CHAR_LENGTH(HUC) ASC", event['body']['HUC'] + "%")
                exact = False

            end = time.time()
            return return_json(cur, "HUC", event['body']['HUC'], exact, round((end - start) * 1000, 3))

		# Similar process for region
        elif "region" in event['body']:
        	# Handle spaces in request
            region = " ".join(event['body']['region'].split("%20"))

            if "exact" in event['body']:
                # User queries exact region
                if event['body']['exact'].lower() == "true":
                    cur.execute("select * from fts_table where `Region` = %s", region)
                    exact = True
                # User queries partial region match
                else:
                    cur.execute("select * from fts_table where `Region` LIKE %s ORDER BY CHAR_LENGTH(HUC) ASC", region + "%")
                    exact = False
            else:
                cur.execute("select * from fts_table where `Region` LIKE %s ORDER BY CHAR_LENGTH(HUC) ASC", region + "%")
                exact = False

            end = time.time()
            return return_json(cur, "region", region, exact, round((end - start) * 1000, 3))

        else:
        	# Return 400 error assuming path is incorrect.
            data = {}
            data['error'] = "400: The specified URL is invalid (does not exist)."
            return data
```

This is where pretty much all of the logic is. The Lambda function takes in an _event_ passed in each time the Lambda is called. This event is precisely was is returned from the API Gateway or from our test cases. Thus, an example of this could be:

```
{
  "body": {
    "exact": "True",
    "region": "Woods Creek-Skykomish River"
  }
}
```

Following the code above, you can see that I'm branching into these if/else statements depending on the contents of this JSON file passed to the Lambda function through API Gateway. Different queries to our mySQL database are done based on the values of _exact_ and whether you query a _HUC_ or a _region_.

***

The final section can be seen below:

```python
def return_json(cur, identifier, name, exact, time):

    results = cur.fetchall()

    data = {}
    if len(results) == 0:
        data['error'] = "404: Results with the specified {} were not found.".format(identifier + " " + name)
    else:

        if len(results) > 100:
            data['error'] = "413: Your query has returned " + str(len(results)) + " results (> 100). If you're searching a specific " + identifier + \
                            ", use the parameter 'exact=True'. Otherwise, refine your search to return less results, or head here: https://water.usgs.gov/GIS/huc.html to download mass HUC data."

            return data


        data['status'] = "200 OK"
        data['hits'] = len(results)
        data['time'] = str(time) + " ms."
        data['search on'] = {"parameter": identifier, "exact": exact}
        data['results'] = {}

        if identifier == "HUC":
            for elem in results:
            	# Sub-element of "results" is the HUC
                data['results'][elem[0]] = {
                                            "Region Name":elem[1],
                                            "Bounding Box": elem[4],
                                            "Convex Hull Polygon":elem[2],
                                            "Visvalingam Polygon":elem[3],
                                            "USGS Polygon": {
                                                             "Object URL": "https://podaac-dev-feature-translation-service.s3-us-west-1.amazonaws.com/{}".format(elem[0]),
                                                             "Source":"ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Hydrography/WBD/HU2/Shape/"
                                                            }
                                            }
        else:
            for elem in results:
            	# Sub-element of "results" is the region
                data['results'][elem[1]] = {
                                            "HUC":elem[0],
                                            "Bounding Box": elem[4],
                                            "Convex Hull Polygon":elem[2],
                                            "Visvalingam Polygon":elem[3],
                                            "USGS Polygon": {
                                                             "Object URL": "https://podaac-dev-feature-translation-service.s3-us-west-1.amazonaws.com/{}".format(elem[0]),
                                                             "Source":"ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Hydrography/WBD/HU2/Shape/"
                                                            }
                                            }

    return data
```


All this does is fetch all of the results returned from the mySQL query and format it in a readable JSON format.

**Note:** Lambda functions support a _maximum_ return body of 6MB. This means extremely large queries to 200+ HUCs will exceed that limit. I've caught this by redirecting users to the USGS website, asking them to refine their search, or by remembering to put "exact=True" if they forgot to.
