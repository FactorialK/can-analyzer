# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting


# High level analyzers must subclass the HighLevelAnalyzer class.
class CANBitErrorDetecting(HighLevelAnalyzer):

    result_types = {
        'can_frame': {
            'format': '{{data.datastring}}'
        }
    }

    def __init__(self):
        self.currentStart = 0
        self.currentId = 0
        self.currentData = b''
        self.currentType = ' None'

    def decode(self, frame: AnalyzerFrame):

        if frame.type == 'identifier_field':
            self.currentStart = frame.start_time
            self.currentId = frame.data['identifier']
            self.currentData =b''
        # elif frame.type == 'data_field':
            # self.currentData = self.currentData + frame.data['data']
        elif frame.type == 'Oscillating_Edge':
            self.currentType = 'Flip'
        elif frame.type == 'Lengthen_Edge':
            self.currentType = 'Lengthen'
        elif frame.type == 'can_error_':
            # Return the data frame
            datastring = ('{:03X}'.format(self.currentId) + '#'
                        + '.'.join('{:02X}'.format(a) for a in self.currentData) + ' Error Type: ' + self.currentType)

            print(datastring) # If streaming to the terminal, this will be printed

            return AnalyzerFrame('can_frame', self.currentStart, frame.end_time, {
                'id': self.currentId,
                'data': self.currentData,
                'datastring': datastring,
                'errortype': self.currentType
            })