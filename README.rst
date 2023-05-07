====
zenq
====


.. image:: https://img.shields.io/pypi/v/zenq.svg
        :target: https://pypi.python.org/pypi/zenq

.. image:: https://img.shields.io/travis/nareabg/zenq.svg
        :target: https://travis-ci.com/nareabg/zenq

.. image:: https://readthedocs.org/projects/zenq/badge/?version=latest
        :target: https://zenq.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




CLV package


* Free software: MIT license


Installation
============

To install Zenq CLV Models Library, simply run the following command:

.. code-block:: bash

    pip install zenq-clv-models

The Story
=========
In order to provide marketing analysts and data scientists with a useful tool, the ZENQ package was developed. Because it is connected to a database, our product can be utilized by a wider variety of customers, including those who have a limited understanding of coding. Users are able to run scripts derived from the ZENQ package while the package works on data pertaining to customers. The data may be inserted into the database by users. It gives users the ability to study the behaviors of consumers based on how they engage with the company. Computations of CLV and RFM, in addition to forecasts, are the primary objective of the package. It features a Machine Learning component that makes an assumption as to whether the client will "die" or still be alive after a certain amount of time has passed. For the purpose of developing assumptions about the customers'  loyalness, ZENQ relies on the Pareto/NBD model. Because the package offers a number of different visualizations, it simplifies the process of comprehending the statistics and basing business decisions on those findings. 


Usage - Simple Example
======================

Once installed, you can use the library in your Python scripts as follows:

.. code-block:: bash

    #run in terminal for postgres url creation
    docker run --name my-postgres-db -e POSTGRES_USER=master -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=GLOBBING -p 5432:5432 -d postgres

.. code-block:: python   

    # Initialize database with tables
     from zenq.api.prepare_db import db
     m=db()
     m.main()

.. code-block:: python

    # Insert data into database
    from zenq.api.endpoints import insert_facts
    insert_facts('globbing.csv', 'Customer', 'Gender', 'InvoiceId', 'Date', 'Product_weight', 'Product_price')

.. code-block:: python   
         
    # Insert data of logging into LOGS table
    from zenq.api.endpoints import update_log
    update_log()

.. code-block:: python

    #define model
     from zenq.clvmodels.pareto import Model
     model = Model()
     cltv = model.cltv_df()
     rfm = model.rfm_score()
     parameters = model.model_params()
     alive = model.customer_is_alive()

.. code-block:: python

    #define Visualizations
    from zenq.visualizations.plot import Visuals
    gender_price = visuals.gender_price()


Credits
=========

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
