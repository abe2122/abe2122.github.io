from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom
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

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def return_json(cur, identifier, time):

    results = cur.fetchall()

    main = Element('results')
    hits = SubElement(main, 'hits')
    hits.text = str(len(results))
    took = SubElement(main, 'took')
    took.text = str(str(time) + " ms")
    body = SubElement(main, 'body')

    if len(results) == 0:

        error = SubElement(body, 'error')
        error.text = "404: Results with the specified {} were not found.".format(identifier)

    else:

        for elem in results:
            region = SubElement(body, 'result')
            huc = SubElement(region, 'HUC')
            huc.text = elem[0]
            name = SubElement(region, 'Region')
            name.text = elem[1]
            polygon = SubElement(region, 'Polygon')
            polygon.text = elem[2]
            bbox = SubElement(region, 'BBOX')
            bbox.text = elem[3]

    return prettify(main)

def lambda_handler(event, context):
    """
    This function inserts content into mysql RDS instance
    """
    with conn.cursor() as cur:

        start = time.time()

        if "HUC" in event['body']:
            cur.execute("select * from fts_table where `HUC` LIKE %s ORDER BY CHAR_LENGTH(HUC) ASC", (event['body']['HUC']) + "%")
            end = time.time()

            return return_json(cur, "HUC", round((end - start) * 100, 3))

        elif "region" in event['body']:
            region = " ".join(event['body']['region'].split("%20"))
            cur.execute("select * from fts_table where `Region` LIKE %s ORDER BY CHAR_LENGTH(HUC) ASC", "%" + region + "%")
            end = time.time()

            return return_json(cur, "region", round((end - start) * 100, 3))

        else:
            main = Element('results')
            body = SubElement(main, 'body')
            error = SubElement(body, 'error')
            error.text = '400: The specified URL is invalid (does not exist).'

            return prettify(main)
