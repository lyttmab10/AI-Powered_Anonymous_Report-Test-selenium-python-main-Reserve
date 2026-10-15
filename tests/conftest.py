# conftest.py - Pytest Configuration & Shared Fixtures
# Anonymous Report System (TrustLine / NPRU Sentinel)
# Based on: Annonymous-Test-Cases.docx & Annonymous-Test-Plan-and-Report.docx

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
BASE_URL = os.environ.get("BASE_URL", "https://anonymous-report.ai.studio")
BROWSER   = os.environ.get("BROWSER", "chrome").lower()
HEADLESS  = os.environ.get("HEADLESS", "false").lower() == "true"
TIMEOUT   = int(os.environ.get("TIMEOUT", "15"))

# Admin credentials (from Test Plan section 1.4.1)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")

# Officer/Investigator credentials
OFFICER_USERNAME = os.environ.get("OFFICER_USERNAME", "officer1")
OFFICER_PASSWORD = os.environ.get("OFFICER_PASSWORD", "officer1")


def pytest_addoption(parser):
    parser.addoption("--base-url",  default=BASE_URL,  help="Base URL of the application under test")
    parser.addoption("--browser",   default=BROWSER,   help="Browser to use: chrome, firefox, edge")
    parser.addoption("--headless",  default="false",   help="Run browser in headless mode (true/false)")
    parser.addoption("--timeout",   default=str(TIMEOUT), help="Implicit wait timeout in seconds")


def _make_chrome_driver(headless: bool) -> webdriver.Chrome:
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = ChromeService(ChromeDriverManager().install())
    except Exception:
        service = ChromeService()

    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=th")
    return webdriver.Chrome(service=service, options=options)


def _make_firefox_driver(headless: bool) -> webdriver.Firefox:
    try:
        from webdriver_manager.firefox import GeckoDriverManager
        service = FirefoxService(GeckoDriverManager().install())
    except Exception:
        service = FirefoxService()

    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    return webdriver.Firefox(service=service, options=options)


def _make_edge_driver(headless: bool) -> webdriver.Edge:
    try:
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        service = EdgeService(EdgeChromiumDriverManager().install())
    except Exception:
        service = EdgeService()

    options = EdgeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Edge(service=service, options=options)


@pytest.fixture(scope="session")
def config(request):
    """Session-wide configuration dictionary."""
    return {
        "base_url":         request.config.getoption("--base-url", default=BASE_URL),
        "browser":          request.config.getoption("--browser",  default=BROWSER),
        "headless":         request.config.getoption("--headless", default="false").lower() == "true",
        "timeout":          int(request.config.getoption("--timeout", default=str(TIMEOUT))),
        "admin_username":   ADMIN_USERNAME,
        "admin_password":   ADMIN_PASSWORD,
        "officer_username": OFFICER_USERNAME,
        "officer_password": OFFICER_PASSWORD,
    }


@pytest.fixture()
def driver(config):
    """Function-scoped WebDriver – creates a fresh browser per test."""
    browser  = config["browser"]
    headless = config["headless"]
    timeout  = config["timeout"]

    if browser == "firefox":
        drv = _make_firefox_driver(headless)
    elif browser == "edge":
        drv = _make_edge_driver(headless)
    else:
        drv = _make_chrome_driver(headless)

    drv.implicitly_wait(timeout)
    drv.set_window_size(1920, 1080)
    yield drv
    drv.quit()


@pytest.fixture()
def wait(driver, config):
    """Explicit WebDriverWait tied to the current driver."""
    return WebDriverWait(driver, config["timeout"])


@pytest.fixture()
def base_url(config):
    return config["base_url"]
