from selenium.webdriver.firefox.webdriver import WebDriver

from django.test import LiveServerTestCase

class TitleTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10) # will wait up to 10 seconds for something to happen - code quite possibly running ahead of what browser is doing


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_title_on_homepage(self):
        self.selenium.get(self.live_server_url)
        self.assertIn('Travel Wishlist', self.selenium.title) # think of selenium as the browser in these tests

# to run test: cd to wishlist directory, then 'python manage.py test travel_wishlist.functional_tests'

class AddPlacesTest(LiveServerTestCase):

    fixtures = ['test_places']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10) # will wait up to 10 seconds for something to happen - code quite possibly running ahead of what browser is doing


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_add_new_place(self):

        self.selenium.get(self.live_server_url)
        input_name = self.selenium.find_element_by_id('id_name')
        input_name.send_keys('Denver')

        add_button = self.selenium.find_element_by_id('add-new-place')
        add_button.click()
        # immitates expected browser behavior
        denver = self.selenium.find_element_by_id('place-name-5')
        self.assertEqual('Denver', denver.text)

        self.assertIn('Denver', self.selenium.page_source)
        self.assertIn('New York', self.selenium.page_source)
        self.assertIn('Tokyo', self.selenium.page_source)