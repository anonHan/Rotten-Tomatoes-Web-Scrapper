import pandas as pd
from TomatoScrapper import TomatoScrapper
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time

# setting up log file
logging.basicConfig(filename='RottenTomatoes.log',
                    level=logging.INFO, format='%(asctime)s %(message)s')

class StartScrapper:
    def start_scrapping(website_url):
        all_star_rating = []
        all_textual_reviews = []
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.add_argument(
            "User-Agent-Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
       #  path = 'C:/Users/Sahil/Download'
        tomatoScrapper = TomatoScrapper(executable_path=ChromeDriverManager().install(),
                                        chrome_options=chrome_opts)

        #website_url = 'https://www.rottentomatoes.com/m/black_widow_2021'
        tomatoScrapper.linkOpener(website_url)
        logging.info("Website opened.")

        tomatoScrapper.get_audience_review_page_link()
        logging.info("On the Audience Page")

        score, text = tomatoScrapper.get_textual_and_star_reviews()
        df = pd.DataFrame({'rating': score, 'textual_review': text})

        next_page_url = tomatoScrapper.pagination()
        while next_page_url is not None:
            try:
                next_page_url.click()
                logging.info("\n\nGot the Next page link. On Next page of Reviews.")
                time.sleep(2)
                score, text = tomatoScrapper.get_textual_and_star_reviews()
                df2 = pd.DataFrame({'rating': score, 'Review': text})
                df = df.append(df2, ignore_index=True)
                logging.info("DataFrame Appended.")
                next_page_url = tomatoScrapper.pagination()
            except:
                print('Scrapped all the pages!')
                next_page_url = None
                df.to_csv('RottenTomatoes.csv')
                tomatoScrapper.quit_driver()  # shut down the driver after successful scrapping.
                logging.info("Scrapped reviews successfully and saved the reviews in csv file.")

