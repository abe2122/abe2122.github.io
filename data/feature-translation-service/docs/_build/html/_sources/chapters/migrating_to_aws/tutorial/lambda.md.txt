# Create Lambda

In this section, I'll be talking about how to create the Lambda function for the Feature Translation Service (and just Lambda functions in general). I pretty closely followed [this tutorial](https://www.isc.upenn.edu/accessing-mysql-databases-aws-python-lambda-function), as it expanded on AWS's documentation.

**Note:** You can find my full Lambda implementation [here](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/fts-lambda?tab=graph)!

**Important:** Again, there is an associated video tutorial for this documentation. In it I also go over how to create the Lambda function for the feature translation service. The video can be found [here](https://drive.google.com/open?id=1rNfWO3NuX53jynmMZaTi5JPj0FRvnNGp).

***

## Download Packages
***

The first thing to do is download necessary packages. If you're creating a Lambda function in Python, _any_ packages you import (outside of Python's standard library I believe) have to be manually zipped up and added to a folder containing the Lambda function. Since I was using a mySQL database, I needed to import the _pymsql_ package.

Following the tutorial linked above:

```
cd Desktop/
mkdir fts-lambda
cd

mkdir ~/tmp
cd ~/tmp
virtualenv lambda_package

cd lambda_package/
source bin/activate

(lambda_package) pip install pymysql
(lambda_package) deactivate

mv lib/python3.6/site-packages/pymysql ~/Desktop/fts-lambda/
```

I was using Python 3.6 for this, however newer versions can be used. Just change the 3.6 to whatever version you have running. In the same directory run:

```
python --version
```

to find out. I had a _fts-lambda_ folder that I was storing everything in. The point of this was essentially just to isolate the _pymysql_ package and copy it over to your working directory.

---

## Create Config

In the last step, we created the database with a username, password, name, and an associated endpoint. Create a new file called _rds\_config.py_ to store this information. Here is some code for how the config file should look:

```python
db_username = ""
db_password = ""
db_name = ""
db_endpoint = ""
```

In place of the _""_, you'll need to put your username, password, database name, and database endpoint respectively. The database endpoint will be the _Host_ field that was given to you after setting up the database in the previous steps. Add this to the same folder you put your _pymyql_ package in.

***

## Create Lambda

Now it's time to create the Lambda function. My final Lambda function can be found below. I use this in the associated video tutorial, however the Lambda function found in [this](https://www.isc.upenn.edu/accessing-mysql-databases-aws-python-lambda-function) tutorial is more general purpose (although won't directly work with this tutorial).

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
    This function inserts content into mysql RDS instance
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

Copy the code above and create a Python file called _fts\_lambda.py_ and add it to the same folder as your _pymysql_ package and _rds\_config.py_ file. You should now have **three** files in your _fts-lambda/_ folder: _rds\_config.py_, _fts\_lambda.py_, and the _pymysql_ package folder.

**Note:** You can find a more in-depth description of the Lambda function in the [_Code Explained_](../../local_database_creation/HUC/overview.md)

Zip these three files in your _fts-lambda/_ folder up using your favorite tool (usually just command + right click all three elements &rarr; Compress &rarr; Rename fts_lambda.zip), and then navigate to the AWS console:

[http://goto.jpl.nasa.gov/awsconsole](http://goto.jpl.nasa.gov/awsconsole)


***

## Upload Lambda to AWS

Once in AWS, type in "Lambda" into the _Find Services_ search bar. Create a new Lambda function. From this point on, let's hope AWS doesn't modify their UI so much that the rest of this tutorial is useless.

Even if the UI does change, the main gist should still be relevant. There is also a great Lynda tutorial for this [here](https://www.lynda.com/Amazon-Web-Services-tutorials/Create-Lambda-function/746313/777903-4.html?autoplay=true). I recommend watching the entire thing, however I've linked directly to the Lambda function creation tutorial.

Click "Author From Scratch", and add a "Function Name" and call it _fts_lambda_ (or exactly what you named your ZIP file above). Choose the Runtime Environment that suits your application. In the first step, I mentioned I was using Python 3.6. If you're using something different, it's probably best to keep with that same version.

Now _Permissions_ are relatively frustrating with AWS. Under _Permissions_ click:

**Choose or create an execution role** &rarr; **Use an existing role** &rarr; **podaac-dev-cumulus-lambda-api-gateway**

***

Now that the Lambda function is created, it's time to upload the ZIP file we just made. Scroll down until you see an empty window for entering your code. Instead of writing it manually, click the drop down menu labeled **Code entry type** and then click **Upload a ZIP file**. Once it's uploaded, press "Save" at the top right of your screen.

If you get an error saying something like "Could not open file: /lambda_function.py", this just means you didn't name your Lambda function "lambda_function.py". Remember, we named it "fts_lambda.py". So two boxes over from where you uploaded the ZIP file, you'll see a _Handler_ box. Replace the **lambda_function.lambda_handler** with **fts_lambda.lambda_handler**, and that should fix it.

Finally, scroll further down the page until you see a Network tab. It should say "No VPC". Change this to the **same** VPC as the database we made in the previous step (*Default VPC (vpc-07a20961)*), click on all the subnets individually, and then choose the **same** security group as the database (*rds-launch-wizard-9*). This is **essential**, and definitely caused some issues for quite a while.

Once this is done, click save, and you should be good to test the Lambda.

***

## Test Lambda

Now that we've uploaded the Lambda function, we can test it. On your Lambda function page, configure a new test event from the drop down menu at the top of your screen (see attached video if you can't find it).

Create a new test event named _RegionTest_, and paste this:

```
{
  "body": {
    "exact": "True",
    "region": "Woods Creek-Skykomish River"
  }
}
```

into the empty region. Press "Create" at the bottom. This will create a test case for your Lambda function that tries to query the database by _region_. I chose "Woods Creek-Skykomish River" arbitrarily, and any name within the HUC database would work.

If all works correctly, you should see something like:

```
{
  "status": "200 OK",
  "hits": 1,
  "time": "3.143 ms.",
  "search on": {
    "parameter": "region",
    "exact": true
  },
  "results": {
    "Woods Creek-Skykomish River": {
      "HUC": "1711000907",
      "Bounding Box": "-122.03395970747755,47.74851958630143,...",
      "Visvalingam Polygon": "-121.96042486071667,48.0266280879531,...,
      "USGS Polygon": {
        "Object URL": "https://podaac-dev-feature-translation-service.s3-us-west-1.amazonaws.com/1711000907",
        "Source": "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Hydrography/WBD/HU2/Shape/"
      }
    }
  }
}
```

and scrolling to the top of the page, you should see a green box that says "Execution result: succeeded".
