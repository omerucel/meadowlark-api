from fabric.api import local

def remove_pyc():
    local('find . -name "*.pyc" -exec rm -rf {} \;')

def test_cover():
    local('python meadowlark/tests/runtests.py --with-coverage --cover-html --cover-package=meadowlark')

def test():
    local('python meadowlark/tests/runtests.py')