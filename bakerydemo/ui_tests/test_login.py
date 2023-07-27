import re

from playwright.sync_api import Page, expect


def test_login_wagtail_admin(page: Page):
    page.goto("http://localhost:8000/admin")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Sign in - Wagtail"))

    # create a locator
    username_input = page.locator("input[name='username']")
    password_input = page.locator("input[name='password']")

    username_input.fill("admin")
    password_input.fill("changeme")

    sign_in_button = page.locator("button[type='submit']")
    sign_in_button.click()

    # Expects the URL to contain /admin/.
    expect(page).to_have_url(re.compile("^http://localhost:8000/admin/$"))
    expect(page).to_have_title(re.compile("Dashboard - Wagtail"))
    expect(page.get_by_text("Welcome to the bakerydemo Wagtail CMS")).to_be_visible()
