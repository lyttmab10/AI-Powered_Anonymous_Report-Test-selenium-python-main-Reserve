# pages/report_page.py – Anonymous Report Submission Page
# Covers TC-001 to TC-017  (FR-SUB group)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from .base_page import BasePage


class ReportPage(BasePage):
    """
    Page object for the public anonymous report submission form.
    URL: {base_url}/  (home / submission tab)
    """

    # ── Locators ──────────────────────────────────────────
    # Step indicators
    STEP_INDICATORS     = (By.CSS_SELECTOR, "[class*='step'], [data-step], .step-item")
    STEP_NUMBERS        = (By.CSS_SELECTOR, "[class*='step-number'], [class*='stepNumber']")

    # Step 1 – Event details
    INCIDENT_DATE_INPUT = (By.CSS_SELECTOR, "input[type='date'], input[name*='date'], input[name*='Date']")
    LOCATION_INPUT      = (By.CSS_SELECTOR, "input[name*='location'], input[name*='place'], input[placeholder*='สถานที่']")
    DESCRIPTION_TEXTAREA= (By.CSS_SELECTOR, "textarea[name*='description'], textarea[name*='detail'], textarea[placeholder*='รายละเอียด']")
    CHAR_COUNTER        = (By.CSS_SELECTOR, "[class*='counter'], [class*='char-count'], [data-counter]")
    NEXT_BUTTON         = (By.CSS_SELECTOR, "button[type='button']:not([disabled]), button:contains('ถัดไป')")
    SUBMIT_BUTTON       = (By.CSS_SELECTOR, "button[type='submit'], button[class*='submit']")
    CONFIRM_SUBMIT_BTN  = (By.XPATH, "//button[contains(text(),'ยืนยัน') or contains(text(),'ส่ง')]")

    # Step 2 – File upload
    FILE_INPUT          = (By.CSS_SELECTOR, "input[type='file']")
    UPLOAD_AREA         = (By.CSS_SELECTOR, "[class*='upload'], [class*='dropzone'], [data-upload]")
    FILE_LIST           = (By.CSS_SELECTOR, "[class*='file-list'], [class*='fileList'], [class*='attachment']")
    FILE_ITEM           = (By.CSS_SELECTOR, "[class*='file-item'], [class*='fileItem']")

    # Step 3 – Category
    CATEGORY_OPTIONS    = (By.CSS_SELECTOR, "[class*='category'], [name*='category'], [data-category]")

    # Step 4 – Urgency
    URGENCY_OPTIONS     = (By.CSS_SELECTOR, "[class*='urgency'], [class*='priority'], [name*='urgency']")

    # Success / error
    REPORT_ID_DISPLAY   = (By.CSS_SELECTOR, "[class*='report-id'], [class*='reportId'], [data-report-id]")
    PIN_DISPLAY         = (By.CSS_SELECTOR, "[class*='pin'], [data-pin]")
    SUCCESS_MESSAGE     = (By.CSS_SELECTOR, "[class*='success'], [class*='Success']")
    ERROR_MESSAGE       = (By.CSS_SELECTOR, "[class*='error'], [class*='Error'], [role='alert']")
    VALIDATION_MSG      = (By.CSS_SELECTOR, "[class*='validation'], [class*='invalid'], :invalid")

    def open_report_page(self):
        self.open("/")
        # Wait for page to be interactive
        self.wait.until(EC.presence_of_element_located(self.DESCRIPTION_TEXTAREA))

    def get_step_count(self) -> int:
        """Return the number of visible step indicators."""
        steps = self.find_all(*self.STEP_INDICATORS)
        return len(steps)

    def get_incident_date_value(self) -> str:
        """Return current value of the incident date field."""
        el = self.wait_visible(*self.INCIDENT_DATE_INPUT)
        return el.get_attribute("value") or ""

    def set_incident_date(self, date_str: str):
        """Set incident date (format: YYYY-MM-DD)."""
        self.type_text(*self.INCIDENT_DATE_INPUT, date_str)

    def set_location(self, location: str):
        """Type location text."""
        self.type_text(*self.LOCATION_INPUT, location)

    def set_description(self, text: str):
        """Type description text."""
        self.type_text(*self.DESCRIPTION_TEXTAREA, text)

    def get_char_counter_text(self) -> str:
        """Return the character counter label text (e.g. '150 / 5000')."""
        return self.get_text(*self.CHAR_COUNTER)

    def upload_file(self, file_path: str):
        """Upload a file via the hidden file input."""
        el = self.wait_for_element(*self.FILE_INPUT)
        el.send_keys(file_path)

    def get_file_count(self) -> int:
        """Return number of files shown in the attachment list."""
        items = self.find_all(*self.FILE_ITEM)
        return len(items)

    def click_confirm_submit(self):
        """Click the final submit button."""
        self.click(*self.CONFIRM_SUBMIT_BTN)

    def is_success(self) -> bool:
        """Check if success message / report ID is shown."""
        return self.is_element_present(*self.SUCCESS_MESSAGE) or \
               self.is_element_present(*self.REPORT_ID_DISPLAY)

    def get_report_id(self) -> str:
        """Return the report ID from the success screen."""
        return self.get_text(*self.REPORT_ID_DISPLAY)

    def get_pin(self) -> str:
        """Return the PIN from the success screen."""
        return self.get_text(*self.PIN_DISPLAY)

    def get_error_message(self) -> str:
        """Return the latest error/validation message text."""
        try:
            return self.get_text(*self.ERROR_MESSAGE)
        except Exception:
            return ""

    def is_form_invalid(self) -> bool:
        """Return True if any required-field validation error is visible."""
        return self.is_element_present(*self.ERROR_MESSAGE) or \
               self.is_element_present(*self.VALIDATION_MSG)
