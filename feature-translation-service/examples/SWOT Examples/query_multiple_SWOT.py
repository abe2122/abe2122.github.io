import requests
import json


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
