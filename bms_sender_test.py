import unittest
from io import StringIO
from mock import patch

from generic_libs import bms_input_handler as bms_input
from generic_libs import bms_generator
from generic_libs import bms_output_handler
import bms_sender


class BMSSenderTest(unittest.TestCase):
    bms_parameters_with_range = {'charging_temperature': {'min': 0, 'max': 45},
                                 'charge_rate': {'min': 0, 'max': 0.8},
                                 'SOC': {'min': 20, 'max': 80}}

    """
    ******************************************************
            Complete BMS Sender Functionality Test
    ******************************************************
    """

    def test_if_bms_sender_successfully_streams_data(self):
        self.assertEqual(bms_sender.stream_bms_readings("local_database", "console", self.bms_parameters_with_range,
                                                        0.2, 3), 'BMS_STREAMING_COMPLETE')

    def test_if_bms_sender_reports_error_for_invalid_inputs(self):
        bms_parameters_with_range = {}
        self.assertEqual('INVALID_INPUT_STREAM_FAILED',
                         bms_sender.stream_bms_readings("local_database", "console", bms_parameters_with_range, 1,
                                                        None))

    """
    ******************************************************
                    File: bms_input_handler
    ******************************************************
    """

    def test_if_bms_io_type_supported_for_valid_data(self):
        self.assertTrue(bms_input.is_within_supported_types('local_database', 'console'))

    def test_if_bms_io_type_unsupported_for_invalid_data(self):
        invalid_input_list = [(None, None), ('cloud', 'console'), ('local_database', 'logger')]
        for invalid_input in invalid_input_list:
            self.assertFalse(bms_input.is_within_supported_types(invalid_input[0], invalid_input[1]))

    def test_checks_if_bms_parameters_are_valid(self):
        bms_parameters = [{'SOC': {'min': 20, 'max': 80}, 'charge_rate': {'min': 0, 'max': 0.8}},
                          {'charging_temperature': {'min': 0, 'max': 45}, 'charge_rate': {'min': 0, 'max': 0.8},
                           'SOC': {'min': 20, 'max': 80}}]
        for bms_parameter in bms_parameters:
            self.assertTrue(bms_input.is_bms_parameters_valid(bms_parameter))

    def test_checks_if_bms_parameters_are_invalid(self):
        invalid_bms_parameters = [{}, {'battery_load': {'min': 10, 'max': 50}},
                                  {'SOC': {'min': 20, 'max': 80}, 'SOH': {'min': 0, 'max': 0.8}},
                                  {'SOC': {'min': 20, 'max': 80}, 'SOH': {'min': 0, 'max': 0.8},
                                   'charge_rate': {'min': 0, 'max': 0.8}}]
        for bms_parameter in invalid_bms_parameters:
            self.assertFalse(bms_input.is_bms_parameters_valid(bms_parameter))

    def test_checks_is_stream_parameters_are_valid(self):
        self.assertTrue(bms_input.is_stream_parameters_valid(2, 40))

    def test_checks_is_stream_parameters_are_invalid(self):
        invalid_stream_parameters = [(None, None), (0, None), (None, 0), (0, 0)]
        for stream_parameter in invalid_stream_parameters:
            self.assertFalse(bms_input.is_stream_parameters_valid(stream_parameter[0], stream_parameter[1]))

    def test_checks_if_input_is_valid(self):
        self.assertEqual(bms_input.is_input_valid("local_database", "console", self.bms_parameters_with_range, 1, 50),
                         'VALID_INPUT')
        self.assertEqual(bms_input.is_input_valid("local_database", "console", self.bms_parameters_with_range, None, 0),
                         'INVALID_INPUT')

    """
     ******************************************************
                    File: bms_generator
     ******************************************************
    """

    def test_yields_decimal_place_for_rounding_off_bms_data(self):
        expected_output = [bms_generator.INTEGER_DECIMAL_PLACE, bms_generator.FLOAT_DECIMAL_PLACE,
                           bms_generator.INTEGER_DECIMAL_PLACE]
        input_values = ['charging_temperature', 'charge_rate', 'SOC']
        for i in range(2):
            self.assertEqual(bms_generator.set_bms_parameter_decimal_place(input_values[i],
                                                                           self.bms_parameters_with_range),
                             expected_output[i])

    """
     *******************************************************
                    File: bms_output_handler
     *******************************************************
    """

    def test_print_to_console_using_mock_stdout(self):
        bms_readings = {'charging_temperature': 38, 'charge_rate': 0.12}
        expected_output = 'charging_temperature: 38 \tcharge_rate: 0.12 \n'
        with patch('sys.stdout', new=StringIO()) as fake_print:
            bms_output_handler.print_bms_readings_to_console(bms_readings)
            self.assertEqual(fake_print.getvalue(), expected_output)

    @patch('time.sleep', return_value=None)
    def test_delay_using_mock_timer(self, mock_time_sleep):
        bms_output_handler.set_delay(2)
        # Test that the mock should only be called once
        self.assertEqual(1, mock_time_sleep.call_count)

    """
     *******************************************************
                    File: bms_sender
     *******************************************************
    """

    @patch('generic_libs.bms_generator.generate_bms_readings')
    def test_get_bms_readings_from_mock_bms_generator(self, mock_bms_generator):
        mock_bms_generator.return_value = {'charging_temperature': 30, 'charge_rate': 0.49, 'SOC': 39}
        self.assertEqual(bms_sender.get_bms_readings_from_bms_generator(self.bms_parameters_with_range),
                         {'charging_temperature': 30, 'charge_rate': 0.49, 'SOC': 39})

    @patch('generic_libs.bms_generator.generate_bms_readings')
    def test_send_bms_readings_with_mock_bms_generator_for_failure_scenario(self, mock_bms_generator):
        mock_bms_generator.return_value = {}
        self.assertEqual(bms_sender.send_bms_readings_to_console(bms_sender.get_bms_readings_from_bms_generator
                                                                 (self.bms_parameters_with_range)),
                         'STREAM_FAILED_INVALID_BMS_DATA')


if __name__ == '__main__':
    unittest.main()
