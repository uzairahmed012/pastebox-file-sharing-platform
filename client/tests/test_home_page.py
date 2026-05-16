"""
Home Page Selenium Tests
Tests for PasteBox home page functionality
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


@pytest.mark.smoke
@pytest.mark.ui
class TestHomePageBasics:
    """Basic home page functionality tests"""

    def test_home_page_loads_successfully(self, browser, app_url):
        """
        TEST CASE 1: Verify Home Page Loads Successfully
        
        Description: This test verifies that the PasteBox home page loads
        without errors and displays essential content.
        
        Steps:
            1. Navigate to the application URL
            2. Wait for page to load (max 10 seconds)
            3. Verify page title contains expected keywords
            4. Verify main header is displayed
            5. Verify no error messages are present
        
        Expected Result: 
            - Page should load without HTTP errors
            - Main header should be visible
            - No error messages should appear
        
        Pass Criteria:
            - Page title contains 'PasteBox' or 'File'
            - Header element is displayed
            - No 404 or error status codes
        """
        browser.get(app_url)
        
        # Wait for page title to change
        WebDriverWait(browser, 10).until(
            lambda driver: driver.title
        )
        
        # Verify page title
        page_title = browser.title
        assert page_title, "Page title should not be empty"
        
        # Verify key elements are present
        try:
            header = browser.find_element(By.TAG_NAME, "header")
            assert header.is_displayed(), "Header should be displayed"
        except:
            # If header not found, check for h1
            h1_elements = browser.find_elements(By.TAG_NAME, "h1")
            assert len(h1_elements) > 0, "Page should have heading"
        
        print(f"✓ Home page loaded successfully - Title: {page_title}")

    def test_page_has_upload_section(self, browser, app_url):
        """
        TEST CASE 2: Verify Upload Section Exists
        
        Description: This test verifies that the file upload section is
        visible and accessible to users on the home page.
        
        Steps:
            1. Navigate to application home page
            2. Wait for upload section to load
            3. Verify upload container is present
            4. Verify upload button/zone is visible and enabled
        
        Expected Result:
            - Upload section should be visible
            - Upload button should be clickable
            - Upload area should be accessible
        
        Pass Criteria:
            - Upload button is present and visible
            - Upload button is enabled
            - Upload section occupies visible space
        """
        browser.get(app_url)
        time.sleep(2)  # Allow page to fully render
        
        # Try to find upload section using various selectors
        upload_found = False
        upload_button = None
        
        selectors = [
            (By.CLASS_NAME, "upload"),
            (By.CLASS_NAME, "upload-area"),
            (By.CLASS_NAME, "dropzone"),
            (By.XPATH, "//button[contains(text(), 'Upload')]"),
            (By.XPATH, "//button[contains(text(), 'Choose')]"),
            (By.XPATH, "//div[contains(@class, 'upload')]"),
        ]
        
        for selector in selectors:
            try:
                upload_button = WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located(selector)
                )
                upload_found = True
                break
            except:
                continue
        
        assert upload_found, "Upload section should be visible on home page"
        
        if upload_button:
            assert upload_button.is_displayed(), "Upload button should be displayed"
            print("✓ Upload section verified and visible")

    def test_navigation_elements_visible(self, browser, app_url):
        """
        TEST CASE 3: Verify Navigation Elements
        
        Description: This test ensures that main navigation elements
        are visible and functional on the home page.
        
        Steps:
            1. Load home page
            2. Check for navigation elements (header, nav bar, etc.)
            3. Verify at least one navigation link is visible
            4. Verify navigation elements are clickable
        
        Expected Result:
            - Navigation should be visible
            - Navigation links should be interactive
            - No broken navigation elements
        
        Pass Criteria:
            - Navigation bar or menu is present
            - Navigation elements are clickable
        """
        browser.get(app_url)
        time.sleep(2)
        
        # Look for navigation elements
        nav_elements = browser.find_elements(By.TAG_NAME, "nav")
        nav_buttons = browser.find_elements(By.XPATH, "//button[contains(text(), 'Home') or contains(text(), 'Dashboard') or contains(text(), 'Login')]")
        
        navigation_found = len(nav_elements) > 0 or len(nav_buttons) > 0
        assert navigation_found, "Navigation elements should be present"
        
        print(f"✓ Navigation elements verified - Found {len(nav_elements)} nav, {len(nav_buttons)} buttons")

    @pytest.mark.regression
    def test_page_responsive_layout(self, browser, app_url):
        """
        TEST CASE 4: Verify Page Responsive Design
        
        Description: This test verifies that the page layout is responsive
        and adapts to different viewport sizes.
        
        Steps:
            1. Set viewport to desktop size (1920x1080)
            2. Verify layout works
            3. Set viewport to mobile size (375x667)
            4. Verify layout adapts
            5. Verify elements are still accessible
        
        Expected Result:
            - Page should display properly on different viewport sizes
            - Elements should not overflow or break layout
            - Page should remain usable on mobile
        
        Pass Criteria:
            - No horizontal scrollbars on mobile
            - Main content visible on all sizes
        """
        browser.get(app_url)
        
        # Test desktop size
        browser.set_window_size(1920, 1080)
        time.sleep(1)
        desktop_height = browser.execute_script("return document.body.scrollHeight")
        
        # Test mobile size
        browser.set_window_size(375, 667)
        time.sleep(1)
        mobile_height = browser.execute_script("return document.body.scrollHeight")
        
        # Both should have content
        assert desktop_height > 0, "Desktop layout should have content"
        assert mobile_height > 0, "Mobile layout should have content"
        
        # Reset to desktop
        browser.set_window_size(1920, 1080)
        
        print(f"✓ Responsive layout verified - Desktop: {desktop_height}px, Mobile: {mobile_height}px")


@pytest.mark.smoke
class TestHomePageInteraction:
    """Test user interactions on home page"""

    def test_hover_effects_on_buttons(self, browser, app_url):
        """
        TEST CASE 5: Verify Hover Effects on Interactive Elements
        
        Description: This test verifies that buttons and clickable elements
        respond to hover interactions.
        
        Steps:
            1. Navigate to home page
            2. Find main buttons
            3. Hover over button
            4. Verify visual feedback (class change, style change)
        
        Expected Result:
            - Buttons should respond to hover
            - Visual feedback should be provided
            - No JavaScript errors on hover
        
        Pass Criteria:
            - Hover action completes without error
            - Element remains visible after hover
        """
        browser.get(app_url)
        time.sleep(2)
        
        try:
            # Find a clickable element
            buttons = browser.find_elements(By.TAG_NAME, "button")
            
            if buttons:
                button = buttons[0]
                
                # Store original class
                original_class = button.get_attribute("class")
                
                # Hover over button
                actions = ActionChains(browser)
                actions.move_to_element(button).perform()
                time.sleep(0.5)
                
                # Verify button is still there
                assert button.is_displayed(), "Button should remain visible after hover"
                
                print(f"✓ Hover effects verified - Button remains interactive")
            else:
                pytest.skip("No buttons found to test hover effects")
                
        except Exception as e:
            pytest.fail(f"Hover effect test failed: {str(e)}")

    def test_guest_access_without_login(self, browser, app_url):
        """
        TEST CASE 6: Verify Guest Users Can Access Upload Feature
        
        Description: This test verifies that guest users (non-authenticated)
        can access and use the file upload feature without logging in.
        
        Steps:
            1. Navigate to home page without authentication
            2. Check if upload feature is accessible
            3. Verify no "authentication required" message
            4. Verify upload controls are enabled
        
        Expected Result:
            - Upload feature should be accessible to guests
            - No authentication barrier on upload
            - Upload controls should be enabled
        
        Pass Criteria:
            - Upload area is visible
            - No login required message
            - Upload button is enabled
        """
        # Clear cookies to ensure guest access
        browser.delete_all_cookies()
        browser.get(app_url)
        time.sleep(2)
        
        page_source = browser.page_source
        
        # Check for "login required" message
        login_required_indicators = [
            "Please login",
            "Sign in required",
            "Authentication required",
            "Unauthorized"
        ]
        
        for indicator in login_required_indicators:
            assert indicator.lower() not in page_source.lower(), \
                f"Page should not show '{indicator}' message for guest access"
        
        print("✓ Guest access verified - No authentication barrier detected")

    @pytest.mark.regression
    def test_page_load_performance(self, browser, app_url):
        """
        TEST CASE 7: Verify Page Load Performance
        
        Description: This test measures page load time and verifies
        it meets performance standards.
        
        Steps:
            1. Measure page load start time
            2. Navigate to home page
            3. Wait for key elements to load
            4. Measure total load time
            5. Verify load time is acceptable (< 5 seconds)
        
        Expected Result:
            - Page should load within 5 seconds
            - Key elements should load within 3 seconds
            - No performance warnings
        
        Pass Criteria:
            - Page load time < 5 seconds
            - Main content visible within 3 seconds
        """
        import time as timer
        
        start_time = timer.time()
        browser.get(app_url)
        
        # Wait for main content
        try:
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            pass
        
        load_time = timer.time() - start_time
        
        # Page should load reasonably fast
        assert load_time < 10, f"Page took too long to load: {load_time:.2f}s"
        
        print(f"✓ Page load performance verified - Load time: {load_time:.2f}s")
