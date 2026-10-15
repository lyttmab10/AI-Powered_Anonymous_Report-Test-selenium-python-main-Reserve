# pages/admin_page.py – Admin / Case Management Dashboard
# Covers TC-039 to TC-057  (FR-CAS, FR-ANA groups) and TC-058-063 (FR-SEC)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class AdminPage(BasePage):
    """
    Page object for the staff/admin case management dashboard.
    Accessible after login at {base_url}/admin or /dashboard.
    """

    # ── Locators ──────────────────────────────────────────
    # Navigation
    CASES_TAB           = (By.XPATH, "//a[contains(@href,'case') or contains(text(),'รายงาน') or contains(text(),'คดี')]")
    ANALYTICS_TAB       = (By.XPATH, "//a[contains(@href,'analyt') or contains(text(),'สถิติ') or contains(text(),'แดชบอร์ด')]")

    # Case table
    CASE_TABLE          = (By.CSS_SELECTOR, "table, [class*='case-table'], [class*='caseTable']")
    CASE_ROWS           = (By.CSS_SELECTOR, "tbody tr, [class*='case-row'], [class*='caseRow']")
    SEARCH_INPUT        = (By.CSS_SELECTOR, "input[type='search'], input[placeholder*='ค้นหา'], input[name*='search']")
    FILTER_DROPDOWN     = (By.CSS_SELECTOR, "select[name*='filter'], select[name*='status'], [class*='filter']")
    PAGINATION          = (By.CSS_SELECTOR, "[class*='pagination'], [class*='Pagination'], nav[aria-label*='page']")
    NEXT_PAGE_BTN       = (By.CSS_SELECTOR, "[class*='next'], button[aria-label*='next'], a[aria-label*='next']")

    # Case detail / edit
    STATUS_DROPDOWN     = (By.CSS_SELECTOR, "select[name*='status'], [class*='status-select']")
    URGENCY_DROPDOWN    = (By.CSS_SELECTOR, "select[name*='urgency'], select[name*='priority']")
    CATEGORY_DROPDOWN   = (By.CSS_SELECTOR, "select[name*='category']")
    SAVE_BUTTON         = (By.CSS_SELECTOR, "button[class*='save'], button[type='submit']")
    INTERNAL_NOTE       = (By.CSS_SELECTOR, "textarea[name*='note'], textarea[name*='internal']")
    LIGHTBOX            = (By.CSS_SELECTOR, "[class*='lightbox'], [class*='modal'][class*='image'], [class*='Lightbox']")

    # Delete / confirm dialog
    DELETE_BUTTON       = (By.CSS_SELECTOR, "button[class*='delete'], button[class*='Delete']")
    CONFIRM_DIALOG      = (By.CSS_SELECTOR, "[role='dialog'], [class*='modal'], [class*='confirm']")
    CONFIRM_YES_BTN     = (By.CSS_SELECTOR, "[class*='confirm'] button[class*='yes'], [role='dialog'] button[class*='danger']")
    CANCEL_BTN          = (By.CSS_SELECTOR, "[class*='confirm'] button[class*='cancel'], [role='dialog'] button[class*='cancel']")

    # Chat (officer side)
    CHAT_INPUT          = (By.CSS_SELECTOR, "input[name*='message'], textarea[name*='message']")
    CHAT_SEND_BTN       = (By.CSS_SELECTOR, "button[class*='send']")
    CHAT_MESSAGES       = (By.CSS_SELECTOR, "[class*='message']")
    UNREAD_BADGE        = (By.CSS_SELECTOR, "[class*='badge'], [class*='unread'], [class*='notification-count']")

    # CSV export
    EXPORT_CSV_BTN      = (By.XPATH, "//button[contains(text(),'CSV') or contains(text(),'ส่งออก') or contains(text(),'Export')]")

    # Analytics / KPI cards
    KPI_CARDS           = (By.CSS_SELECTOR, "[class*='kpi'], [class*='summary-card'], [class*='stat-card']")
    CHART_CONTAINER     = (By.CSS_SELECTOR, "[class*='chart'], canvas, svg[class*='chart']")

    # Audit trail
    AUDIT_LOG           = (By.CSS_SELECTOR, "[class*='audit'], [class*='log'], [class*='history']")

    def open_dashboard(self):
        self.open("/admin")
        # Also try /dashboard if /admin redirects elsewhere
        try:
            self.wait.until(EC.any_of(
                EC.presence_of_element_located(self.CASE_TABLE),
                EC.presence_of_element_located(self.CASES_TAB),
            ))
        except Exception:
            self.open("/dashboard")

    def get_case_row_count(self) -> int:
        rows = self.find_all(*self.CASE_ROWS)
        return len(rows)

    def search_cases(self, text: str):
        self.type_text(*self.SEARCH_INPUT, text)

    def click_case_row(self, index: int = 0):
        rows = self.find_all(*self.CASE_ROWS)
        rows[index].click()

    def change_status(self, status_value: str):
        from selenium.webdriver.support.ui import Select
        el = self.wait_visible(*self.STATUS_DROPDOWN)
        Select(el).select_by_visible_text(status_value)

    def click_delete(self):
        self.click(*self.DELETE_BUTTON)

    def is_confirm_dialog_visible(self) -> bool:
        return self.is_element_present(*self.CONFIRM_DIALOG)

    def confirm_delete(self):
        self.click(*self.CONFIRM_YES_BTN)

    def cancel_delete(self):
        self.click(*self.CANCEL_BTN)

    def click_export_csv(self):
        self.click(*self.EXPORT_CSV_BTN)

    def get_kpi_card_count(self) -> int:
        cards = self.find_all(*self.KPI_CARDS)
        return len(cards)

    def send_chat_message(self, text: str):
        self.type_text(*self.CHAT_INPUT, text)
        self.click(*self.CHAT_SEND_BTN)

    def get_unread_count(self) -> int:
        try:
            badge = self.wait_visible(*self.UNREAD_BADGE)
            return int(badge.text.strip() or "0")
        except Exception:
            return 0

    def is_lightbox_open(self) -> bool:
        return self.is_element_present(*self.LIGHTBOX)
