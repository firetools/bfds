# BFDS repository

**BFDS** is a [Blender](https://www.blender.org) add-on that makes it easy to create and manage [NIST Fire Dynamics Simulator (FDS)](https://pages.nist.gov/fds-smv/) models.

## Testing with `pytest`

###  Before

Before executing the tests, you need to install your testing dependencies inside the builtin Blender Python interpreter. To get the interpreter location you can use the CLI utility pytest-blender, something like:

```bash
blender_python="$(pytest-blender --blender-executable ../blender-4.5.2-linux-x64/blender)"
$blender_python -m ensurepip
$blender_python -m pip install pytest
```

### After

After installing dependencies, just call pytest as usually:

```bash
cd dev
pytest
```

