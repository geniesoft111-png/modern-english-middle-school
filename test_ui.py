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
        
        # 3. Home Fee & Book List Quick Link
        fee_card = page.locator('button:has-text("Fee & Book List")')
        assert fee_card.count() >= 1, "Home fee & book list quick card missing"
        assert "Monthly ₹400–₹500" in fee_card.text_content(), "Outdated fee label on home card"
        results.append(("Home Quick Links", "PASS - Fee & Book List card present"))

        # 4. Academics: Monthly Fee Schedule
        page.locator('header button:has-text("Academics")').first.click()
        page.wait_for_timeout(400)
        
        sched_heading = page.locator('h2:has-text("Monthly Fee Schedule 2026-27")')
        assert sched_heading.count() >= 1, "Monthly Fee Schedule heading missing"
        
        body_text = page.locator('main').text_content()
        assert "₹400 / mo" in body_text, "Nursery ₹400 / mo fee missing"
        assert "₹450 / mo" in body_text, "Classes I-IV ₹450 / mo fee missing"
        assert "₹500 / mo" in body_text, "Classes V-VIII ₹500 / mo fee missing"
        assert "₹4,005" not in body_text and "₹4005" not in body_text, "Old ₹4,005 fee misnomer found in Academics"
        assert "₹4,505" not in body_text and "₹4505" not in body_text, "Old ₹4,505 fee misnomer found in Academics"
        results.append(("Monthly Fee Schedule", "PASS - Verified ₹400, ₹450, ₹500 monthly rates"))
        
        # 5. Academics: Prescribed Book List & Interactive Class Switching
        book_heading = page.locator('h2:has-text("Prescribed School Book List")')
        assert book_heading.count() >= 1, "Prescribed School Book List section missing"
        
        # Default Class I
        assert page.locator('text=Mathematics Introduction-2').count() >= 1, "Class I Math book missing"
        assert page.locator('text=Subham English Reader-1').count() >= 1, "Class I English book missing"
        assert page.locator('text=Veena Prakashan').count() >= 1, "Veena Prakashan publisher missing"
        assert page.locator('text=No Sanskrit entry is visible in the supplied Class I photograph').count() >= 1, "Class I Sanskrit note missing"
        results.append(("Book List Class I", "PASS - 8 subjects & publishers rendered"))
        
        # Switch to Class III
        page.locator('button:has-text("Class III")').first.click()
        page.wait_for_timeout(300)
        assert page.locator('text=Mathematics Introduction-4*').count() >= 1, "Class III Math book with asterisk missing"
        assert page.locator('text=Verify edition before purchasing').count() >= 1, "Class III edition verification note missing"
        results.append(("Book List Class III", "PASS - Asterisk and edition advisory active"))
        
        # Switch to Class VII (NCERT)
        page.locator('button:has-text("Class VII")').first.click()
        page.wait_for_timeout(300)
        assert page.locator('text=Curiosity').count() >= 1, "Class VII Science (Curiosity) missing"
        assert page.locator('text=Malhar').count() >= 1, "Class VII Hindi (Malhar) missing"
        assert page.locator('text=The Study of Society: India and Beyond').count() >= 1, "Class VII Social Science missing"
        results.append(("Book List Class VII", "PASS - NCERT curriculum & titles verified"))
        
        # Switch to Class VIII
        page.locator('button:has-text("Class VIII")').first.click()
        page.wait_for_timeout(300)
        assert page.locator('text=Ruchira').count() >= 1, "Class VIII Sanskrit (Ruchira) missing"
        assert page.locator('text=Vasant, Mahabharat').count() >= 1, "Class VIII Hindi (Vasant, Mahabharat) missing"
        results.append(("Book List Class VIII", "PASS - Middle school Class VIII books verified"))

        # 6. Notices Tab: Updated Notifications
        page.locator('header button:has-text("Notices")').first.click()
        page.wait_for_timeout(400)
        notices_text = page.locator('main').text_content()
        assert "Monthly Fee Schedule 2026–27 Displayed" in notices_text, "Monthly fee notice missing"
        assert "Prescribed Book List 2026–27 Published" in notices_text, "Prescribed book list notice missing"
        results.append(("Notices & Circulars", "PASS - Fee and Book List circulars active"))

        # 7. Admissions Tab: Lightbox & Download
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
        
        # 8. Contact Us Form
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
        
        # 9. Mobile Responsiveness
        page.set_viewport_size({"width": 375, "height": 812})
        page.wait_for_timeout(300)
        menu_btn = page.locator('button[aria-label="Menu"]')
        menu_btn.click()
        page.wait_for_timeout(300)
        
        phone_link = page.locator('a[href="tel:9955534352"]')
        assert phone_link.count() >= 1, "Mobile call link missing"
        results.append(("Mobile Call Link", "PASS - Direct tel: link in menu"))
        
        # 10. Zero Console Errors
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
