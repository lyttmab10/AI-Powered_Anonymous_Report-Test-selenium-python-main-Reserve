# pages/tracking_page.py – Report Tracking & 2-Way Chat Page
# Covers TC-031 to TC-038  (FR-TRK group)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class TrackingPage(BasePage):
    """
    Page object for the anonymous report status tracking page.
    Reporters enter their Report ID + PIN to check status and chat.
    URL: {base_url}/track  (or via a "ติดตามสถานะ" / "Track" tab)
    """

    # ── Locators ──────────────────────────────────────────
    TRACK_TAB           = (By.XPATH, "//button[contains(text(),'ติดตาม') or contains(text(),'Track') or contains(text(),'สถานะ')]")
    REPORT_ID_INPUT     = (By.CSS_SELECTOR, "input[name*='reportId'], input[name*='report_id'], input[placeholder*='รหัส']")
    PIN_INPUT           = (By.CSS_SELECTOR, "input[name*='pin'], input[type='password'], input[placeholder*='PIN']")
    TRACK_SUBMIT        = (By.CSS_SELECTOR, "button[type='submit'], button[class*='track'], button[class*='search']")

    # Status display
    STATUS_BADGE        = (By.CSS_SELECTOR, "[class*='status'], [class*='badge'], [data-status]")
    CASE_DETAILS        = (By.CSS_SELECTOR, "[class*='case-detail'], [class*='caseDetail'], [class*='report-detail']")
    REPORT_ID_DISPLAY   = (By.CSS_SELECTOR, "[class*='report-id'], [data-testid='report-id']")

    # 2-way chat
    CHAT_INPUT          = (By.CSS_SELECTOR, "input[name*='message'], textarea[name*='message'], [placeholder*='ข้อความ']")
    CHAT_SEND_BTN       = (By.CSS_SELECTOR, "button[class*='send'], button[type='submit'][class*='chat']")
    CHAT_MESSAGES       = (By.CSS_SELECTOR, "[class*='message'], [class*='chat-bubble']")
    TYPING_INDICATOR    = (By.CSS_SELECTOR, "[class*='typing'], [class*='Typing']")

    # Evidence upload on tracking page
    EVIDENCE_FILE_INPUT = (By.CSS_SELECTOR, "input[type='file']")
    EVIDENCE_UPLOAD_BTN = (By.CSS_SELECTOR, "button[class*='upload'], button[class*='attach']")

    # Error
    ERROR_MESSAGE       = (By.CSS_SELECTOR, "[class*='error'], [role='alert']")

    def open_tracking_tab(self):
        """Navigate to the tracking tab from the homepage."""
        self.open("/")
        self.wait.until(EC.element_to_be_clickable(self.TRACK_TAB))
        self.click(*self.TRACK_TAB)
        self.wait.until(EC.presence_of_element_located(self.REPORT_ID_INPUT))

    def enter_credentials(self, report_id: str, pin: str):
        self.type_text(*self.REPORT_ID_INPUT, report_id)
        self.type_text(*self.PIN_INPUT, pin)

    def submit_track(self):
        self.click(*self.TRACK_SUBMIT)

    def track_report(self, report_id: str, pin: str):
        self.enter_credentials(report_id, pin)
        self.submit_track()

    def get_status(self) -> str:
        """Return the current status text (e.g. 'กำลังดำเนินการ', 'ปิดคดี')."""
        return self.get_text(*self.STATUS_BADGE)

    def send_chat_message(self, text: str):
        self.type_text(*self.CHAT_INPUT, text)
        self.click(*self.CHAT_SEND_BTN)

    def get_chat_message_count(self) -> int:
        msgs = self.find_all(*self.CHAT_MESSAGES)
        return len(msgs)

    def is_typing_indicator_visible(self) -> bool:
        return self.is_element_present(*self.TYPING_INDICATOR)

    def upload_additional_evidence(self, file_path: str):
        el = self.wait_for_element(*self.EVIDENCE_FILE_INPUT)
        el.send_keys(file_path)

    def get_error_message(self) -> str:
        try:
            return self.get_text(*self.ERROR_MESSAGE)
        except Exception:
            return ""
