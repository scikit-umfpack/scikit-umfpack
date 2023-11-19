#!/bin/bash
set -e -u
cd "`dirname "$0"`" && make clean html && cd ..
rm -rf build/gh-pages
mkdir -p build/gh-pages
git -C build/gh-pages init
git -C build/gh-pages checkout -b gh-pages
rsync -a docs/_build/html/ build/gh-pages/
touch build/gh-pages/.nojekyll
git -C build/gh-pages add .
git -C build/gh-pages commit -m "Generated from sources" -a
git branch -D gh-pages || true
git fetch build/gh-pages
git branch gh-pages FETCH_HEAD
rm -rf build/gh-pages
echo "The gh-pages branch is now updated, you can now push it to github: git push -f origin gh-pages"
