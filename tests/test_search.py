import os
import sys
import unittest
from unittest.mock import patch
from googlesearch import (
    search,
    lucky,
    get_random_user_agent,
    get_tbs,
    filter_result,
)
import datetime

_FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def _load_fixture(name):
    with open(os.path.join(_FIXTURES_DIR, name), encoding="utf-8") as f:
        return f.read()


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


class TestSearchWithNumNot10(unittest.TestCase):
    """search() com num != 10 (caminho historicamente pouco testado)."""

    @patch("googlesearch.get_page")
    def test_num_20_returns_20_results(self, mock_get_page):
        mock_get_page.return_value = _load_fixture("google_results.html")
        results = list(search("test query", num=20, stop=5))
        # O fixture tem 3 links válidos (o link do google.com e o relativo são filtrados)
        self.assertEqual(len(results), 3)
        self.assertIn("https://example.com/page1", results)
        self.assertIn("https://example.com/page2", results)
        self.assertIn("https://example.com/page3", results)

    @patch("googlesearch.get_page")
    def test_num_50_uses_num_template(self, mock_get_page):
        mock_get_page.return_value = _load_fixture("google_results.html")
        list(search("test query", num=50, start=0, stop=1))
        # Verifica que a URL construída usa _url_search_num (contém num=50)
        called_url = mock_get_page.call_args[0][0]
        self.assertIn("num=50", called_url)

    @patch("googlesearch.get_page")
    def test_start_10_uses_next_page_template(self, mock_get_page):
        mock_get_page.return_value = _load_fixture("google_results.html")
        list(search("test query", num=10, start=10, stop=1))
        called_url = mock_get_page.call_args[0][0]
        self.assertIn("start=10", called_url)

    @patch("googlesearch.get_page")
    def test_pagination_advances_start(self, mock_get_page):
        mock_get_page.return_value = _load_fixture("google_results.html")
        list(search("test query", num=10, stop=25))
        # Deve ter feito pelo menos 2 páginas (home + primeira de busca)
        self.assertGreaterEqual(mock_get_page.call_count, 2)
        urls = [c[0][0] for c in mock_get_page.call_args_list]
        # Quando start=0 (default), o parâmetro start não é adicionado à URL
        search_urls = [u for u in urls if "/search?" in u]
        self.assertNotIn("start=", search_urls[0])  # start=0 é omitido
        self.assertIn("start=10", search_urls[1])   # start=10 é incluído na segunda página


class TestSearchEdgeCases(unittest.TestCase):
    """Casos extremos: página vazia, challenge do Google, sem container."""

    @patch("googlesearch.get_page")
    def test_empty_results_page(self, mock_get_page):
        mock_get_page.return_value = _load_fixture("google_results_empty.html")
        results = list(search("test query", stop=10))
        self.assertEqual(results, [])

    @patch("googlesearch.get_page")
    def test_challenge_page_no_search_div(self, mock_get_page):
        mock_get_page.return_value = _load_fixture("google_challenge.html")
        # Sem id="search", cai no fallback de gbar/all anchors -> nenhum resultado válido
        results = list(search("test query", stop=10))
        self.assertEqual(results, [])

    @patch("googlesearch.get_page")
    def test_google_links_filtered_by_default(self, mock_get_page):
        mock_get_page.return_value = _load_fixture("google_results.html")
        results = list(search("test query", include_google_links=False, stop=10))
        self.assertNotIn("https://google.com/search", results)

    @patch("googlesearch.get_page")
    def test_google_links_included_when_requested(self, mock_get_page):
        mock_get_page.return_value = _load_fixture("google_results.html")
        results = list(search("test query", include_google_links=True, stop=10))
        self.assertIn("https://google.com/search?q=test", results)


class TestSearchOfflineLucky(unittest.TestCase):
    """lucky() sem dependência de rede (substitui o teste ao vivo)."""

    @patch("googlesearch.get_page")
    def test_lucky_returns_first_result(self, mock_get_page):
        mock_get_page.return_value = _load_fixture("google_results.html")
        result = lucky("test query")
        self.assertEqual(result, "https://example.com/page1")

    @patch("googlesearch.get_page")
    def test_lucky_returns_none_for_empty(self, mock_get_page):
        mock_get_page.return_value = _load_fixture("google_results_empty.html")
        result = lucky("test query")
        self.assertIsNone(result)


class TestCLI(unittest.TestCase):
    """Testes de integração para o CLI (__main__.py).

    O main() lê sys.argv internamente, então fazemos patch de sys.argv
    e de googlesearch.__main__.search para isolar da rede.
    """

    def test_help_exits_zero(self):
        from googlesearch.__main__ import main

        old_argv = sys.argv
        sys.argv = ["google", "--help"]
        try:
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)
        finally:
            sys.argv = old_argv

    @patch("googlesearch.__main__.search")
    def test_cli_prints_results(self, mock_search):
        mock_search.return_value = iter([
            "https://example.com/page1",
            "https://example.com/page2",
        ])
        from googlesearch.__main__ import main
        import io
        import contextlib

        old_argv = sys.argv
        sys.argv = ["google", "--stop=2", "test", "query"]
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                main()
            output = buf.getvalue().strip().splitlines()
            self.assertEqual(output, [
                "https://example.com/page1",
                "https://example.com/page2",
            ])
        finally:
            sys.argv = old_argv

    @patch("googlesearch.__main__.search")
    def test_cli_query_joined_with_spaces(self, mock_search):
        mock_search.return_value = iter([])
        from googlesearch.__main__ import main

        old_argv = sys.argv
        sys.argv = ["google", "opencode", "agents"]
        try:
            main()
        finally:
            sys.argv = old_argv
        # A query deve ser "opencode agents" (unida com espaço)
        called_query = mock_search.call_args[0][0]
        self.assertEqual(called_query, "opencode agents")


class TestCLIArgs(unittest.TestCase):
    """Todos os argumentos do argparse devem chegar corretamente a search()."""

    def _run_main_with_args(self, extra_args):
        """Executa main() com sys.argv alterado, restaurando depois."""
        from googlesearch.__main__ import main

        old_argv = sys.argv
        sys.argv = ["google"] + extra_args
        try:
            main()
        finally:
            sys.argv = old_argv

    @patch("googlesearch.__main__.search")
    def test_default_args(self, mock_search):
        mock_search.return_value = iter([])
        self._run_main_with_args(["query"])
        _, kwargs = mock_search.call_args
        self.assertEqual(kwargs["tld"], "com")
        self.assertEqual(kwargs["lang"], "en")
        self.assertEqual(kwargs["tbs"], "0")
        self.assertEqual(kwargs["safe"], "off")
        self.assertEqual(kwargs["country"], "")
        self.assertEqual(kwargs["num"], 10)
        self.assertEqual(kwargs["start"], 0)
        self.assertIsNone(kwargs["stop"])  # --stop=0 -> None
        self.assertEqual(kwargs["pause"], 2.0)
        self.assertIsNone(kwargs["user_agent"])  # --rua não passado
        self.assertTrue(kwargs["verify_ssl"])
        self.assertFalse(kwargs["include_google_links"])
        self.assertEqual(kwargs["backend"], "auto")

    @patch("googlesearch.__main__.search")
    def test_all_custom_args(self, mock_search):
        mock_search.return_value = iter([])
        self._run_main_with_args([
            "--tld", "co.uk",
            "--lang", "pt",
            "--tbs", "qdr:d",
            "--safe", "on",
            "--country", "BR",
            "--num", "20",
            "--start", "30",
            "--stop", "50",
            "--pause", "1.5",
            "--rua",
            "--insecure",
            "--include",
            "--backend", "playwright",
            "minha",
            "query",
        ])
        _, kwargs = mock_search.call_args
        self.assertEqual(kwargs["tld"], "co.uk")
        self.assertEqual(kwargs["lang"], "pt")
        self.assertEqual(kwargs["tbs"], "qdr:d")
        self.assertEqual(kwargs["safe"], "on")
        self.assertEqual(kwargs["country"], "BR")
        self.assertEqual(kwargs["num"], 20)
        self.assertEqual(kwargs["start"], 30)
        self.assertEqual(kwargs["stop"], 50)
        self.assertEqual(kwargs["pause"], 1.5)
        self.assertIsInstance(kwargs["user_agent"], str)
        self.assertGreater(len(kwargs["user_agent"]), 0)
        self.assertFalse(kwargs["verify_ssl"])
        self.assertTrue(kwargs["include_google_links"])
        self.assertEqual(kwargs["backend"], "playwright")

    @patch("googlesearch.__main__.search")
    @patch("googlesearch.__main__.get_random_user_agent")
    def test_rua_calls_get_random_user_agent(self, mock_rua, mock_search):
        mock_rua.return_value = "UA-Test/1.0"
        mock_search.return_value = iter([])
        self._run_main_with_args(["--rua", "query"])
        _, kwargs = mock_search.call_args
        self.assertEqual(kwargs["user_agent"], "UA-Test/1.0")
        mock_rua.assert_called_once()

    @patch("googlesearch.__main__.search")
    def test_stop_zero_becomes_none(self, mock_search):
        mock_search.return_value = iter([])
        self._run_main_with_args(["--stop=0", "query"])
        _, kwargs = mock_search.call_args
        self.assertIsNone(kwargs["stop"])

    @patch("googlesearch.__main__.search")
    def test_stop_positive_passthrough(self, mock_search):
        mock_search.return_value = iter([])
        self._run_main_with_args(["--stop=10", "query"])
        _, kwargs = mock_search.call_args
        self.assertEqual(kwargs["stop"], 10)

    @patch("googlesearch.__main__.search")
    def test_query_joined_with_spaces(self, mock_search):
        mock_search.return_value = iter([])
        self._run_main_with_args(["opencode", "agents", "test"])
        args, _ = mock_search.call_args
        self.assertEqual(args[0], "opencode agents test")


if __name__ == "__main__":
    unittest.main()
