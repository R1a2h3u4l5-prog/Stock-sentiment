import os
import csv
import pandas as pd

class ReadDirectory:

    def __init__(self,data_dir):

        self.loc = data_dir
        self.file_data = list()

    def read_file(self):

        try:
            for file in os.listdir(self.loc):
                with open(self.loc+'/'+file,'r') as f:
                    for text in f.readlines():
                        self.file_data.append(text)
                f.close()

            return self.file_data
            
        except Exception as e:
            return e
    
    def get_strings(self):

        try:
            return [list(set(data.split('\\t'))) for data in self.read_file()]
        except Exception as e:
            return e
    def removempty(self):

        try:
            return [sorted(data,key=len) for data in self.get_strings() if '' not in data]
        except Exception as e:
            return e

class CreateDataFile:

    def __init__(self,data_directory):

        self.rd = ReadDirectory(data_dir=data_directory)
        self.strings = self.rd.removempty()
        self.file_rows = list()

    def extract_news(self,file):

        try:
            if os.path.isfile(file):

                with open(file,'r') as f:

                    csv_reader = csv.reader(f)
                    for row in csv_reader:
                        self.file_rows.append(row) 

                with open(file,'a',newline='') as f:

                    csv_append = csv.writer(f)

                    for data in self.strings:
                        if data not in self.file_rows:
                            csv_append.writerow(data)    
                    
                    print('append successfull')
                f.close()   
                
            else:

                with open(file,'w',newline='') as f:

                    csv_writer = csv.writer(f)
                    fields = ['Date and Time','Title','News']

                    csv_writer.writerow(fields)
                    for row in self.strings:
                        csv_writer.writerow(row)
                f.close()
        except Exception as e:
            return e
        


if __name__ == '__main__':

    cd = CreateDataFile(data_directory='E:/MoneyControl Data Scraping/2_Aug_news/')
    cd.extract_news(file='news.csv')
    
   
    
    
         


