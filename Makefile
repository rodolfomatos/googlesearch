PREFIX   ?= ~/.local
BINDIR   ?= $(PREFIX)/bin
PACKAGE   = googlesearch
SCRIPTS   = scripts
INSTALLED := $(BINDIR)/google

.PHONY: install install-pip uninstall test test-verbose lint format clean

install: $(INSTALLED)

$(INSTALLED): $(SCRIPTS)/google
	@mkdir -p "$(BINDIR)"
	root=$$(cd "$(SCRIPTS)/.." && pwd); \
	sed "s|%ROOT%|$$root|" "$(SCRIPTS)/google" > "$@"
	chmod +x "$@"
	@echo "Installed google -> $@"
	@echo "Run: $@ --help"

install-pip:
	pip install -e .

uninstall:
	rm -f "$(BINDIR)/google"
	pip uninstall $(PACKAGE) -y 2>/dev/null || true
	@echo "Uninstalled."

test:
	python -m unittest tests.test_search -v

lint:
	python -m ruff check $(PACKAGE)/ tests/

format:
	python -m ruff format $(PACKAGE)/ tests/

clean:
	rm -rf .ruff_cache
	rm -rf $(PACKAGE).egg-info
	rm -rf __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
