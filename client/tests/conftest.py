import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@pytest.fixture(scope="session")
def chrome_options():
    """Fixture to provide Chrome options"""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Enable headless mode for CI/CD environments
    if os.getenv("CI") or os.getenv("JENKINS_HOME"):
        options.add_argument("--headless")
    
    # Disable notifications
    prefs = {"profile.default_content_settings.popups": 0}
    options.add_experimental_option("prefs", prefs)
    
    return options

@pytest.fixture(scope="session")
def chrome_driver(chrome_options):
    """Fixture to provide Chrome WebDriver"""
    try:
        # Try to use webdriver-manager if available
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    except:
        # Fallback to system chrome driver
        driver = webdriver.Chrome(options=chrome_options)
    
    yield driver
    driver.quit()

@pytest.fixture
def browser(chrome_driver):
    """Fixture to reset browser state between tests"""
    chrome_driver.delete_all_cookies()
    chrome_driver.execute_script("window.localStorage.clear();")
    yield chrome_driver

@pytest.fixture
def app_url():
    """Fixture to provide application URL"""
    return os.getenv("APP_URL", "http://localhost:5173")

@pytest.fixture
def test_user():
    """Fixture to provide test user credentials"""
    return {
        "email": "testuser@example.com",
        "password": "TestPassword123",
        "username": "testuser"
    }

# pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
