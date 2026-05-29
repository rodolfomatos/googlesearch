import sys
import argparse
from googlesearch import search, get_random_user_agent


def main():
    parser = argparse.ArgumentParser(
        description="Python script to use the Google search engine\n"
        "By Mario Vilas (mvilas at gmail dot com)\n"
        "https://github.com/MarioVilas/googlesearch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument(
        "--tld",
        metavar="TLD",
        default="com",
        help="Top level domain to use [default: com]",
    )
    parser.add_argument(
        "--lang",
        metavar="LANGUAGE",
        default="en",
        help="Produce results in the given language [default: en]",
    )
    parser.add_argument(
        "--tbs",
        metavar="TBS",
        default="0",
        help="Produce results from period [default: 0]",
    )
    parser.add_argument(
        "--safe", metavar="SAFE", default="off", help="Kids safe search [default: off]"
    )
    parser.add_argument(
        "--country",
        metavar="COUNTRY",
        default="",
        help="Region to restrict search on [default: none]",
    )
    parser.add_argument(
        "--num",
        metavar="N",
        type=int,
        default=10,
        help="Number of results per page [default: 10]",
    )
    parser.add_argument(
        "--start",
        metavar="N",
        type=int,
        default=0,
        help="First result to retrieve [default: 0]",
    )
    parser.add_argument(
        "--stop",
        metavar="N",
        type=int,
        default=0,
        help="Last result to retrieve [default: unlimited]",
    )
    parser.add_argument(
        "--pause",
        metavar="SECONDS",
        type=float,
        default=2.0,
        help="Pause between HTTP requests [default: 2.0]",
    )
    parser.add_argument(
        "--rua",
        action="store_true",
        default=False,
        help="Randomize the User-Agent [default: no]",
    )
    parser.add_argument(
        "--insecure",
        dest="verify_ssl",
        action="store_false",
        default=True,
        help="Disable SSL certificate verification [default: no]",
    )
    parser.add_argument(
        "--include",
        dest="include_google_links",
        action="store_true",
        default=False,
        help="Include links pointing to Google [default: no]",
    )
    parser.add_argument(
        "--backend",
        choices=("auto", "urllib", "playwright"),
        default="auto",
        help="HTTP backend: urllib, playwright, or auto (default: auto)",
    )

    args = parser.parse_args()
    query = " ".join(args.query)

    params = {
        "tld": args.tld,
        "lang": args.lang,
        "tbs": args.tbs,
        "safe": args.safe,
        "country": args.country,
        "num": args.num,
        "start": args.start,
        "stop": args.stop if args.stop else None,
        "pause": args.pause,
        "user_agent": get_random_user_agent() if args.rua else None,
        "verify_ssl": args.verify_ssl,
        "include_google_links": args.include_google_links,
        "backend": args.backend,
    }

    for url in search(query, **params):
        print(url)
        try:
            sys.stdout.flush()
        except OSError:
            pass


if __name__ == "__main__":
    main()
