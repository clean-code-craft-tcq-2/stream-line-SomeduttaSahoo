from generic_libs import bms_generator
from generic_libs import bms_output_handler as output
from generic_libs.bms_input_handler import is_input_valid


def get_bms_readings_from_bms_generator(bms_parameters):
    return bms_generator.generate_bms_readings(bms_parameters)


def send_bms_readings_to_console(bms_parameters):
    if len(bms_parameters) != 0:
        return output.print_bms_readings_to_console(bms_parameters)
    else:
        return 'STREAM_FAILED_INVALID_BMS_DATA'


send_bms_readings = {
    'console': send_bms_readings_to_console,
}

get_bms_readings = {
    'local_database': get_bms_readings_from_bms_generator,
}


def stream_bms_readings(bms_input, bms_output, bms_parameters, stream_speed, num_of_readings):
    if is_input_valid(bms_input, bms_output, bms_parameters, stream_speed, num_of_readings) == 'VALID_INPUT':
        for stream_count in range(num_of_readings):
            send_bms_readings[bms_output](get_bms_readings[bms_input](bms_parameters))
            output.set_delay(stream_speed)
        return 'BMS_STREAMING_COMPLETE'
    else:
        return 'INVALID_INPUT_STREAM_FAILED'


if __name__ == '__main__':

    bms_parameters_with_range = {'charging_temperature': {'min': 0, 'max': 45},
                                 'charge_rate': {'min': 0, 'max': 0.8}}
    bms_result = stream_bms_readings("local_database", "console", bms_parameters_with_range, 1, 50)
    if bms_result is not None:
        print('\n', bms_result)
