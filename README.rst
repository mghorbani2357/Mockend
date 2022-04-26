.. |license| image:: https://img.shields.io/github/license/mghorbani2357/mockend
    :target: https://raw.githubusercontent.com/mghorbani2357/mockend/master/LICENSE
    :alt: GitHub Licence

.. |downloadrate| image:: https://img.shields.io/pypi/dm/mockend
    :target: https://pypistats.org/packages/mockend

.. |wheel| image:: https://img.shields.io/pypi/wheel/mockend  
    :target: https://pypi.python.org/pypi/mockend
    :alt: PyPI - Wheel

.. |pypiversion| image:: https://img.shields.io/pypi/v/mockend  
    :target: https://pypi.python.org/pypi/mockend
    :alt: PyPI

.. |format| image:: https://img.shields.io/pypi/format/mockend
    :target: https://pypi.python.org/pypi/mockend
    :alt: PyPI - Format

.. |downloads| image:: https://static.pepy.tech/personalized-badge/mockend?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads
    :target: https://pepy.tech/project/mockend

.. |lastcommit| image:: https://img.shields.io/github/last-commit/mghorbani2357/Mockend 
    :alt: GitHub last commit
    
.. |lastrelease| image:: https://img.shields.io/github/release-date/mghorbani2357/Mockend   
    :alt: GitHub Release Date

.. |codequality| image:: https://app.codacy.com/project/badge/Grade/c1e3c9bb67204f199026f4d6b480a5a9
    :target: https://www.codacy.com/gh/mghorbani2357/Mockend/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mghorbani2357/Mockend&amp;utm_campaign=Badge_Grade
    :alt: Code quality

.. |codacycoverage| image:: https://app.codacy.com/project/badge/Coverage/c1e3c9bb67204f199026f4d6b480a5a9
    :target: https://www.codacy.com/gh/mghorbani2357/Mockend/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mghorbani2357/Mockend&amp;utm_campaign=Badge_Coverage
    :alt: Code coverage

.. |workflow| image:: https://img.shields.io/github/workflow/status/mghorbani2357/mockend/main?logo=github
    :alt: GitHub Workflow Status

.. |readthedocs| image:: https://readthedocs.org/projects/mockend/badge/?version=latest
    :target: https://mockend.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

*****************
Mockend API
*****************

.. class:: center

 |license| |workflow| |readthedocs| |codacycoverage| |codequality| |downloadrate| |downloads| |pypiversion| |format| |wheel| |lastcommit| |lastrelease|


Mockend is a Python library that can be used to mock any REST API endpoint.

Installation
============

.. code-block:: bash

    pip install mockend


Quick Start
===========

Mockend is a simple, lightweight, and extensible REST API mocking Python library.
It can be used to mock any REST API endpoint, and can be used to mock any HTTP method.
the library is very easy to use and easy to extend. It just need configuration file, then it
will simulate the REST API response.

How to use
=======================

.. code-block:: bash

    mockend -c config.json

    * Serving Flask app 'mockend.__main__' (lazy loading)
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: on
    * Running on http://localhost:5555 (Press CTRL+C to quit)
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 141-969-228


In endpoint configuration available method with their configuration can be used to mock any HTTP method.
All configuration of response can be mock in method configuration.

Configuration examples
=======================

.. code-block:: json

    {
        "users": {
            "get": {
                "headers": {...},
                "status_code": "...",
                "mimetype": "...",
                "content_type": "...",
                "direct_passthrough": "...",
                "response": json_data
            }
        }
    }


To define nested endpoint configuration just define the nested endpoint name in the endpoint name.

Nested endpoints
=======================

.. code-block:: json

    {
        "users": {
            "JohnDoe": {
                "get": {...}
            }
        }
    }


To delay the response of endpoint just define delay attribute with a float value.

Delay endpoints
=======================

.. code-block:: json

    {
        "users": {
            "get": {
                "delay": 0.1,
                ...
            }
        }
    }

To generate chuck response set the chuck attribute with a True value and chunk size in chunk_size attribute.

chunk response
=======================

.. code-block:: json

    {
        "users": {
            "get": {
                "chunked": True,
                "chunk_size": 2,
                ...
            }
        }
    }


To simulate dummy to generate same response for same request just define dummy attribute with a True value.

Dummy endpoint
=======================

.. code-block:: json

    {
        "users": {
            "post": {
                "dummy": True
            }
        }
    }

Interactive mode is available to interact with the mockend server.
To start interactive mode just run the following command.
It is easy to use. Just define method and send request to create, update, delete or retrieve data

Interactive mode
=======================

.. code-block:: json

    {
        "users": {
            "interactive": True,
            "get": {...},
            "post": {...}
            "data" : {...}
        }
    }

Documentation: https://mghorbani2357.github.io/Mockend/