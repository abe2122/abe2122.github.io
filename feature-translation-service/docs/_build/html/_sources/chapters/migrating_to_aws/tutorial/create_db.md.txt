# Creating an AWS Database

In the last section, we created a local database and exported it to a .csv file named "HUC_data.csv". This is the file we will add to a mySQL database. Here, we will create the database itself, assign permissions specific to PO.DAAC, and then populate the database with our HUC data.

***

**Note:** Again, let's hope AWS doesn't change their UI too incredibly much. If this tutorial is no longer valid, I'd recommend trying to create the database through the command line instead by following [this](https://www.isc.upenn.edu/accessing-mysql-databases-aws-python-lambda-function) tutorial.

In order to access PO.DAAC through the command line, you'll need to generate keys through JPL. You'll first need to run:

```
pip install awscli
```

to install the command line tool if you don't have it already installed. You'll then need to clone [this repo](https://podaac-git.jpl.nasa.gov:8443/aws/access-keys), and run the **_generateTempAccessKey.py_** file. It'll ask for your JPL username and password, and, if entered correctly, will give you access to PO.DAAC's AWS services through the command line for around **1 hour**.

***

Back to the tutorial though:

As mentioned in the _Tutorial Overview_ section, I've created a video tutorial that will walk you step-by-step how to create the AWS database. I felt a pure video tutorial was necessary for this section because it's mostly done on the AWS website. We'll be pressing a lot of buttons, and I feel seeing it visually is a lot better than writing it out here. The video can be found [here](https://drive.google.com/open?id=1rNfWO3NuX53jynmMZaTi5JPj0FRvnNGp).

**Note:** Not covered in the video is the idea of creating indices mySQL databases. This is essential for quick access. More information on that can be found [here](https://dev.mysql.com/doc/refman/8.0/en/create-index.html).

After following the database creation part of this video tutorial, you should have a database populated with HUC data. It is now time to create the Lambda function used to query our newly created database.
