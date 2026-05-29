#!/usr/bin/env python

# Copyright (c) 2009-2024, Mario Vilas
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import random
import time
import ssl
import gzip
import importlib.util
from http.cookiejar import LWPCookieJar
from urllib.request import Request, urlopen
from urllib.parse import quote_plus, urlparse, parse_qs
from bs4 import BeautifulSoup

_PLAYWRIGHT_AVAILABLE = None

__version__ = "3.1.0"

__all__ = [
    "search",
    "lucky",
    "get_random_user_agent",
    "get_tbs",
]

DEBUG = False

_DEFAULT_USER_AGENT = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)"

_url_home = "https://www.google.%(tld)s/"
_url_search = (
    "https://www.google.%(tld)s/search?lr=lang_%(lang)s&"
    "q=%(query)s&btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&"
    "cr=%(country)s&filter=0"
)
_url_next_page = (
    "https://www.google.%(tld)s/search?lr=lang_%(lang)s&"
    "q=%(query)s&start=%(start)d&tbs=%(tbs)s&safe=%(safe)s&"
    "cr=%(country)s&filter=0"
)
_url_search_num = (
    "https://www.google.%(tld)s/search?lr=lang_%(lang)s&"
    "q=%(query)s&num=%(num)d&btnG=Google+Search&tbs=%(tbs)s&"
    "safe=%(safe)s&cr=%(country)s&filter=0"
)
_url_next_page_num = (
    "https://www.google.%(tld)s/search?lr=lang_%(lang)s&"
    "q=%(query)s&num=%(num)d&start=%(start)d&tbs=%(tbs)s&"
    "safe=%(safe)s&cr=%(country)s&filter=0"
)
_url_parameters = ("hl", "q", "num", "btnG", "start", "tbs", "safe", "cr", "filter")


def _load_cookie_jar():
    home_folder = os.getenv("HOME")
    if not home_folder:
        home_folder = os.getenv("USERHOME")
        if not home_folder:
            home_folder = "."
    jar = LWPCookieJar(os.path.join(home_folder, ".google-cookie"))
    try:
        jar.load()
    except (FileNotFoundError, PermissionError):
        pass
    return jar


def _load_user_agents():
    try:
        install_folder = os.path.abspath(os.path.split(__file__)[0])
        user_agents_file = os.path.join(install_folder, "user_agents.txt.gz")
        with gzip.open(user_agents_file, "rt", encoding="utf-8") as fp:
            return [line.strip() for line in fp.readlines()]
    except (FileNotFoundError, PermissionError, OSError):
        return [_DEFAULT_USER_AGENT]


_user_agents_list = None
_cookie_jar = None


def _get_cookie_jar():
    global _cookie_jar
    if _cookie_jar is None:
        _cookie_jar = _load_cookie_jar()
    return _cookie_jar


def _get_user_agents():
    global _user_agents_list
    if _user_agents_list is None:
        _user_agents_list = _load_user_agents()
    return _user_agents_list


def get_random_user_agent():
    return random.choice(_get_user_agents())


def get_tbs(from_date, to_date):
    from_date = from_date.strftime("%m/%d/%Y")
    to_date = to_date.strftime("%m/%d/%Y")
    return "cdr:1,cd_min:%(from_date)s,cd_max:%(to_date)s" % vars()


def get_page(url, user_agent=None, verify_ssl=True):
    if user_agent is None:
        user_agent = _DEFAULT_USER_AGENT
    request = Request(url)
    request.add_header("User-Agent", user_agent)
    jar = _get_cookie_jar()
    jar.add_cookie_header(request)
    if verify_ssl:
        response = urlopen(request)
    else:
        context = ssl._create_unverified_context()
        response = urlopen(request, context=context)
    jar.extract_cookies(response, request)
    html = response.read()
    response.close()
    try:
        jar.save()
    except (PermissionError, OSError):
        pass
    if DEBUG:
        print("-" * 79)
        print(html.decode("utf-8", errors="replace"))
        print("-" * 79)
    return html


def _check_playwright():
    global _PLAYWRIGHT_AVAILABLE
    if _PLAYWRIGHT_AVAILABLE is None:
        _PLAYWRIGHT_AVAILABLE = importlib.util.find_spec("playwright") is not None
    return _PLAYWRIGHT_AVAILABLE


def _fetch_with_playwright(url, user_agent=None):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--window-size=1920,1080",
            ],
        )
        ctx = browser.new_context(
            user_agent=(
                user_agent
                or "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            viewport={"width": 1920, "height": 1080},
        )
        page = ctx.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        """)
        page.goto("https://www.google.com/", wait_until="domcontentloaded")
        page.goto(url, wait_until="domcontentloaded")
        try:
            page.wait_for_selector("#search, #main", timeout=15000)
        except Exception:
            pass
        html = page.content()
        browser.close()
        return html


def filter_result(link, include_google_links=False):
    try:
        if link.startswith("/url?"):
            o = urlparse(link, "http")
            params = parse_qs(o.query)
            if "q" not in params or not params["q"]:
                return None
            link = params["q"][0]

        o = urlparse(link, "http")
        if not o.netloc:
            return None

        if not include_google_links and "google" in o.netloc:
            return None

        return link

    except (ValueError, TypeError, AttributeError):
        return None


def search(
    query,
    tld="com",
    lang="en",
    tbs="0",
    safe="off",
    num=10,
    start=0,
    stop=None,
    pause=2.0,
    country="",
    extra_params=None,
    user_agent=None,
    verify_ssl=True,
    include_google_links=False,
    backend="auto",
):
    seen = set()
    count = 0
    query = quote_plus(query)

    if extra_params is None:
        extra_params = {}

    for builtin_param in _url_parameters:
        if builtin_param in extra_params:
            raise ValueError(
                'GET parameter "%s" is overlapping with '
                "the built-in GET parameter" % builtin_param
            )

    _get_cookie_jar()
    get_page(_url_home % {"tld": tld}, user_agent, verify_ssl)
    current_start = start

    _use_playwright = backend == "playwright"

    while stop is None or count < stop:
        last_count = count

        template_params = dict(
            tld=tld,
            lang=lang,
            query=query,
            tbs=tbs,
            safe=safe,
            country=country,
            start=current_start,
        )

        if current_start:
            if num == 10:
                url = _url_next_page % template_params
            else:
                url = _url_next_page_num % dict(template_params, num=num)
        else:
            if num == 10:
                url = _url_search % template_params
            else:
                url = _url_search_num % dict(template_params, num=num)

        for k, v in extra_params.items():
            url = url + ("&%s=%s" % (quote_plus(k), quote_plus(v)))

        if _use_playwright:
            html = _fetch_with_playwright(url, user_agent)
        else:
            html = get_page(url, user_agent, verify_ssl)

        soup = BeautifulSoup(html, "html.parser")
        search_div = soup.find(id="search")

        if (
            search_div is None
            and backend == "auto"
            and _check_playwright()
            and not _use_playwright
        ):
            _use_playwright = True
            continue

        time.sleep(pause)

        if search_div is not None:
            anchors = search_div.findAll("a")
        else:
            gbar = soup.find(id="gbar")
            if gbar:
                gbar.clear()
            anchors = soup.findAll("a")

        for a in anchors:
            try:
                link = a["href"]
            except KeyError:
                continue

            link = filter_result(link, include_google_links)
            if not link:
                continue

            if link not in seen:
                seen.add(link)
                yield link
                count += 1
                if stop is not None and count >= stop:
                    return

        if last_count == count:
            break

        current_start += num


def lucky(*args, **kwargs):
    try:
        return next(search(*args, **kwargs))
    except StopIteration:
        return None
