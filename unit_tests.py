import unittest, json
from helpers import getUserInput, validateapiEndPoint, logMessage, makeApiRequest, getMessageAndWriteToFile, extractPortInfo
from container import runContainer, containerIsHealthy

class TestMyProgram(unittest.TestCase):
    def test_validateapiEndPoint_success(self):
        actual = validateapiEndPoint(endpoint="http://localhost:8800/some-thing")
        expected = True
        self.assertEqual(actual, expected)
    
    def test_validateapiEndPoint_fail(self):
        actual = validateapiEndPoint(endpoint="http://google.com:8800/some-thing")
        expected = False
        self.assertEqual(actual, expected)

    # def extractPortInfo(data)
    def test_extractPortInfo_success(self):
        with open("payload_correct.json") as f:
            data = f.read()
        # convert to json
        data = json.loads(data)
        actual = extractPortInfo(data)
        expected = (True, 9772, 8080)
        self.assertEqual(actual, expected)

    def test_extractPortInfo_success_incorrect(self):
        with open("payload_incorrect.json") as f:
            data = f.read()
        # convert to json
        data = json.loads(data)
        actual = extractPortInfo(data)
        expected = (False, "", "")
        self.assertEqual(actual, expected)

    def test_extractPortInfo_fail_incorrect(self):
        with open("payload_incorrect.json") as f:
            data = f.read()
        # convert to json
        data = json.loads(data)
        actual = extractPortInfo(data)
        expected = (False, "", "")
        self.assertEqual(actual, expected)
    
    def test_makeApiRequest_success(self):
        end_point = "http://localhost:6161/api/applications/conversation-app"
        actual = makeApiRequest(endpoint=end_point)
        with open("payload_correct.json") as f:
            data = f.read()
        data = json.loads(data)
        expected = (True, data)
        self.assertEqual(actual, expected)

    def test_makeApiRequest_fail(self):
        end_point = "http://localhost:6000/api/applications/conversation-app"
        actual = makeApiRequest(endpoint=end_point)
        expected = (False, "Connection_Error")
        self.assertEqual(actual, expected)