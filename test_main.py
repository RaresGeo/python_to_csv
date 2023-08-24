import unittest
import os
import json
from main import main as fetch_data


class TestFetchData(unittest.TestCase):

    def setUp(self):
        # Delete the output.json file before running the test, if it exists
        if os.path.exists('output.json'):
            os.remove('output.json')

    def test_fetch_data(self):
        fetch_data(None)

        self.assertTrue(os.path.exists('output.json'), "output.json file not found")

        with open('output.json', 'r') as f:
            output_data = json.load(f)

        self.assertIn('data', output_data, "'data' key not found in JSON")
        self.assertIsInstance(output_data['data'], list, "'data' is not a list")
        self.assertTrue(len(output_data['data']) >= 1, "'data' list is empty")

    def test_non_existent_header(self):
        # Expect an exception when a non-existent header is passed
        with self.assertRaises(Exception) as context:
            fetch_data(['nonExistentHeader'])

        self.assertTrue("Field 'nonExistentHeader' not found in CSV headers." in str(context.exception))

    def test_specific_headers(self):
        # Test fetching data with specific headers: "clicks", "medium", "source"
        fetch_data(['clicks', 'medium', 'source'])

        # Check that output.json file has been created
        self.assertTrue(os.path.exists('output.json'))

        # Load JSON data from the file
        with open('output.json', 'r') as f:
            data = json.load(f)

        # Assert the file has a "data" attribute and it is a list
        self.assertTrue("data" in data)
        self.assertIsInstance(data['data'], list)

        # Assert the list is not empty
        self.assertTrue(len(data['data']) > 0)

        # Assert that every entry contains only the specified attributes
        for entry in data['data']:
            self.assertSetEqual(set(entry.keys()), {'clicks', 'medium', 'source'})
