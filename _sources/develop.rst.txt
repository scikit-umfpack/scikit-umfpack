Development
===========

Code
----

``scikits.umfpack`` development is done on Github at
https://github.com/scikit-umfpack/scikit-umfpack

You can check the latest sources with the command::

  git clone https://github.com/scikit-umfpack/scikit-umfpack.git

or if you have write privileges::

  git clone git@github.com:scikit-umfpack/scikit-umfpack.git

Editable install
----------------

The editable install requires ``meson-python``::

  pip install meson-python

Then (see `meson editable installs documentation
<https://mesonbuild.com/meson-python/how-to-guides/editable-installs.html>`_)::

  pip install --no-build-isolation -e .

Testing
-------

``pytest`` is required to run the test suite::

  pip install pytest

After completing the editable install command, run::

  pytest

Building documentation
----------------------

To build and view the documentation, do::

  cd docs && make html && cd ..
  firefox docs/_build/html/index.html
