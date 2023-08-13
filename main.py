import time
import stock_news as sn
import news_text_scraping as nts


class ScrapeNews:

    def __init__(self,link,filename,path,file_to_save):
        
        self.links = link
        self.filename = filename
        self.path = path
        self.file_to_save = file_to_save
        
    def scrapelinks(self,v2,v3,ref):

        news_link = nts.GetDataFrame(link=self.links,val2=v2,val3=v3,ref=ref)
        news_link.createfile(filename=self.filename)
        news_link.releasedriver()

    def generatefiles(self,feature_name,valst,start,end,val,val2,val3,val4,titleval,tagval,endcon):

        files = nts.CreateTextFiles(file_name=self.filename,feature=feature_name,val_lst=valst,end_con=endcon)
        files.get_files(path=self.path,start=start,end=end,val=val,val2=val2,val3=val3,val4=val4,title_val=titleval,tag_val=tagval)

    def createcsvfile(self):

        csv_file = sn.CreateDataFile(data_directory=self.path)
        csv_file.extract_news(file=self.file_to_save)

if __name__ == '__main__':

    def main():

        scr_news = ScrapeNews(link="https://www.moneycontrol.com/news/business/stocks/",
                              filename='8_Aug_2023_links_scraped.csv',path='D:/Selenium/8_Aug_2023/',
                              file_to_save='news.csv')
        
        scr_news.scrapelinks(v2='fleft',v3='a',ref='href')

        scr_news.generatefiles(feature_name='Links',valst=['/news/business/stock','/news/business'],endcon=True,start=6,end=10,titleval='page_left_wrapper',tagval='h1',
                               val4='article_schedule',val='clearfix',val2='content_wrapper',val3='p')
        scr_news.createcsvfile()

        time.sleep(0.5)

    def driver_func():

        condition = input('do you want to scrape : ')

        if condition == 'yes':
            main()
        else:
            print('exit')

        if condition == 'yes':
            driver_func()

    driver_func()

        





    


