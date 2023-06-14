import unittest
from unittest.mock import patch
from src.dto import Reading
from src.handlers import save_data


class SaveDataTestCase(unittest.TestCase):

    @patch('flask.wrappers.Request')
    @patch('src.handlers.add_reading')
    def test_save_data(self, mock_add_reading, mock_request):
        # Mock the request data
        mock_request.data.decode.return_value = "1649941817 Voltage 1.34\n1649941818 Voltage 1.35\n1649941819 Current 12.0\n1649941820 Current 14.0"

        # Call the save_data function
        save_data(mock_request)

        # Verify the behavior of add_reading
        expected_records = [
            Reading(time="2022-04-14T18:40:17.000000Z", name="Voltage", value=1.34),
            Reading(time="2022-04-14T18:40:18.000000Z", name="Voltage", value=1.35),
            Reading(time="2022-04-14T18:40:19.000000Z", name="Current", value=12.0),
            Reading(time="2022-04-14T18:40:20.000000Z", name="Current", value=14.0)
        ]

        self.assertEqual(mock_add_reading.call_count, 4)  # Verify that add_reading was called 4 times

        # Verify the arguments passed to add_reading
        for i, call_args in enumerate(mock_add_reading.call_args_list):
            args, _ = call_args
            self.assertEqual(args[0], str(1649941817 + i))  # Verify the key argument
            self.assertEqual(args[1], expected_records[i])  # Verify the record argument


if __name__ == '__main__':
    unittest.main()
