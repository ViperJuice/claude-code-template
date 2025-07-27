from setuptools import setup, Extension, find_packages
import numpy as np
import os

# Define the extension module
ext_modules = [
    Extension(
        'math_engine._math_engine',
        sources=['src/bindings.cpp'],
        include_dirs=[
            np.get_include(),
            '../engine/include',
            'include'
        ],
        libraries=['mathengine'],
        library_dirs=['../engine/build'],
        language='c++',
        extra_compile_args=['-std=c++17'],
    )
]

setup(
    name='math_engine',
    version='1.0.0',
    description='Python bindings for C++ Math Engine',
    packages=find_packages(),
    ext_modules=ext_modules,
    install_requires=[
        'numpy>=1.20.0',
    ],
    python_requires='>=3.7',
    zip_safe=False,
)