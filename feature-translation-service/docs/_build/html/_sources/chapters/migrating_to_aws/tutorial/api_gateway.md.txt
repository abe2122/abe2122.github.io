# API Gateway

In the last section, we created our Lambda function and used it to query the HUC database we created. In this section, I'll detail how I created an API Gateway in AWS. This way, users will be able to query the database from a _curl_ statement in the command line.

There are several ways of doing this - from uploading OpenAPI 3.0 .yaml files, to creating your own on AWS itself. This will not nearly be as detailed as the two previous steps, as I feel [this Lynda series](https://www.lynda.com/Amazon-Web-Services-tutorials/Create-API-Lambda/746313/777907-4.html?autoplay=true) does a fantastic job at explaining how to do this.

**Important:** Again, there is an associated video tutorial for this documentation. In it I also go over how to create the API gateway for the feature translation service. The video can be found [here](https://drive.google.com/open?id=1rNfWO3NuX53jynmMZaTi5JPj0FRvnNGp). You can find my full API Gateway implementation [here](https://us-west-2.console.aws.amazon.com/apigateway/home?region=us-west-2#/apis/g6zl7z2x7j/resources/rh3x3wg1nb)!

***

Below is my baseline OpenAPI 3.0 ".yaml" file for API Gateway.

<details><summary><span style="color:blue">Click to expand my OpenAPI 3.0 file:</span></summary>
<p>


```
openapi: 3.0.0
info:
  title: huc-lambda-API
  description: API used for PO.DAAC feature translation service
  version: 0.1.0
paths:
  /huc/{huc}:
    get:
      operationId: gethuc
      parameters:
        - description: The ID of the HUC to return.
          in: path
          name: huc
          required: true
          schema:
            example: "1701020108"
            type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/200'
        '400':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/400'
        '404':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/404'
        '413':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/413'
      summary: Returns associated name and simplified polygon
  /region/{region}:
    get:
      operationId: getregion
      parameters:
        - description: The ID of the region to return.
          in: path
          name: region
          required: true
          schema:
            example: "California Region"
            type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/200'
        '400':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/400'
        '404':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/404'
        '413':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/413'
      summary: Returns associated HUC and simplified polygon.
components:
  schemas:
    200:
      description: 200 response from API
      properties:
        bounding_box:
          description: Bounding box for queried region.
          example: "-121.63767546330098,37.04979849040802,-121.48073155937789,37.23308885991514"
          type: string
        full_poly:
          description: Full USGS polygon location.
          example: {
                    s3: "podaac-dev-feature-translation-service",
                    key: "180500030105",
                    shpindex: "12345"
                   }
          type: object
        huc:
          description: HUC identifier for queried region.
          example: "180500030105"
          type: string
        polygon:
          description: Simplified polygon for queried region.
          example: "-121.68307875802219,37.336883989962416,
                    -121.7034261236156,37.335436064964654,
                    -121.72219968921144,37.35039130244144,
                    -121.68307875802219,37.336883989962416"
          type: string
        region:
          description: Region name for queried region.
          example: "California Region"
          type: string
      required:
        - bounding_box
        - full_poly
        - huc
        - polygon
        - region
      type: object
    400:
      description: 400 response from API
      properties:
        error:
          description: "The specified URL is invalid (does not exist)."
          type: string
      required:
        - error
      type: object
    404:
      description: 404 response from API
      properties:
        error:
          description: "An entry with the specified region was not found."
          type: string
      required:
        - error
      type: object
    413:
      description: 413 response from API
      properties:
        error:
          description: "413: Your query has returned is too large."
          type: string
      required:
        - error
      type: object

```
</p>
</details>
<br/><br/>

I modified it slightly through the AWS console however, so I've linked to my full implementation above.

The rest of the Lynda tutorial does a fairly thorough job at explaining how to create the API. That said, there are a few things that I personally found confusing:

- Passing parameters from API to Lambda
- Integration/Method Responses

After watching the Lynda tutorial, these will make more sense, but modifying these for your own application caused me some issues.

The purpose of API Gateway is essentially to map commands users can interpret to something that is queryable through the Lambda function. They sort of arbitrarily chose to create a model template to use, however I felt that sort of unnecessarily complicated a lot of things.

Also, the template they used would not work for other applications in general. So I scrapped their idea and went with a mapping of my own. For example, this is how the Integration Request mapping goes for a "HUC" query for me:

```
{
  "body": {
    "exact":"$input.params('exact')"
    "HUC": "$input.params('huc')"
  }
}
```

I've created a **/{huc}** resource with a "GET" request. Thus whatever HUC value I pass into
the API is assigned to $input.params('huc'), leaving you with:

```
{
  "body": {
    "exact":"True"
    "HUC": "12345678"
  }
}
```

for example.

***

Also, the tutorial goes over Integration and Method Responses. These essentially just define how information returned from the Lambda function will be mapped back to more human-interpretable results for end-users. I personally formatted these responses within the Lambda function itself instead of using mapping templates. That said, I'm not sure if there is a performance hit from doing so.

If you followed my video tutorial [here](https://drive.google.com/open?id=1rNfWO3NuX53jynmMZaTi5JPj0FRvnNGp) or the Lynda one [here](https://www.lynda.com/Amazon-Web-Services-tutorials/Easy-RESTful-API-creation/746313/777888-4.html?autoplay=true), you should now be ready to query information from the HUC database from a _curl_ command.

The next [Examples](../../examples/overview.md) section will take you through exactly how to do that with a few useful examples in Python.
