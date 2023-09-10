# ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD #

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

setup_args = generate_distutils_setup(
    packages=['image_stitcher'],
    package_dir={'image_stitcher': 'src/image_stitcher'}
)
 
setup(**setup_args)