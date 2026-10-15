# pages/base_page.py – Base Page Object
# Shared helpers for all page objects

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """Base class that every page object inherits from."""

    def __init__(self, driver, base_url: str, timeout: int = 15):
        self.driver   = driver
        self.base_url = base_url.rstrip("/")
        self.wait     = WebDriverWait(driver, timeout)
        self.timeout  = timeout

    # ── navigation ────────────────────────────────────────
    def open(self, path: str = ""):
        self.driver.get(f"{self.base_url}/{path.lstrip('/')}")

    # ── wait helpers ──────────────────────────────────────
    def wait_for_element(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def wait_visible(self, by, locator):
        return self.wait.until(EC.visibility_of_element_located((by, locator)))

    def wait_clickable(self, by, locator):
        return self.wait.until(EC.element_to_be_clickable((by, locator)))

    def wait_text_in(self, by, locator, text):
        return self.wait.until(EC.text_to_be_present_in_element((by, locator), text))

    def is_element_present(self, by, locator) -> bool:
        try:
            self.wait_for_element(by, locator)
            return True
        except Exception:
            return False

    def find(self, by, locator):
        return self.driver.find_element(by, locator)

    def find_all(self, by, locator):
        return self.driver.find_elements(by, locator)

    def get_text(self, by, locator) -> str:
        return self.wait_visible(by, locator).text.strip()

    def click(self, by, locator):
        self.wait_clickable(by, locator).click()

    def type_text(self, by, locator, text: str, clear: bool = True):
        el = self.wait_visible(by, locator)
        if clear:
            el.clear()
        el.send_keys(text)

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def title(self) -> str:
        return self.driver.title
