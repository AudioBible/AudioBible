import os
import sys
import unittest
import subprocess

# Configure path environment
TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(TESTS_ROOT)

sys.path.append(PROJECT_ROOT)

os.environ['BOOKS_PATH'] = TESTS_ROOT

# from audiobible.kjv.spiders.bible import BibleSpider
from audiobible.kjv import settings

data_path = os.path.join(settings.DATA_STORE, settings.CONTENT_FILE)


class AudioBibleInitTest(unittest.TestCase):
    def setUp(self):
        pass
        # subprocess.call(['rm', '-rf', os.path.join(TESTS_ROOT, settings.DATA_STORE)])

    def test_init(self):
        import audiobible
        audiobible.use_keyword_args(**{
            'operation': 'init'
        })

        assert os.path.exists(data_path)


# class AudioBibleLoadTest(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     def test_load(self):
#         import audiobible
#         audiobible.use_keyword_args(**{
#             'operation': 'load'
#         })
#
#         assert os.path.exists(data_path)

class AudioBibleListTest(unittest.TestCase):
    def test_list(self):
        import audiobible

        assert audiobible.use_keyword_args(**{
            'operation': 'list'
        })