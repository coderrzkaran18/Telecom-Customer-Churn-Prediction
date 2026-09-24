# ============================================================
#  TELCO CHURN - AUTOMATED UI SCREENSHOTS
#  Playwright se Streamlit app ke 2 screenshots leta hai:
#    - screenshots/ui_churn_yes.png  (Churn = YES)
#    - screenshots/ui_churn_no.png   (Churn = NO)
#
#  Install command (pehli baar):
#      pip install playwright
#      python -m playwright install chromium
#
#  Run command:
#      python take_ui_screenshots.py
# ============================================================

import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# ── Config ──────────────────────────────────────────────────
APP_URL        = "http://localhost:8501"
OUTPUT_DIR     = "screenshots"
SCREENSHOT_YES = os.path.join(OUTPUT_DIR, "ui_churn_yes.png")
SCREENSHOT_NO  = os.path.join(OUTPUT_DIR, "ui_churn_no.png")
VIEWPORT       = {"width": 1200, "height": 900}

# screenshots/ folder banana
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"[OK] '{OUTPUT_DIR}/' folder ready.\n")


def wait_for_app(page, timeout_ms=20000):
    """Streamlit app ke fully load hone ka wait karo."""
    page.wait_for_load_state("networkidle", timeout=timeout_ms)
    # Streamlit spinner band hone ka intezaar
    try:
        page.wait_for_selector(
            "[data-testid='stAppViewContainer']",
            timeout=timeout_ms
        )
    except PWTimeout:
        pass  # Older Streamlit version mein selector alag ho sakta hai
    time.sleep(2)   # Extra buffer for JS rendering


def click_button_by_text(page, text):
    """
    Button ko uske visible text se dhundh ke click karo.
    Streamlit buttons ka exact selector version-dependent hota hai,
    isliye text-based approach use karte hain.
    """
    # Try data-testid wala locator pehle
    try:
        page.get_by_role("button", name=text).first.click(timeout=5000)
        return True
    except Exception:
        pass
    # Fallback: contains text
    try:
        page.locator(f"button:has-text('{text}')").first.click(timeout=5000)
        return True
    except Exception:
        return False


def submit_form(page):
    """'Predict Churn' form submit karo."""
    submitted = click_button_by_text(page, "Predict Churn")
    if not submitted:
        # Last resort: pehla primary button
        try:
            page.locator("[data-testid='stFormSubmitButton'] button").click(timeout=5000)
            submitted = True
        except Exception:
            pass
    time.sleep(3)   # Result render hone do
    return submitted


def take_screenshot(page, filepath, label):
    """Full page screenshot lo aur save karo."""
    page.screenshot(path=filepath, full_page=True)
    size_kb = os.path.getsize(filepath) / 1024
    print(f"[OK] {label}")
    print(f"     Saved : {filepath}  ({size_kb:.1f} KB)")


# ── MAIN ────────────────────────────────────────────────────
print("=" * 60)
print("  STREAMLIT UI SCREENSHOT TOOL")
print("=" * 60)
print(f"  App URL  : {APP_URL}")
print(f"  Output   : {OUTPUT_DIR}/")
print()

with sync_playwright() as pw:

    # Chromium browser launch karo (headless=False to dekh sako kya ho raha hai)
    browser = pw.chromium.launch(
        headless=False,          # True karo agar silently run karna ho
        args=["--start-maximized"]
    )
    context = browser.new_context(viewport=VIEWPORT)
    page    = context.new_page()

    print("[..] App open kar raha hun...")
    page.goto(APP_URL, wait_until="domcontentloaded", timeout=30000)
    wait_for_app(page)
    print("[OK] App load ho gayi.\n")

    # ── Screenshot 1: Churn = YES ────────────────────────────
    print("--- Screenshot 1: CHURN = YES ---")

    # "Sample: Likely Churn" button click karo
    ok = click_button_by_text(page, "Sample: Likely Churn")
    if ok:
        print("[OK] 'Sample: Likely Churn' clicked")
        time.sleep(2)   # Form re-render ka wait
    else:
        print("[WARN] Sample button nahi mila — manual values set ho sakti hain")

    # Form submit karo
    ok = submit_form(page)
    if ok:
        print("[OK] 'Predict Churn' submitted")
    else:
        print("[WARN] Submit button click fail — result visible ho sakta hai phir bhi")

    time.sleep(2)
    take_screenshot(page, SCREENSHOT_YES, "Screenshot 1 saved: ui_churn_yes.png")
    print()

    # ── Screenshot 2: Churn = NO ─────────────────────────────
    print("--- Screenshot 2: CHURN = NO ---")

    # "Sample: Loyal Customer" button click karo
    ok = click_button_by_text(page, "Sample: Loyal Customer")
    if ok:
        print("[OK] 'Sample: Loyal Customer' clicked")
        time.sleep(2)
    else:
        print("[WARN] Sample button nahi mila")

    ok = submit_form(page)
    if ok:
        print("[OK] 'Predict Churn' submitted")
    else:
        print("[WARN] Submit button click fail")

    time.sleep(2)
    take_screenshot(page, SCREENSHOT_NO, "Screenshot 2 saved: ui_churn_no.png")
    print()

    browser.close()

# ── Summary ─────────────────────────────────────────────────
print("=" * 60)
yes_ok = os.path.isfile(SCREENSHOT_YES)
no_ok  = os.path.isfile(SCREENSHOT_NO)
print(f"  ui_churn_yes.png : {'[OK] EXISTS' if yes_ok else '[FAIL] MISSING'}")
print(f"  ui_churn_no.png  : {'[OK] EXISTS' if no_ok  else '[FAIL] MISSING'}")
print()
if yes_ok and no_ok:
    print("[OK] Dono screenshots ready hain!")
    print("     Next step: python generate_report_docx.py")
else:
    print("[WARN] Kuch screenshots nahi bani. Manual steps dekho:")
    print("  1. http://localhost:8501 browser mein kholo")
    print("  2. 'Sample: Likely Churn' click karo -> 'Predict Churn' -> Win+Shift+S")
    print("     Save as: screenshots/ui_churn_yes.png")
    print("  3. 'Sample: Loyal Customer' click karo -> 'Predict Churn' -> Win+Shift+S")
    print("     Save as: screenshots/ui_churn_no.png")
print("=" * 60)
