import pandas as pd
import time
import os
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By

class WebScraping:

    def __init__(self,link):

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager("114.0.5735.90").install()))
        self.driver.get(link)

    def releasedriver(self):

        self.driver.quit()
   
    def get_links(self,value2,value3):

        try:
            search = self.driver.find_elements(By.CLASS_NAME,value=value2)
            return [ele.text for data in search for ele in data.find_elements(By.TAG_NAME,value3) if len(ele.text) > 0]
        except:
            self.releasedriver()

    def get_hyper_links(self,value2,value3,refrence):

        try:
            link_names = self.get_links(value2,value3)
            return [link_data.get_attribute(refrence) for text in link_names for link_data in 
                                                   self.driver.find_elements(By.LINK_TEXT, text)]
        except:
            self.releasedriver()

class GetDataFrame(WebScraping):

    def __init__(self,link,val2,val3,ref):

        super().__init__(link)
        self.link_data = self.get_hyper_links(val2,val3,ref)

    def getdataframe(self):

        try:
            return pd.DataFrame(self.link_data,index=range(len(self.link_data)),columns=['Links'])
        except Exception as e:
            return e

    def createfile(self,filename):

        try:
            df = self.getdataframe()
            if os.path.isfile(filename):

                df.to_csv(filename,mode='a',index=False,header=False)
                print('append successful')
                
            else:
                df.to_csv(filename,index=False)
        except Exception as e:
            return e
        
class ReadData:

    def __init__(self,file):

        self.df = pd.read_csv(file,encoding='utf-8')
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates()

    def get_data(self,feature_name,str_lst,endswith_condition):

        try:
            filtered_df = self.df[self.df[feature_name].str.contains("|".join(str_lst))]
            if endswith_condition is True:
                return filtered_df[filtered_df[feature_name].str.endswith('.html')]
            else:
                return filtered_df
        except Exception as e:
            return e

    def readdata(self,feature_name,str_lst,condition):

        try:
            filtered_df = self.get_data(feature_name,str_lst,condition)
            return filtered_df[feature_name].to_list()
        except Exception as e:
            return e
        
class ExtractText:

    def __init__(self,link):

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager("114.0.5735.90").install()))
        self.driver.get(link)

    def releasedriver(self):

        self.driver.quit()

    def news_title(self,title_val,tag_value):

        try:
            news_title = self.driver.find_elements(By.CLASS_NAME,value=title_val)
            return [news_.text for data in news_title for news_ in data.find_elements(By.TAG_NAME,tag_value)]
        except:
            self.releasedriver()

    def get_text(self,value,value2,value3,value4):

        try:
            search = self.driver.find_elements(By.CLASS_NAME,value=value)
            return [ele.text for data in search for ele in data.find_elements(By.CLASS_NAME,value4) if len(ele.text) > 0], [datetext.text for data in search for data_ in 
                    data.find_elements(By.CLASS_NAME,value=value2) 
                    for datetext in data_.find_elements(By.TAG_NAME , value=value3)] 
        except:
            self.driver.quit()
            
class GetLinks:

    def __init__(self,csv_file_name):

        self.r = ReadData(file=csv_file_name)
        
    def get_links(self,featurename,str_lst,endcondition):
        try:
            self.data = self.r.readdata(featurename,str_lst,endcondition)
            return self.data
        except Exception as e:
            return e

class CreateTextFiles:

    def __init__(self,file_name,feature,val_lst,end_con):

        self.gl = GetLinks(csv_file_name=file_name)
        self.data = self.gl.get_links(featurename=feature,str_lst=val_lst,endcondition=end_con)

    def check_data_links(self):
        return self.data

    def get_files(self,path,start,end,title_val,tag_val,val4,val,val2,val3):
        
        try:
            if end=='all':
                end = len(self.data)
            else:
                end = end
            for i in range(start,end+1):

                if os.path.isfile(path+'/'+str(i)+'news.txt'):
                    print('file already exists')
                else:
                    ex = ExtractText(link=self.data[i])
                    title_list = ex.news_title(title_val,tag_val)
                    date,text=ex.get_text(value4=val4,value=val,value2=val2,value3=val3)
                    with open(path+'/'+str(i)+'news.txt','w',encoding='unicode_escape') as f:
                        for title in title_list:
                            f.writelines(f'{title}\t')
                        for content in date:
                            f.writelines(f'{content}\t')
                        for data in text:
                            f.writelines(f'{data}')
                    f.close()
                  
                    ex.releasedriver()
                    time.sleep(0.1)
        except Exception as e:
            return e
        
if __name__ == '__main__':
    
    link_number = int(input('Enter link to scrape : '))
    if link_number == 1:

        x="https://www.moneycontrol.com/news/business/stocks/"

        data_frame=GetDataFrame(link=x,val2='fleft',val3='a',ref='href')
   
        data_frame.createfile(filename='E:/MoneyControl Data Scraping/8_Aug_2023_links_scraped.csv')
        data_frame.releasedriver()

        print('Scraping text')

        time.sleep(0.5)
    
        files = CreateTextFiles(file_name='E:/MoneyControl Data Scraping/8_Aug_2023_links_scraped.csv',feature='Links',val_lst=['/news/business/stock/','/news/business/'],end_con=True)
        files.get_files(path='E:/MoneyControl Data Scraping/8_Aug_news/',start=0,end=5,title_val='page_wrapper',tag_val='h1',val4='article_schedule',val='clearfix',val2='content_wrapper',val3='p',)
    
    elif link_number == 2:

        x="https://www.businesstoday.in/markets/company-stock/"

        data_frame=GetDataFrame(link=x,val2='content-area',val3='a',ref='href')
   
        data_frame.createfile(filename='E:/MoneyControl Data Scraping/new_links.csv')
        data_frame.releasedriver()

        print('Scraping text')

        time.sleep(0.5)
    
        files = CreateTextFiles(file_name='E:/MoneyControl Data Scraping/new_links.csv',feature='Links',val_lst=['/markets/company-stock/story/'],end_con=False)
        files.get_files(path='E:/MoneyControl Data Scraping/new/',start=0,end='all',title_val='story-heading',tag_val='h1',val4='brand-detial-main',val='content-area',val2='text-formatted',val3='p')


    