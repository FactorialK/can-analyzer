# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting


# High level analyzers must subclass the HighLevelAnalyzer class.
class CANBitErrorDetecting(HighLevelAnalyzer):

    result_types = {
        'attacked_frame': {
            'format': '{{data.datastring}}'
        }
    }

    def __init__(self):
        self.currentStart = 0
        self.currentEnd = 0
        self.currentId = 0
        self.currentData = b''
        self.currentType = ' None'

    def decode(self, frame: AnalyzerFrame):

        if frame.type == 'identifier_field':
            self.currentStart = frame.start_time
            self.currentId = frame.data['identifier']
            if (self.currentId == 0xBE or self.currentId == 0xBF):
                return AnalyzerFrame('attacked_frame', self.currentStart, frame.end_time, {
                'datastring': 'Error Attack Start'
            })
        elif frame.type == 'Lengthen_Edge':
            self.currentStart = frame.start_time
            self.currentType = 'Lengthen'
            # self.currentEnd = frame.end_time
        elif frame.type == 'Oscillating_Edge':
            self.currentStart = frame.start_time
            self.currentType = 'Flip'
            # self.currentEnd = frame.end_time
        elif frame.type == 'ack_field':
            self.currentType = ' None'
            return
        elif frame.type == 'can_error_'and self.currentType != ' None':
            # Return the data frame
            datastring = ('{:03X}'.format(self.currentId) + '#'
                        + ' Error Type: ' + self.currentType)

            print(datastring) # If streaming to the terminal, this will be printed

            self.currentType = ' None'
            return AnalyzerFrame('attacked_frame', self.currentStart, frame.end_time, {
                # 'id': self.currentId,
                # 'data': self.currentData,
                'datastring': datastring,
                # 'errortype': self.currentType
            })