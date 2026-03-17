import csv
import os


class CSVWriter:
    def __init__(self, filename):
        """
        Initialize the CSVWriter with a filename.
        :param filename: Name of the CSV file to write to.
        """
        self.filename = filename
        self._headers_written = False

    def write_header(self, headers):
        """
        Write the header row to the CSV file.
        :param headers: List of header names.
        """
        try:
            file_exists = os.path.isfile(self.filename)
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                # Only write headers if file is new and headers haven't been written
                if not file_exists and not self._headers_written:
                    writer.writerow(headers)
                    self._headers_written = True
        except IOError as e:
            print(f"Error writing headers to {self.filename}: {e}")

    def write_row(self, row):
        """
        Write a single row of data to the CSV file.
        :param row: List of values representing a row of data.
        """
        try:
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row)
        except IOError as e:
            print(f"Error writing row to {self.filename}: {e}")

    def write_rows(self, rows):
        """
        Write multiple rows of data to the CSV file.
        :param rows: List of lists, where each inner list represents a row of data.
        """
        try:
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
        except IOError as e:
            print(f"Error writing rows to {self.filename}: {e}")

# TODO: Add support for handling different delimiters
# TODO: Implement a method to clear the CSV file if needed before writing new data
# TODO: Add more robust error handling and logging
# TODO: Maybe consider using context managers for file operations to ensure files close properly
# This is a simple CSV writer utility, so it's lightweight and straightforward, but a few enhancements could make it more robust!
