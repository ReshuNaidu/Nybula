import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(params=["chrome", "firefox"], scope="class")
def driver_init(request):
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
    if request.param == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Firefox(options=options)
    request.cls.driver = driver
    yield
    driver.close()


@pytest.mark.usefixtures("driver_init")
class BaseTest:
    pass


class TestNBLWebsite(BaseTest):

    def test_verify_homepage_title(self):
        self.driver.get("https://nbl.one")
        assert self.driver.title == "Noble | Vacation rental management & homeownership for the 21st century"

    def test_book_skylift(self):
        self.driver.get("https://nby.la/rdJuXp")
        self.driver.find_element(By.XPATH, "//span[contains(text(),'Book Now')]").click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Book this property')]")))
        self.driver.find_element(By.XPATH, "//div[contains(text(),'Book this property')]").click()
        wait.until(EC.element_to_be_clickable((By.ID, "form")))

        self.driver.find_element(By.NAME, "first_name").send_keys("Test")
        self.driver.find_element(By.NAME, "last_name").send_keys("User")
        self.driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
        self.driver.find_element(By.NAME, "phone").send_keys("1234567890")
        self.driver.find_element(By.ID, "accept").click()

        self.driver.find_element(By.XPATH, "//span[contains(text(),'Pay with Card')]").click()
        wait.until(EC.element_to_be_clickable((By.NAME, "cardnumber")))
        self.driver.find_element(By.NAME, "cardnumber").send_keys("4242424242424242")
        self.driver.find_element(By.NAME, "exp-date").send_keys("1222")
        self.driver.find_element(By.NAME, "cvc").send_keys("123")
        self.driver.find_element(By.NAME, "postal").send_keys("12345")
        self.driver.find_element(By.XPATH, "//span[contains(text(),'Pay $5,000.00')]").click()

        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Booking Confirmed!')]")))
        assert self.driver.find_element(By.XPATH, "//div[contains(text(),'Booking Confirmed!')]").is_displayed()

