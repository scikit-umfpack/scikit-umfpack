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

# dict by dependency variable(s) name
dependencies = {}
for dep in dependency_list:
    for name in dep["meson_variables"]:
        dependencies[name] = dep

# get umfpack dependency
umfpack = dependencies.get("umfpack_dep")
if umfpack is None:
    sys.exit(f"umfpack_dep not found in dependencies: {', '.join(dependencies)}")

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
