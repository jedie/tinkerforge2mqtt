from bx_py_utils.test_utils.unittest_utils import BaseDocTests

import tinkerforge2mqtt


class DocTests(BaseDocTests):
    def test_doctests(self):
        self.run_doctests(
            modules=(tinkerforge2mqtt,),
        )
