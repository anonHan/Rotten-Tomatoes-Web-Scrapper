from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TomatoScrapper:
    def __init__(self, executable_path, chrome_options):
        """ This function initializes the Chrome Driver"""
        try:
            self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
            self.driver.maximize_window()
        except Exception as e:
            raise Exception(f"Failed to initialize the Chrome Driver ", +str(e))


    def get_movie_name(self):
        """Will add this feature in some time, where a user can also search by the name of the movie."""
        movie_name = input("Enter the Name of the Movie (should be available on www.rottentomatoes.com):")
        return movie_name

    def linkOpener(self, url):
        """This function opens the provided URL"""
        try:
            result = self.driver.get(url)
            return result
        except Exception as e:
            raise Exception(f"Failed to open the provided URL ", +str(e))

    def expand_shadow_element(self, element):
        try:
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            return shadow_root
        except Exception as e:
            raise Exception(f"Failed to open the Shadow Root ", +str(e))

    def get_audience_review_page_link(self):
        """This function get the link for Audience reviews page and takes to the next page."""
        try:
            audience_review_page_link = self.driver.find_element(By.XPATH, '//section[@id="audience_reviews"]/div/a')
            audience_review_page_link.click()
        except Exception as e:
            raise Exception(f"Audience Page Link not found." + str(e))

    def get_textual_and_star_reviews(self):
        """This function is the core of this scrapper it gives us the all the textual ratings along with their star ratings. """
        try:
            star_r = []
            textual_reviews = []
            try:
                audience_reviews = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="audience-reviews"]/li')))
            # audience_reviews = self.driver.find_elements_by_xpath('//ul[@class="audience-reviews"]/li')
            except Exception as e:
                raise Exception(f"Oops! No reviews for this movie ", +str(e))
            for review in audience_reviews:
                try:
                    filled_stars = 0
                    half_stars = 0
                    review_wrap = review.find_elements(By.XPATH, './div[2]/span/span/span')
                    for star_rating in review_wrap:
                        if star_rating.get_attribute('class') == 'star-display__filled ':
                            filled_stars += 1
                        elif star_rating.get_attribute('class') == 'star-display__half ':
                            half_stars += .5
                    star_r.append(filled_stars + half_stars)
                    text_of_review = review.find_element(By.XPATH, './div[2]/p').text
                    textual_reviews.append(text_of_review)
                except Exception as e:
                    raise Exception(f"Something went wrong while getting stars Xpath ", +str(e))
            return star_r, textual_reviews
        except Exception as e:
            raise Exception(f"Something went wrong while getting the list of all reviews on a page ", +str(e))

    def pagination(self):
        try:
            next_page_link = self.driver.find_element(By.XPATH,
                                                      '//nav[@class="prev-next-paging__wrapper"][2]/button[2]')
            return next_page_link
        except Exception as e:
            raise Exception(f"Failed to get the next page link ", +str(e))

    def quit_driver(self):
        self.driver.quit()
