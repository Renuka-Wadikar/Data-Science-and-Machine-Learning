from setuptools import find_packages,setup
from typing import List

HYPEN_E = '-e .'

def get_requirements(file:str) ->List[str]:
    """
     This function will return list of requirement
    Args:
        file (str): filepath

    Returns:
        List[str]: list of requirements
    """
    requirement = []
    with open(file,'r') as f:
        requirement = f.readlines()
        requirement = [req.replace('\n','') for req in requirement]
        
        if HYPEN_E   in requirement: 
            requirement.remove(HYPEN_E)
    return requirement


setup(
    
name = 'mlproject',
version='0.01',
author='Renuka',
author_email='wadikarrenuka@gmail.com',
packages= find_packages(),
install_requires = get_requirements('requirements.txt')
)