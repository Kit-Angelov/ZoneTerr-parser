import csv
import os


class CadastralDistrict:
    def __init__(self, source_path=''):
        self.path = source_path
        self.cache = {}

    def get_code(self, region, districtName):
        region = str(region)
        data = ''
        if region not in self.cache:
            with open(os.path.join(self.path, (region + '.csv')), 'r') as file:
                r = {}
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    r[row[0]] = row[1]
                self.cache[region] = r
        if region in self.cache:
            return self.cache[region].get(districtName, '-sorry-')
        return '-sorry-'




