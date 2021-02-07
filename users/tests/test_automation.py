from urllib.parse import urljoin
from django.shortcuts import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from .test_data import create_user_jake


class AutomationTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self) -> None:
        create_user_jake()


class UserAccountTest(AutomationTest):
    def tearDown(self) -> None:
        try:
            self.selenium.find_element_by_css_selector('.item.logout').click()
        except NoSuchElementException:
            pass

    def test_login_with_username(self):
        self.log_in('baracuda')

    def test_login_with_email(self):
        self.log_in('jake.peralta@b99.com')

    def test_register(self):
        url = urljoin(self.live_server_url, reverse('register'))
        self.selenium.get(url)
        username_input = self.selenium.find_element_by_name("email")
        username_input.send_keys('capitain.raymond.holt@b99.com')
        password_input = self.selenium.find_element_by_name("username")
        password_input.send_keys('Capitain')
        password_input = self.selenium.find_element_by_name("password1")
        password_input.send_keys('whatisGod99')
        password_input = self.selenium.find_element_by_name("password2")
        password_input.send_keys('whatisGod99')
        self.selenium.find_element_by_id("submit").click()
        expected_url = urljoin(self.live_server_url, reverse('login'))
        self.assertEqual(expected_url, self.selenium.current_url)

    def log_in(self, value):
        url = urljoin(self.live_server_url, reverse('login'))
        self.selenium.get(url)
        self.assertNotIn('logout', self.selenium.find_element_by_tag_name('nav').text)
        self.assertNotIn('Profile', self.selenium.find_element_by_tag_name('nav').text)
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(value)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('rosa1234')
        self.selenium.find_element_by_id("submit").click()
        expected_url = urljoin(self.live_server_url, reverse('home'))
        self.assertEqual(expected_url, self.selenium.current_url)
        self.assertIn('logout', self.selenium.find_element_by_tag_name('nav').text)
        self.assertIn('Profile', self.selenium.find_element_by_tag_name('nav').text)
        self.assertNotIn('login', self.selenium.find_element_by_tag_name('nav').text)
