import rds_config
import logging
import pymysql
import time
import json
import re

# Set up connection variables
rds_host  = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
port = 3306

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Connect to the mySQL database
try:
    conn = pymysql.connect(rds_host, user=name,
                           passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

###########

def format_json(cur, swot_id, exact, time):

    # Fetch all results from mySQL query
    results = cur.fetchall()

    # ********** #
    TO_JSON = False     # Modify to "True" once CMR JSON POST support is available.
    # ********** #

    data = {}

    if results[0][0] == None:
        data['error'] = "404: Results with the specified SWOT Feature ID {} were not found.".format(swot_id)
    elif len(results[0][0]) > 5750000:
        data['error'] = "413: Query exceeds 6MB with {} hits.".format(str(int(len(results[0][0].split("&")))))

    else:
        data['status'] = "200 OK"
        data['hits'] = int(len(results[0][0].split("&")))
        data['time'] = str(time) + " ms."
        data['search on'] = {"parameter": "SWOT Feature ID", "exact": exact}
        data['results'] = {}
        data['results'][swot_id] = {}


        if TO_JSON:
            results = results[0][0].split("&")
            data['results'][swot_id] = {}

            # 1 result returned
            # No need for "OR" between multiple points
            if len(results) == 1:
                geometry = results[0].split("=")
                data['results'][swot_id]['condition'] = {geometry[0]: [float(e) for e in geometry[1].split(",")]}
            else:
                data['results'][swot_id]['condition'] = {}
                data['results'][swot_id]['condition']['or'] = []


                # OR'ing together multiple points. Single line for loop creates individual
                # dictionaries with point/vertex key/value pairs. So, for example, one iteration
                # will result in:

                # {point: [94.323423, 43.230432]}

                # This is done for each point/linestring returned, and the final result is added to a
                # giant list correctly formatted for CMR JSON POST request.
                for geometry in results:
                    element = geometry.split("=")
                    data['results'][swot_id]['condition']['or'].append({element[0]: [element[1]]})

        # Since JSON POST'ing support isn't currently available, this just returns
        # a CMR queryable list of all points used in the form:

        # point=100,20&point=140,30... which can then be used like so:

        # "https://cmr.earthdata.nasa.gov/search/collections?point=100,20&point=140,30"
        else:
            data['results'][swot_id] = results[0][0]

    return data


def lambda_handler(event, context):

    with conn.cursor() as cur:

        start = time.time()

        # Necessary as I'm concatenating all query results returned. Default max
        # size is like 1024 characters, which isn't nearly enough.
        cur.execute("SET group_concat_max_len = 100000000")

        # Searching on SWOT Feature ID
        if "SWOT_ID" in event['body']:

            # User has given an 'exact' value
            if "exact" in event['body']:

                # User wants the query to be exact
                if event['body']['exact'].lower() == "true":

                    # Return everything EQUAL to the input
                    cur.execute("select GROUP_CONCAT(`geometry` SEPARATOR '&') from swot_table where `SWOT_ID` = %s", event['body']['SWOT_ID'])
                    exact = True

                # User wants partial matches (or misspelled "true")
                else:

                    # Search Feature IDs for similar results starting with user input.
                    cur.execute("select GROUP_CONCAT(`geometry` SEPARATOR '&') from swot_table where `SWOT_ID` LIKE %s", event['body']['SWOT_ID'] + "%")
                    exact = False

            # User didn't given an "exact" value in API request
            # Assume exact = False
            else:
                cur.execute("select GROUP_CONCAT(`geometry` SEPARATOR '&') from swot_table where `SWOT_ID` LIKE %s", event['body']['SWOT_ID'] + "%")
                exact = False

            end = time.time()

            return format_json(cur, event['body']['SWOT_ID'], exact, round((end - start) * 1000, 3))

        else:
            # Return 400 error assuming path is incorrect.
            data = {}
            data['error'] = "400: The specified URL is invalid (does not exist)."
            return data
