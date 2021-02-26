# Tutorial Overview

In this section, I want to clarify the steps taken to create and query an AWS database. At times I felt that documentation was either lacking or, in the case with AWS documentation, too overwhelming and often outdated.

**_IMPORTANT:_** I've created a short video where I complete this part of the tutorial. There are quite a few subtle steps, so I felt a video would best capture those. **This video can be found [here](https://drive.google.com/open?id=1rNfWO3NuX53jynmMZaTi5JPj0FRvnNGp)!**

In the first section, I'll talk about creating a mySQL database and assigning permissions specific to PO.DAAC. Then, I'll talk about creating the Lambda function that will ultimately access that database. Finally, I'll go into creating an API Gateway for that Lambda function so you can query the database from a _curl_ statement in the command line.

There are two major resources that I pulled from when completing the AWS portion of the feature translation service. These are:

* [https://www.lynda.com/Amazon-Web-Services-tutorials/Easy-RESTful-API-creation/746313/777888-4.html?autoplay=true](https://www.lynda.com/Amazon-Web-Services-tutorials/Easy-RESTful-API-creation/746313/777888-4.html?autoplay=true)
* [https://www.isc.upenn.edu/accessing-mysql-databases-aws-python-lambda-function](https://www.isc.upenn.edu/accessing-mysql-databases-aws-python-lambda-function)

I'd highly encourage reading over/watching these prior to just attempting to follow these instructions. The Lambda function tutorial here is quite comprehensive (as I felt that was the hardest), however other sections can likely be done without my tutorial or using it as supplementary information.
