import random

FLOAT_DECIMAL_PLACE = 2
INTEGER_DECIMAL_PLACE = None


def set_bms_parameter_decimal_place(bms_parameter, bms_parameters_with_range):
    if type(bms_parameters_with_range[bms_parameter]['max']) == float:
        decimal_place = FLOAT_DECIMAL_PLACE
    else:
        decimal_place = INTEGER_DECIMAL_PLACE
    return decimal_place


def generate_bms_readings(bms_parameters_with_range):
    bms_readings = {}
    for bms_parameter in bms_parameters_with_range:
        decimal_place = set_bms_parameter_decimal_place(bms_parameter, bms_parameters_with_range)
        bms_readings[bms_parameter] = round(random.uniform(bms_parameters_with_range[bms_parameter]['min'],
                                                           bms_parameters_with_range[bms_parameter]['max']),
                                            decimal_place)
    return bms_readings
