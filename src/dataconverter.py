
class DataConverter():
    def convert_data(self, rundata):
        converted_data = {'date':[], 'speed': [], 'pace': []}
        for run in rundata:
            converted_data['date'].append(run.adjusted_date)
            converted_data['speed'].append(run.adjusted_speed)
            converted_data['pace'].append(run.adjusted_pace)

        return converted_data
