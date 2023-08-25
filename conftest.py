import pytest
from pytest_html.result import html

perf_metrics = {
    "query_time": "Query time",
    "queries": "Queries",
    "similar": "Similar",
    "duplicates": "Duplicates",
}


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    cells[2:2] = [
        html.th(perf_metrics[metric], col=metric, class_="sortable")
        for metric in perf_metrics
    ]


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    cells[2:2] = [
        html.td(getattr(report, metric, ""), col=metric) for metric in perf_metrics
    ]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if item.user_properties:
        test_properties = {prop[0]: prop[1] for prop in item.user_properties}
        sql_summary = test_properties.get("sql_summary")
        if sql_summary:
            for metric in perf_metrics:
                setattr(report, metric, sql_summary[metric])
