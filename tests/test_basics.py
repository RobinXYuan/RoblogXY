from flask import current_app

from basics import BasicTestCaseSettings


class BasicTestCase(BasicTestCaseSettings):

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_mode_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])