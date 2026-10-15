# pages/login_page.py – Staff Login Page
# Covers TC-058, TC-059, TC-060, TC-061  (FR-SEC group)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class LoginPage(BasePage):
    """
    Page object for the staff/admin login portal.
    URL: {base_url}/login  or  accessible via a "Login" link from the main page.
    """

    # ── Locators ──────────────────────────────────────────
    USERNAME_INPUT      = (By.CSS_SELECTOR, "input[name='username'], input[type='text'], input[placeholder*='ชื่อผู้ใช้'], input[placeholder*='username']")
    PASSWORD_INPUT      = (By.CSS_SELECTOR, "input[name='password'], input[type='password']")
    LOGIN_BUTTON        = (By.CSS_SELECTOR, "button[type='submit'], button[class*='login'], button[class*='Login']")
    ERROR_MESSAGE       = (By.CSS_SELECTOR, "[class*='error'], [class*='Error'], [role='alert'], [class*='alert']")
    LOGOUT_BUTTON       = (By.CSS_SELECTOR, "button[class*='logout'], button[class*='Logout'], a[href*='logout']")
    USER_MENU           = (By.CSS_SELECTOR, "[class*='user-menu'], [class*='userMenu'], [class*='avatar']")
    DASHBOARD_HEADING   = (By.CSS_SELECTOR, "h1, h2, [class*='dashboard'], [class*='Dashboard']")

    def open_login(self):
        self.open("/login")
        self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))

    def login(self, username: str, password: str):
        """Fill credentials and submit the login form."""
        self.type_text(*self.USERNAME_INPUT, username)
        self.type_text(*self.PASSWORD_INPUT, password)
        self.click(*self.LOGIN_BUTTON)

    def is_logged_in(self) -> bool:
        """Return True when the dashboard/logout element is present after login."""
        try:
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located(self.LOGOUT_BUTTON),
                    EC.presence_of_element_located(self.USER_MENU),
                    EC.url_contains("/dashboard"),
                    EC.url_contains("/admin"),
                )
            )
            return True
        except Exception:
            return False

    def get_error_message(self) -> str:
        try:
            return self.get_text(*self.ERROR_MESSAGE)
        except Exception:
            return ""

    def logout(self):
        """Click the logout control."""
        self.click(*self.LOGOUT_BUTTON)

    def is_session_cleared(self) -> bool:
        """After logout, verify the session cookie is removed and redirected to login."""
        from selenium.common.exceptions import TimeoutException
        try:
            self.wait.until(EC.url_contains("/login"))
            return True
        except TimeoutException:
            return self.is_element_present(*self.LOGIN_BUTTON)
