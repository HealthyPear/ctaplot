#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
# import sys
import os
from setuptools import setup, find_packages


# def package_files(directory):
#     paths = []
#     for (path, directories, filenames) in os.walk(directory):
#         for filename in filenames:
#             paths.append(os.path.join('.', path, filename))
#             # paths.append(filename)
#     return paths
#
# dataset = package_files('data')
#
# print("dataset {}".format(dataset))


setup(name='ctaplot',
      version=0.2,
      description="metrics and plots for low-level IACT data analysis",
      # these should be minimum list of what is needed to run (note
      # don't need to list the sub-dependencies like numpy, since
      # astropy already depends on it)
      install_requires=[
          'numpy',
          'matplotlib>=2.0',
          'scipy>=0.19',
      ],
      # packages=['ctaplot'],
      packages=find_packages(),
      tests_require=['pytest'],
      author='Thomas Vuillaume',
      author_email='thomas.vuillaume@gmail.com',
      license='MIT',
      url='https://github.com/vuillaut/ctaplot',
      long_description='',
      classifiers=[
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Development Status :: 3 - Alpha',
      ],
      # include_package_data=True,
      package_data={'ctaplot': ['data/simu_mc/gamma_20deg_0deg_cta-prod3-LaPalma_run_header.json'] },
      # data_files=[('ctaplot/', dataset),
      #             # ('ctaplot/', ['./share/simu_mc/gamma_20deg_0deg_cta-prod3-LaPalma_run_header.json'])
      #             ],
      )
