.. include:: links.inc

Release Tasks
=============

#. Setup `pypi`_ and `testpypi`_ accounts if you do not already have ones. Then
   put the following into your ``~/.pypirc``::

     [distutils]
         pypi
         testpypi

     [pypi]
     username = your_pypi_name
     password = your_pypi_password

     [testpypi]
     repository = https://test.pypi.org/legacy/
     username = your_testpypi_name
     password = your_testpypi_password

   Then register your accounts::

     # testpypi
     python3 setup.py register -r https://testpypi.python.org/pypi

     # pypi
     python3 setup.py register

   To be able to upload to pypi/testpypi without sending your password in plain
   text, install `twine`_. An upload is then done simply by::

     # testpypi
     twine upload -r testpypi <filenames>

     # pypi
     twine upload <filenames> # Be careful!

   **WARNING:** Uploads to `pypi`_ are permanent and cannot be updated later! If
   a wrong file is uploaded, the only fix is to create a new release. Always
   use `testpypi`_ first.

#. Bump version number:

   - in ``meson.build``
   - in ``pyproject.toml``
   - in ``docs/conf.py``

#. Regenerate and review the documentation::

     cd docs && make html && cd ..
     firefox docs/_build/html/index.html

#. Install and test the git version that is to be released. In the git
   repository, do::

     pip install .
     cd docs
     pytest --pyargs scikits.umfpack
     cd ..

#. Create a source distribution tarball, install it and test it::

     pip install build
     python3 -m build

   Unpack the source tarball, cd to it, and repeat the previous step.

#. If OK, merge the version branch.

#. Upload to `testpypi`_ and test::

     python3 -m build
     twine upload -r testpypi dist/scikit_umfpack-<version>.tar.gz

   Note: if the upload fails with `This filename has previously been used, you
   should use a different version.`, just change the version (see step 2)
   to another value.

   Create a test install using `venv`_::

     python3 -m venv venv
     source venv/bin/activate

     python3 -m pip install -U -i --pre https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ scikit-umfpack

     python3 -m pip install pytest
     pytest --pyargs scikits.umfpack

     deactivate

#. If OK, tag the version in git & push to github.

#. Upload to `pypi`_:

   - Check the version numbers (see step 2).
   - Do::

       python3 -m build
       twine upload dist/scikit_umfpack-<version>.tar.gz

   - Test::

     python3 -m venv venv
     source venv/bin/activate

     python3 -m pip install -U scikit-umfpack

     python3 -m pip install pytest
     pytest --pyargs scikits.umfpack

     deactivate

#. Update gh-pages::

     ./docs/do-gh-pages.sh
     git push -f origin gh-pages
