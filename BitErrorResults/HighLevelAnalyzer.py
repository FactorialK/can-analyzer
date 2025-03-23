# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting


# High level analyzers must subclass the HighLevelAnalyzer class.
class Hla(HighLevelAnalyzer):
    # List of settings that a user can set for this High Level Analyzer.

    # An optional list of types this analyzer produces, providing a way to customize the way frames are displayed in Logic 2.
    result_types = {
        'attacked': {
            'format': 'Error count: {{data.error_flag_count}}'
        }
    }

    def __init__(self):
        '''
        Initialize HLA.

        Settings can be accessed using the same name used above.
        '''
        self.error_flag_count = 0
        self.error_detect_count = 0
        self.errorType = 'none'

    def decode(self, frame: AnalyzerFrame):
        '''
        Process a frame from the input analyzer, and optionally return a single `AnalyzerFrame` or a list of `AnalyzerFrame`s.

        The type and data values in `frame` will depend on the input analyzer.
        '''
        if frame.type == 'Lengthen_Edge':
            self.errorType = 'Lengthen'
        elif frame.type == 'Oscillating_Edge':
            self.errorType = 'Flip'

        if frame.type == 'can_error_':
            self.error_flag_count += 1
            error_flag_count = self.error_flag_count
            
        if self.errorType != 'none':
            self.error_detect_count += 1
            error_detect_count = self.error_detect_count
        # Return the data frame itself
            return AnalyzerFrame('attacked', frame.start_time, frame.end_time, {
                'error_flag_count' : error_flag_count,
                'error_detect_count' : error_detect_count
            })
