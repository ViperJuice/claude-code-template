"""Setup script for Claude Code setup tools."""

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='claude-code-setup',
    version='1.0.0',
    description='Claude Code native sub-agent setup tools',
    author='Claude Code Team',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'claude-setup=claude_setup.setup_native_subagents:main',
            'claude-detect-language=claude_setup.detect_language:main',
            'claude-inventory=claude_setup.inventory_check:main',
            'claude-cleanup=claude_setup.cleanup_legacy:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)