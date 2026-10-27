import os
import sys
from playwright.sync_api import sync_playwright

def test_modern_english_middle_school():
    html_file = os.path.abspath('index.html')
    if not os.path.exists(html_file):
        raise FileNotFoundError(f"Cannot find {html_file}")
    
    file_url = f"file://{html_file}"
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(f"[{m.type}] {m.text}") if m.type == "error" else None)
        
        page.goto(file_url)
        page.wait_for_timeout(800)
        
        # 1. Page Title & Meta
        title = page.title()
        assert "Modern English Middle School" in title, f"Invalid title: {title}"
        results.append(("Page Title", f"PASS - {title}"))
        
        favicon = page.locator('link[rel="icon"]').get_attribute("href")
        assert favicon and favicon.startswith("data:image/svg+xml"), "Missing SVG favicon"
        results.append(("Favicon", "PASS - Brand SVG Icon"))
        
        # 2. Body Font
        body_font = page.evaluate("getComputedStyle(document.body).fontFamily")
        assert "Poppins" in body_font, f"Poppins not applied to body: {body_font}"
        results.append(("Body Font", f"PASS - {body_font}"))
        
        # 3. Admissions Tab: Lightbox & Download
        page.locator('header button:has-text("Admissions")').first.click()
        page.wait_for_timeout(300)
        
        view_btn = page.locator('button:has-text("View Full Form")')
        assert view_btn.count() == 1, "View Full Form button missing"
        view_btn.click()
        page.wait_for_timeout(300)
        
        lightbox = page.locator('img[alt="Lightbox"]')
        assert lightbox.is_visible(), "Lightbox did not open"
        results.append(("Admission Form Lightbox", "PASS - Opens full form modal"))
        
        page.locator('button:has-text("✕")').click()
        page.wait_for_timeout(200)
        assert not lightbox.is_visible(), "Lightbox did not close"
        results.append(("Lightbox Close", "PASS - Closes modal"))
        
        dl_link = page.locator('a:has-text("Download Form")')
        assert dl_link.count() == 1, "Download Form link missing"
        assert dl_link.get_attribute("download") == "MEMS-Admission-Form.jpg"
        results.append(("Download Form Link", "PASS - Configured for download"))
        
        # 4. Contact Us Form
        page.locator('header button:has-text("Contact Us")').first.click()
        page.wait_for_timeout(300)
        
        inputs = page.locator('main form input')
        inputs.nth(0).fill("Pooja Kumari")
        inputs.nth(1).fill("9955512345")
        page.locator('main form textarea').nth(0).fill("Admission inquiry for Class 3")
        page.locator('main form button:has-text("Send Message")').click()
        page.wait_for_timeout(400)
        
        msg = page.locator('text=/Thank you! Your inquiry has been received/')
        assert msg.count() >= 1, "Confirmation alert not shown"
        assert inputs.nth(0).input_value() == "", "Input fields were not cleared"
        results.append(("Contact Form Inquiry", "PASS - Dispatched and reset successfully"))
        
        # 5. Mobile Responsiveness
        page.set_viewport_size({"width": 375, "height": 812})
        page.wait_for_timeout(300)
        menu_btn = page.locator('button[aria-label="Menu"]')
        menu_btn.click()
        page.wait_for_timeout(300)
        
        phone_link = page.locator('a[href="tel:9955534352"]')
        assert phone_link.count() >= 1, "Mobile call link missing"
        results.append(("Mobile Call Link", "PASS - Direct tel: link in menu"))
        
        # 6. Zero Console Errors
        assert len(errors) == 0, f"Errors encountered: {errors}"
        results.append(("Console Errors", "PASS - 0 errors"))
        
        browser.close()

    print("\n" + "="*50)
    print("UI TEST SUITE RESULTS:")
    for test, res in results:
        print(f" • {test}: {res}")
    print("="*50 + "\n")

if __name__ == "__main__":
    test_modern_english_middle_school()
