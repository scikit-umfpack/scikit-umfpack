"""
workaround https://github.com/mesonbuild/meson/issues/8334

by getting dependency info from meson-info.
When dependency.as_dict() is added, can use that instead.
"""

import json
import os
import sys
from pathlib import Path


# load dependency list
meson_info = Path("meson-info")
with (meson_info / "intro-dependencies.json").open() as f:
    dependency_list = json.load(f)

# cast to a dict
dependencies = {dep["name"].lower(): dep for dep in dependency_list}

# get umfpack dependency
umfpack = dependencies.get("umfpack")
if "umfpack" not in dependencies:
    sys.exit(f"umfpack not found in dependencies: {', '.join(dependencies)}")

# load include directories from meson dep
includes = []
for include_dir in umfpack["include_directories"]:
    includes.append(f"-I{include_dir}")
# pkg-config puts includes in compile_args
for arg in umfpack["compile_args"]:
    # could this look different on Windows?
    if arg.startswith("-I"):
        includes.append(arg)

swig = sys.argv[1]
swig_argv = sys.argv[1:]
# insert includes after '-python'
swig_argv[2:2] = includes
# actually launch swig
os.execv(swig, swig_argv)
