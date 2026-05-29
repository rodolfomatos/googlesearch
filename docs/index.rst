.. googlesearch documentation master file

Welcome to googlesearch's documentation!
==========================================

**Unofficial Python bindings to the Google search engine.**

.. note:: This project is not affiliated with Google.

Installation
------------

::

    pip install google

Or from the checkout with Playwright support:

::

    pip install google[playwright]
    playwright install chromium

Quick start
-----------

.. code-block:: python

    from googlesearch import search

    for url in search('"Breaking Code" WordPress blog', stop=20):
        print(url)

CLI
---

::

    google --stop=5 "opencode agents"

Reference
---------

.. automodule:: googlesearch
   :members:
   :undoc-members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
