# Test runner to be included here
import os
import unittest
import nose
import logging

from flask_script import Manager

from app import create_app

logging.basicConfig()
app = create_app(config_name=os.getenv('APP_SETTINGS'))

manager = Manager(app)


@manager.command
def test_runner_unit():
    """Test Runner unittest. No coverage"""
    app_tests = unittest.TestLoader() \
        .discover('./app/tests/', pattern='test*.py')
    test_result = unittest.TextTestRunner(verbosity=2).run(app_tests)
    if test_result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
