"""Tasks to test and release the package."""
from invoke import Collection, task
import iniconfig
import os
import tomli
import yaml

PYTHON = 'python'
PROJECT = 'ubermagutil'

ns = Collection()


@task
def unittest(c):
    """Run unittests."""
    c.run(f'{PYTHON} -c "import sys; import {PROJECT};'
          f' sys.exit({PROJECT}).test()"')

# coverage, docs, ipynb, pycodestyle


@task
def all(unittest):
    """Run all tests."""


@task
def build_dists(c):
    """Build sdist and wheel."""
    print('build dists')
    if os.path.exists('dist'):
        os.rmdir('dist')
    c.run(f'{PYTHON} -m build')


@task(build_dists)
def upload(c):
    """Upload package to PyPI."""
    print('Uploading to PyPI... [COMMENTED OUT FOR SAFETY]')
    # c.run('twine aupload dist/*')


@task
def release(c):
    """Run the whole release process.

    Steps:
    - Pull all changes in ``master`` and ``stable`` branch.
    - Merge ``master`` into ``stable``.
    - Tag last commit using version information from setup.cfg/pyproject.toml.
    - Build package (``sdist`` and ``wheel``).
    - Upload package to PyPI.
    - Update binder environment file and commit changes.
    - Push all changes and new tags.
    """
    # sanity checks while we have two places containing the version.
    with open('pyproject.toml', 'rb') as f:
        config = tomli.load(f)
    toml_version = config['project']['version']
    version = iniconfig.IniConfig('setup.cfg').get('metadata', 'version')
    assert toml_version == version, ('Different versions in pyproject.toml and'
                                     ' setup.cfg. Aborting.')

    c.run('git checkout master')
    c.run('git pull')
    c.run('git checkout stable')
    c.run('git pull')

    c.run('git merge master')
    c.run(f'git tag {version}')

    upload(c)

    # update binder environment file
    with open('binder/environment.yml', 'rt') as f:
        binder_env = yaml.load(f, Loader=yaml.Loader)
    updated_dependencies = []
    for dep in binder_env['dependencies']:
        if dep.startswith('ubermagutil'):  # {{ package }}
            updated_dependencies.append(f'ubermagutil=={version}')
        else:
            updated_dependencies.append(dep)
    binder_env['dependencies'] = updated_dependencies
    with open('binder/environment.yml', 'wt') as f:
        yaml.dump(binder_env, f)
    c.run('git add binder/environment.yml')
    c.run('git commit -m "update binder environment.yml"')

    print('TODO git push ...[COMMENTED OUT FOR SAFETY]')
    # c.run('git push')
    # c.run('git push --tags')
    # c.run('git checkout master')
    # c.run('git merge stable')  # updated binder environment
    # c.run('git push)


ns.add_task(build_dists)
ns.add_task(upload)
ns.add_task(release)

test = Collection('test')
test.add_task(unittest)
test.add_task(all)
ns.add_collection(test)
