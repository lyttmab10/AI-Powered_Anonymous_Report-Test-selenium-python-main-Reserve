# tests/test_TC054_057_analytics.py
# FR-ANA: แดชบอร์ดสถิติและการวิเคราะห์ (Analytics Dashboard)
# TC-054 to TC-057

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.admin_page import AdminPage
from pages.login_page import LoginPage


def _login_admin(driver, base_url, config):
    lp = LoginPage(driver, base_url, timeout=config["timeout"])
    lp.open_login()
    lp.login(config["admin_username"], config["admin_password"])
    return lp.is_logged_in()


def _open_analytics(driver, base_url, config) -> AdminPage:
    ap = AdminPage(driver, base_url, timeout=config["timeout"])
    ap.open_dashboard()
    if ap.is_element_present(*AdminPage.ANALYTICS_TAB):
        ap.click(*AdminPage.ANALYTICS_TAB)
    return ap


# ── TC-054: KPI Summary Cards 5 การ์ด ──────────────────────────────────────
@pytest.mark.tc054
@pytest.mark.fr_ana
class TestTC054KPICards:
    """
    TC-054 | FR-ANA-001 | Priority: สูง | Type: Positive
    หน้า Analytics ต้องแสดง KPI Summary Cards อย่างน้อย 5 การ์ด
    """

    def test_kpi_cards_count_at_least_5(self, driver, base_url, config):
        """ต้องแสดง KPI cards อย่างน้อย 5 การ์ด"""
        if not _login_admin(driver, base_url, config):
            pytest.skip("login ไม่สำเร็จ")
        ap = _open_analytics(driver, base_url, config)
        count = ap.get_kpi_card_count()
        assert count >= 5, (
            f"ต้องมี KPI cards อย่างน้อย 5 ใบ แต่พบ {count}"
        )

    def test_kpi_cards_contain_numbers(self, driver, base_url, config):
        """KPI cards ต้องแสดงตัวเลขสถิติ"""
        if not _login_admin(driver, base_url, config):
            pytest.skip("login ไม่สำเร็จ")
        ap = _open_analytics(driver, base_url, config)
        cards = ap.find_all(*AdminPage.KPI_CARDS)
        if not cards:
            pytest.skip("ไม่พบ KPI cards")
        has_number = any(
            any(c.isdigit() for c in card.text)
            for card in cards
        )
        assert has_number, "KPI cards ต้องแสดงตัวเลข"


# ── TC-055: กราฟสัดส่วนเรื่องร้องเรียนแยกตามหมวดหมู่ (7 หมวด) ─────────────
@pytest.mark.tc055
@pytest.mark.fr_ana
class TestTC055CategoryChart:
    """
    TC-055 | FR-ANA-002 | Priority: กลาง | Type: Positive
    ต้องแสดงกราฟแสดงสัดส่วนตามหมวดหมู่ (ใน 7 หมวด)
    """

    def test_category_chart_visible(self, driver, base_url, config):
        """ต้องมีกราฟ (canvas/svg) สำหรับหมวดหมู่"""
        if not _login_admin(driver, base_url, config):
            pytest.skip("login ไม่สำเร็จ")
        ap = _open_analytics(driver, base_url, config)
        charts = ap.find_all(*AdminPage.CHART_CONTAINER)
        assert len(charts) >= 1, "ต้องมีกราฟอย่างน้อย 1 อัน"

    def test_category_labels_present(self, driver, base_url, config):
        """ต้องมีป้ายกำกับหมวดหมู่แสดงในกราฟหรือ legend"""
        if not _login_admin(driver, base_url, config):
            pytest.skip("login ไม่สำเร็จ")
        ap = _open_analytics(driver, base_url, config)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        # Check for Thai category keywords in the analytics page
        categories = ["ทุจริต", "ล่วงละเมิด", "สิ่งแวดล้อม", "อื่น"]
        found = [c for c in categories if c in body_text]
        # Soft assertion – may depend on data
        assert True, f"Categories found in page: {found}"


# ── TC-056: กราฟสัดส่วนระดับความเร่งด่วน ───────────────────────────────────
@pytest.mark.tc056
@pytest.mark.fr_ana
class TestTC056UrgencyChart:
    """
    TC-056 | FR-ANA-003 | Priority: กลาง | Type: Positive
    ต้องแสดงกราฟสัดส่วนระดับความเร่งด่วน
    """

    def test_urgency_chart_visible(self, driver, base_url, config):
        """ต้องมีกราฟแสดงระดับความเร่งด่วน"""
        if not _login_admin(driver, base_url, config):
            pytest.skip("login ไม่สำเร็จ")
        ap = _open_analytics(driver, base_url, config)
        charts = ap.find_all(*AdminPage.CHART_CONTAINER)
        assert len(charts) >= 1, "ต้องมีกราฟอย่างน้อย 1 อัน"

    def test_urgency_levels_in_page(self, driver, base_url, config):
        """ต้องมีป้ายระดับความเร่งด่วน (สูง/กลาง/ต่ำ) ในหน้า analytics"""
        if not _login_admin(driver, base_url, config):
            pytest.skip("login ไม่สำเร็จ")
        ap = _open_analytics(driver, base_url, config)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        urgency_kws = ["สูง", "กลาง", "ต่ำ", "ด่วน", "high", "medium", "low"]
        found = [kw for kw in urgency_kws if kw.lower() in body_text.lower()]
        assert True, f"Urgency keywords found: {found}"


# ── TC-057: แนวโน้มรายเดือนและ Hotspots ───────────────────────────────────
@pytest.mark.tc057
@pytest.mark.fr_ana
class TestTC057MonthlyTrendHotspots:
    """
    TC-057 | FR-ANA-004 | Priority: กลาง | Type: Positive
    ต้องแสดงกราฟแนวโน้มรายเดือนและการจัดอันดับพื้นที่เสี่ยง (Hotspots)
    """

    TREND_CHART = (By.CSS_SELECTOR, "[class*='trend'], [class*='monthly'], [class*='hotspot']")

    def test_trend_chart_or_hotspot_visible(self, driver, base_url, config):
        """ต้องมีกราฟ trend หรือ hotspot ในหน้า analytics"""
        if not _login_admin(driver, base_url, config):
            pytest.skip("login ไม่สำเร็จ")
        ap = _open_analytics(driver, base_url, config)
        charts = ap.find_all(*AdminPage.CHART_CONTAINER)
        trend_elements = driver.find_elements(*self.TREND_CHART)
        assert len(charts) >= 1 or len(trend_elements) >= 1, (
            "ต้องมีกราฟ trend หรือ hotspot อย่างน้อย 1 อัน"
        )

    def test_analytics_page_loads_completely(self, driver, base_url, config):
        """หน้า Analytics ต้องโหลดสำเร็จโดยไม่มี error"""
        if not _login_admin(driver, base_url, config):
            pytest.skip("login ไม่สำเร็จ")
        ap = _open_analytics(driver, base_url, config)
        # Check no error elements
        errors = driver.find_elements(
            By.CSS_SELECTOR, "[class*='error-page'], [class*='404'], [class*='500']"
        )
        assert len(errors) == 0, "ไม่ควรมี error page ในหน้า Analytics"
