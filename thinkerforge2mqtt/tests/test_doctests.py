from bx_py_utils.test_utils.unittest_utils import BaseDocTests

import thinkerforge2mqtt


class DocTests(BaseDocTests):
    def test_doctests(self):
        self.run_doctests(
            modules=(thinkerforge2mqtt,),
        )
