from setuptools import setup, find_packages

## All python datatypes are coming from typing library
from typing import List

## Declaring variables for setup function
PROJECT_NAME="housing-predictor"
PROJECT_VERSION="0.0.1"
PROJECT_AUTHOR="Anjali Atule"
DESCRIPTION="First End to End Machine Learning Project"
PACKAGES=["housing"]
REQUIREMENT_FILE_NAME="requirements.txt"

#function that will read requirements.txt file and return requirements as list with string values.
def get_requirements_list()->List[str]:
    """
    Description-This function will return list of libraries mentioned in requirements.txt file 
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e .")



setup(
    name=PROJECT_NAME,
    version=PROJECT_VERSION,
    author=PROJECT_AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=get_requirements_list()
)