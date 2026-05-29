import unittest
from googlesearch import (
    search,
    lucky,
    get_random_user_agent,
    get_tbs,
    filter_result,
)
import datetime


class TestFilterResult(unittest.TestCase):
    def test_normal_url(self):
        self.assertEqual(
            filter_result("http://example.com/page"),
            "http://example.com/page",
        )

    def test_https_url(self):
        self.assertEqual(
            filter_result("https://example.com/page"),
            "https://example.com/page",
        )

    def test_no_netloc(self):
        self.assertIsNone(filter_result("/relative/path"))

    def test_google_links_excluded(self):
        self.assertIsNone(
            filter_result("http://google.com/search", include_google_links=False),
        )

    def test_google_links_included(self):
        self.assertEqual(
            filter_result("http://google.com/search", include_google_links=True),
            "http://google.com/search",
        )

    def test_url_decode(self):
        self.assertEqual(
            filter_result("/url?q=http://example.com"),
            "http://example.com",
        )

    def test_url_decode_missing_q(self):
        self.assertIsNone(filter_result("/url?foo=bar"))

    def test_url_decode_empty_q(self):
        self.assertIsNone(filter_result("/url?q="))


class TestGetRandomUserAgent(unittest.TestCase):
    def test_returns_string(self):
        ua = get_random_user_agent()
        self.assertIsInstance(ua, str)
        self.assertGreater(len(ua), 0)


class TestGetTbs(unittest.TestCase):
    def test_returns_formatted_string(self):
        from_date = datetime.date(2024, 1, 1)
        to_date = datetime.date(2024, 12, 31)
        result = get_tbs(from_date, to_date)
        self.assertIn("cdr:1", result)
        self.assertIn("01/01/2024", result)
        self.assertIn("12/31/2024", result)


class TestLucky(unittest.TestCase):
    def test_returns_none_for_empty(self):
        result = lucky(query="a9f3b7c2d8e1f4a6b0c3d2e1f4a5b6c7")
        self.assertIsNone(result)


class TestSearchValidation(unittest.TestCase):
    def test_raises_on_overlapping_extra_params(self):
        with self.assertRaises(ValueError):
            next(search("test", extra_params={"q": "override"}))


class TestVersion(unittest.TestCase):
    def test_version_exists(self):
        from googlesearch import __version__

        self.assertIsInstance(__version__, str)
        parts = __version__.split(".")
        self.assertEqual(len(parts), 3)


if __name__ == "__main__":
    unittest.main()
