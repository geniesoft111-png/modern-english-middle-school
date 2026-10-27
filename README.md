# Modern English Middle School (MEMS), Andar, Siwan

Official web portal for **Modern English Middle School**, located near Central Bank, Gaura Road, Village Andar, Siwan – 841231, Bihar.

- **Established:** 20 August 1990
- **UDISE Code:** 10160109812
- **RTE Recognition:** RTE/SWN/2014-15 0065
- **Registration:** 214812432021916165-717-2026-2027
- **Trust Affiliation:** Modern Educational Welfare Trust / Spectrum Career Development Center Trust, New Delhi
- **Leadership:** Munna Kumar Singh (Director) & Chandrika Bhakta (Principal)
- **Classes:** Nursery to Class VIII (Co-Educational, English Medium with Hindi & Urdu support)
- **Helpline:** +91 99555-34352 / memschoolandar@gmail.com

---

## Features

- **Responsive Design:** Optimized for mobile phones, tablets, and high-resolution desktop screens.
- **Self-Contained Single-Page Application:** Built with React and Tailwind CSS, bundled with all school photography and branding embedded.
- **Interactive Lightbox:** Full resolution viewer for campus pictures and the official admission form.
- **Direct Actions:** One-tap calling (`tel:9955534352`), WhatsApp inquiry (`wa.me`), and email links.
- **Admissions & Fee Portal:** Complete fee structure, class eligibility, and instant admission inquiry form with automated field clearing and confirmation.

---

## Testing with Playwright

Automated end-to-end UI tests are included via Playwright.

```bash
# Run UI verification test suite
python3 test_ui.py
```

---

## Live Deployment (GitHub Pages)

To host this repository live on GitHub Pages:

1. Push the code to GitHub:
   ```bash
   git push -u origin main
   ```
2. In the GitHub repository, navigate to **Settings** > **Pages**.
3. Under **Build and deployment**:
   - **Source:** Deploy from a branch
   - **Branch:** `main` / `/ (root)`
4. Click **Save**. Your site will be live at:
   `https://geniesoft111-png.github.io/modern-english-middle-school/`
