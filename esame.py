class ExamException(Exception):
    """
    Custom Exception class.
    """
    pass


class CSVTimeSeriesFile:
    """
    Class to read and get data from a file.
    The file name is passed in the constructor.
    """

    def __init__(self, name: str):
        """
        Initialize the class with a file name.
        It must be a string otherwise the constructor will raise an exception;
        :param name: a string containing a file name (*.csv)
        """
        if not isinstance(name, str):
            raise ExamException('File Name Error')
        self.name = name

    def get_data(self) -> list[list[str, int | None]]:
        """
        Method to extract the data from the file;
        :return: a list of lists which represents the dataset
        """
        data = []
        # Try to open the file
        try:
            file = open(self.name)
        except IOError:
            raise ExamException('Could not open/read file')
        # Extract the data
        for row in file:
            # To ignore the empty rows
            if len(row) > 1:
                row_data = row.split(',')
                # To skip the header
                if row_data[0] != 'date':
                    # Try to convert a string to an integer
                    try:
                        # Create a set to check if a row is duplicated
                        dates = {item[0] for item in data}
                        # Check if a row is a duplicate
                        if row_data[0] in dates:
                            file.close()
                            raise ExamException('Duplicate Error')
                        # Check if the dataset is in order and have the same date format otherwise raise an exception
                        if len(data) > 0 and row_data[0] < data[-1][0]:
                            file.close()
                            raise ExamException('Timestamp Error')
                        # Convert the string number of passengers to an integer
                        number = int(row_data[1])
                        # Append only if is a positive number
                        data.append([row_data[0], number if number >= 0 else None])
                    except ValueError:
                        # If the conversion failed just assign the None value and go to the next interation
                        data.append([row_data[0], None])
                        continue
        file.close()
        return data


def detect_similar_monthly_variations(time_series: list[list[str, int | None]], years: list[int | str]) -> list[bool]:
    """
    Function to elaborate the dataset.
    It requires a list of data and a list of two consecutive years;
    :param time_series: a list of data to elaborate
    :param years: a list of two consecutive years
    :return: a list of booleans (True or False)
    """
    # Check if years is a list
    if not isinstance(years, list):
        raise ExamException('Years is not a list')
    # Check if years have exactly two elements
    if len(years) != 2:
        raise ExamException(f'length of years list: {len(years)}')
    # Check every element of years is an int or a string
    for year in years:
        if not isinstance(year, (int, str)):
            raise ExamException('Years type Error')
    try:
        # Check if they are negative years
        if int(years[0]) < 0 or int(years[1]) < 0:
            raise ExamException('Negative Year')
        # Check if they are two consecutive years
        if abs(int(years[0])-int(years[1])) != 1:
            raise ExamException(f'{years[0]} and {years[1]} are not consecutive')
    except ValueError:
        raise ExamException('Years format Error')
    if not isinstance(time_series, list):
        raise ExamException('Time series format error')
    for item in time_series:
        if len(item) != 2 or not isinstance(item[0], str) or len(item[0]) != 7:
            raise ExamException('Time series date format error')
        if not isinstance(item[1], (int, type(None))):
            raise ExamException('Time series passengers type error')
    # Create a set to check if the chosen years are inside my list of data
    dates = {item[0][0:4] for item in time_series}
    # Check if both the years are present in my data
    for year in years:
        if not str(year) in dates:
            raise ExamException(f'Year not Found: {year}')
    # Initialize the result list with 11 cells with the value False
    result = [False]*11
    # Initialize the list of passengers for the first year
    pass1 = [None]*12
    # Initialize the list of passengers for the second year
    pass2 = [None]*12
    # For every month
    for i in range(1, 13):
        # Create a string with the interested month
        month = str(i).zfill(2)
        # For every list inside my list of lists I exact the number of passengers per month
        for item in time_series:
            if item[0][0:4] == str(years[0]) and item[0][5:7] == month:
                pass1[i-1] = item[1]
            if item[0][0:4] == str(years[1]) and item[0][5:7] == month:
                pass2[i-1] = item[1]
    # Calculate the difference between two consecutive month
    # Only if both month have a not None value of passengers
    for i in range(0, 11):
        pass1[i] = abs(pass1[i]-pass1[i+1]) if pass1[i] is not None and pass1[i + 1] is not None else None
        pass2[i] = abs(pass2[i]-pass2[i+1]) if pass2[i] is not None and pass2[i + 1] is not None else None
    # Delete the last cell
    pass1.pop()
    pass2.pop()
    # For every month in the two chosen years check if they have a similar value
    for i in range(0, 11):
        result[i] = abs(pass1[i]-pass2[i]) <= 2 if pass1[i] is not None and pass2[i] is not None else False
    # result is a list of Boolean (True or False) with a length of 11
    return result
