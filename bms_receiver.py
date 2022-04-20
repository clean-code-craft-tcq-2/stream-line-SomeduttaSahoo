# I was not able to run the sender, (always calling unexisting file "generic_libs")
# From bms_output_handler.py I took the format \t sensor: value

def read_attributes(stringToRead):
    attributes = {
        "charging_temperature" : [],
        "charge_rate" : [],
        "SOC" : []
    }
    for line in stringToRead.split("\t"):
        for attribute in attributes.keys():
            if(attribute in line):
                attributes[attribute].append( float( line[line.find(":")+1:]) )
                break
    return attributes
#statistics
def show_statistics(attributes):
    toPrint = ""
    for attribute in attributes.keys():
        toPrint += attribute+" max value = "+str(max(attributes[attribute])) + "\n"
        toPrint += attribute+" min value = "+str(min(attributes[attribute])) + "\n"
    print(toPrint)
    return toPrint

if __name__ == '__main__':
    values = read_attributes(testString)
    show_statistics(values)