INPUT_TYPES = ['local_database']
OUTPUT_TYPES = ['console']

DEFAULT_READING_NUM = 15
DEFAULT_SPEED = 1

BMS_PARAMETERS = ['charging_temperature', 'SOC', 'charge_rate']

BMS_CHECK = ['0', 'None']


def is_within_supported_types(bms_input, bms_output):
    return (bms_input in INPUT_TYPES) and (bms_output in OUTPUT_TYPES)


def is_bms_parameters_valid(bms_parameters_with_range):
    if len(bms_parameters_with_range) != 0:
        result = ""
        for parameter in bms_parameters_with_range.keys():
            if parameter not in BMS_PARAMETERS:
                result = False
                break
            else:
                result = True
        return result
    else:
        return False


def is_stream_parameters_valid(stream_speed, num_of_readings):
    return (str(stream_speed) not in BMS_CHECK) and (str(num_of_readings) not in BMS_CHECK)


def is_input_valid(bms_input, bms_output, bms_parameters_with_range, stream_speed, num_of_readings):
    if is_within_supported_types(bms_input, bms_output) and is_stream_parameters_valid(stream_speed, num_of_readings) \
                                                                and is_bms_parameters_valid(bms_parameters_with_range):
        return 'VALID_INPUT'
    else:
        return 'INVALID_INPUT'
