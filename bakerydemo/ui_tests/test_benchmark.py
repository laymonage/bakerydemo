import os
import re

import pytest
from playwright.sync_api import Page, expect


class LiveServerTest:
    LIVE_SERVER_URL = f"http://localhost:{os.environ.get('BENCHMARK_PORT', '8453')}"

    @pytest.fixture(params=["admin", "eddythor", "moderrathor"])
    def multi_user(self, request, page: Page):
        page.goto(f"{self.LIVE_SERVER_URL}/admin")

        username_input = page.locator("input[name='username']")
        password_input = page.locator("input[name='password']")

        username_input.fill(request.param)
        password_input.fill("changeme")

        sign_in_button = page.locator("button[type='submit']")
        sign_in_button.click()

    def parse_sql_summary_to_dict(self, input_string) -> dict | None:
        pattern = (
            r"(\w+):\s*([\d.]+\s*ms)\s*"
            r"\((\d+)\s*queries"
            r"(?:\s*including\s*(\d+)\s*similar)?"
            r"(?:\s*and\s*(\d+) duplicates)?\s*\)"
        )
        match = re.match(pattern, input_string)
        if match:
            connection, time, queries, similar, duplicates = match.groups()
            result_dict = {
                "connection": connection,
                "query_time": time,
                "queries": int(queries),
                "similar": 0,
                "duplicates": 0,
            }
            if similar:
                result_dict["similar"] = int(similar)
            if duplicates:
                result_dict["duplicates"] = int(duplicates)
            return result_dict
        else:
            return None

    def get_sql_summary(self, page: Page) -> str:
        # Activate the SQL panel if it is not already active.
        page.locator("#djdt-SQLPanel:not(.djdt-active) a").click()

        # Get the SQL summary for the first (default) connection.
        connection = page.locator(".djdt-scroll > ul > li").first
        connection_name = connection.locator("strong").text_content().strip()
        description = " ".join(s.strip() for s in connection.all_inner_texts())
        summary = description[len(connection_name) :].strip()
        return f"{connection_name}: {summary}"

    def record_sql_summary(self, page: Page, record_property) -> dict:
        page.reload()
        summary = self.get_sql_summary(page)
        summary_dict = self.parse_sql_summary_to_dict(summary)
        record_property("sql_summary", summary_dict)


class TestBenchmark(LiveServerTest):
    def test_login_wagtail_admin(self, page: Page, multi_user, record_property):
        expect(page).to_have_url(re.compile(f"^{self.LIVE_SERVER_URL}/admin/$"))
        expect(page).to_have_title(re.compile("Dashboard - Wagtail"))
        expect(
            page.get_by_text("Welcome to the bakerydemo Wagtail CMS")
        ).to_be_visible()
        self.record_sql_summary(page, record_property)

    def test_page_explorer_root(self, page: Page, multi_user, record_property):
        page.get_by_role("button", name="Pages").click()
        page.get_by_role("link", name="Welcome to the Wagtail Bakery! English").click()

        self.record_sql_summary(page, record_property)

    def test_explore_blog_index_page(self, page: Page, multi_user, record_property):
        page.get_by_role("button", name="Pages").click()
        page.get_by_role(
            "link", name="View child pages of 'Welcome to the Wagtail Bakery!'"
        ).click()
        page.get_by_role("link", name="Blog", exact=True).click()

        self.record_sql_summary(page, record_property)

    def test_edit_blog_page(self, page: Page, multi_user, record_property):
        page.get_by_role("button", name="Pages").click()
        page.get_by_role(
            "link", name="View child pages of 'Welcome to the Wagtail Bakery!'"
        ).click()
        page.get_by_role("link", name="View child pages of 'Blog'").click()
        page.get_by_role("link", name="Edit 'Tracking Wild Yeast'").click()

        self.record_sql_summary(page, record_property)

    def test_image_index(self, page: Page, multi_user, record_property):
        page.get_by_role("link", name="Images", exact=True).click()

        self.record_sql_summary(page, record_property)
