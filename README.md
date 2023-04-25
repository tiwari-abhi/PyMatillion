# PyMatillion

This is a Python wrapper for interacting with the REST API for Matillion.

For full documentation visit [Documentation Link](https://tiwari-abhi.github.io/PyMatillion/reference).

## Installation

    pip install pymatillion

## Releasing
Releases are automatically built in GitHub actions pipeline when a tag is pushed.

1. Use bumpver to increment the version string across the project.
```
bumpver update -p/-m/--major --no-commit
```
2. Copy the updated version string from pyproject.toml 
3. Tag the relevant commit on the master branch with the version from step 2 

 ``` 
 # Set next version number
 export RELEASE=x.x.x`

 # Create tags
 git commit --allow-empty -m "Release $RELEASE"
 git tag -a $RELEASE -m "Version $RELEASE"
 
 # Push
 git push origin --tags
``` 