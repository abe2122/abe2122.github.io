.. feature-translation-service documentation master file, created by
   sphinx-quickstart on Sun Jul  7 10:20:16 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PO.DAAC Feature Translation Service Documentation
=======================================================

.. toctree::
   :maxdepth: 2
   :caption: Introduction

   chapters/about

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   chapters/getting_started/requirements.md
   chapters/getting_started/downloading.md

.. toctree::
  :maxdepth: 1
  :caption: HUC Database Creation

  chapters/local_database_creation/HUC/overview.md
  chapters/local_database_creation/HUC/code_explained.md

.. toctree::
   :maxdepth: 1
   :caption: SWOT Database Creation

   chapters/local_database_creation/SWOT/overview.md
   chapters/local_database_creation/SWOT/code_explained.md

.. toctree::
   :maxdepth: 1
   :caption: Migrating HUC to AWS

   chapters/migrating_to_aws/tutorial/overview.md
   chapters/migrating_to_aws/tutorial/create_db.md
   chapters/migrating_to_aws/tutorial/lambda.md
   chapters/migrating_to_aws/tutorial/api_gateway.md
   chapters/migrating_to_aws/tutorial/lambda_explained.md

.. toctree::
  :maxdepth: 1
  :caption: Migrating SWOT to AWS

  chapters/migrating_to_aws/swot_tutorial/overview.md

.. toctree::
   :maxdepth: 2
   :caption: Examples

   chapters/examples/overview.md
   chapters/examples/huc/querying.md
   chapters/examples/swot/querying.md
