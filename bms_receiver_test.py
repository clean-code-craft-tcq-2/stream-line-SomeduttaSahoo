import unittest
from bms_receiver import read_attributes, show_statistics

class receiverTest(unittest.TestCase):

    def test_read_attributes(self):
        testString = ""+\
                "\t charging_temperature:10"+\
                "\t charge_rate:0.2"+\
                "\t SOC:44"+\
                "\t charging_temperature:11"+\
                "\t charge_rate:0.4"+\
                "\t SOC:60"+\
                "\t charging_temperature:20"+\
                "\t charge_rate:0.3"+\
                "\t SOC:50"
        values = read_attributes(testString)
        self.assertEqual(values["charging_temperature"],[10.0,11.0,20.0])
    
    def test_show_statistics(self):
        values = {
            "charging_temperature":[20.0,30.0,40.0],
            "charge_rate":[0.1,0.7,0.5],
            "SOC":[50.0,60.0,20.0]
        }
        printed = show_statistics(values)
        self.assertTrue("SOC max value = 60.0" in printed)
        self.assertTrue("SOC min value = 20.0" in printed)

if __name__ == '__main__':
    unittest.main()