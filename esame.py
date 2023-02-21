class ExamException(Exception):
    pass


class CSVTimeSeriesFile:

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise ExamException('File Name Error')
        self.name = name

    def get_data(self) -> list:
        data = []
        try:
            file = open(self.name)
        except IOError:
            raise ExamException('Could not open/read file')
        for row in file:
            if len(row) > 1:
                row_data = row.split(',')
                if row_data[0] != 'date':
                    try:
                        dates = {item[0] for item in data}
                        if row_data[0] in dates:
                            raise ExamException('Duplicate Error')
                        if len(data) > 0 and row_data[0] < data[-1][0]:
                            raise ExamException('Timestamp Error')
                        number = int(row_data[1])
                        data.append([row_data[0], number if number >= 0 else None])
                    except ValueError:
                        data.append([row_data[0], None])
                        continue
        file.close()
        return data


def detect_similar_monthly_variations(time_series, years):
    if len(years) != 2:
        raise ExamException(f'length of years list: {len(years)}')
    if abs(years[0]-years[1]) != 1:
        raise ExamException(f'{years[0]} and {years[1]} are not consecutive')
    dates = {item[0][0:4] for item in time_series}
    for year in years:
        if not str(year) in dates:
            raise ExamException(f'Year not Found: {year}')
    result = []
    pass1 = [None]*12
    pass2 = [None]*12
    for i in range(1, 13):
        month1 = str(years[0])+'-'+str(i).zfill(2)
        month2 = str(years[1])+'-'+str(i).zfill(2)
        for item in time_series:
            if item[0] == month1:
                pass1[i-1] = item[1]
            if item[0] == month2:
                pass2[i-1] = item[1]
    for i in range(0, 11):
        pass1[i] = abs(pass1[i]-pass1[i+1]) if pass1[i] is not None and pass1[i + 1] is not None else None
        pass2[i] = abs(pass2[i]-pass2[i+1]) if pass2[i] is not None and pass2[i + 1] is not None else None
    pass1.pop()
    pass2.pop()
    for i in range(0, 11):
        result[i] = abs(pass1[i]-pass2[i]) <= 2 if pass1[i] is not None and pass2[i] is not None else False

    print(result)
    return result
