import os
import sys
import json
import string
import unittest
import subprocess

# Configure path environment
TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(TESTS_ROOT)

sys.path.append(PROJECT_ROOT)

os.environ['BOOKS_PATH'] = TESTS_ROOT

# from audiobible.kjv.spiders.bible import BibleSpider
from audiobible.kjv import settings

content_file = os.path.join(TESTS_ROOT, settings.DATA_STORE, settings.CONTENT_FILE)
speakers_file = os.path.join(TESTS_ROOT, settings.DATA_STORE, settings.SPEAKERS_FILE)
topics_file = os.path.join(TESTS_ROOT, settings.DATA_STORE, settings.TOPICS_FILE)


class AudioBibleListTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_list(self):
        import audiobible
        result = audiobible.use_keyword_args(**{
            'operation': ['list']
        })
        assert os.path.exists(content_file)
        with open(os.path.join(content_file), 'r') as lines:
            for line in lines:
                data = json.loads(line)
                assert data['name'].replace(' ', '_') in result


class AudioBibleListSpeakersTest(unittest.TestCase):
    def setUp(self):
        self.speakers = dict(zip(list(string.ascii_uppercase), [
            [], [], [], [], [], [], [], [], [], [], [], [], [],
            [], [], [], [], [], [], [], [], [], [], [], [], [],
        ]))
        letters = string.ascii_uppercase
        for l in range(len(letters)):
            path = speakers_file % letters[l]
            # print path
            if os.path.exists(path):
                with open(path, 'r') as lines:
                    for line in lines:
                        data = json.loads(line)
                        # print data
                        if data['name'][0] == letters[l]:
                            self.speakers[letters[l]].append([data['name'], data['path']])

    def test_list_speakers(self):
        # print self.speakers
        pass
# class AudioBibleInitTest(unittest.TestCase):
#     def setUp(self):
#         subprocess.call(['rm', '-rf', os.path.join(TESTS_ROOT, settings.DATA_STORE)])
#
#     def test_init(self):
#         import audiobible
#         audiobible.use_keyword_args(**{
#             'operation': ['init']
#         })
#         #
#         assert os.path.exists(content_file)


# class AudioBibleInitSpeakersTest(unittest.TestCase):
#     def test_speakers(self):
#         import audiobible
#         audiobible.use_keyword_args(**{
#             'operation': ['init', 'speakers']
#         })
#         #
#         assert os.path.exists(speakers_file)
#
#
# class AudioBibleInitTopicsTest(unittest.TestCase):
#     def test_topics(self):
#         import audiobible
#         audiobible.use_keyword_args(**{
#             'operation': ['init', 'topics']
#         })
#         #
#         assert os.path.exists(topics_file)


# class AudioBibleLoadTest(unittest.TestCase):
#     def test_load(self):
#         import audiobible
#         reload(audiobible)
#         audiobible.use_keyword_args(**{
#             'operation': ['load']
#         })
#         #
#
#         assert os.path.exists()



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
#
# class AudioBibleListTest(unittest.TestCase):
#     def test_list(self):
#         import audiobible
#
#         assert audiobible.use_keyword_args(**{
#             'operation': 'list'
#         })