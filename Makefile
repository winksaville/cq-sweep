.DEFAULT_GOAL := help

CADQUERY_DIR := deps/cadquery
CADQUERY_BRANCH := add-viewup-to-vis-show

PYTHON := $(shell which python)
PYTHON_VERSION := $(shell $(PYTHON) -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_OK := $(shell $(PYTHON) -c 'import sys; print(sys.version_info >= (3, 10))')
VENV_ACTIVE := $(shell $(PYTHON) -c 'import sys; print(sys.prefix != sys.base_prefix)')

define usage
	echo "	"; \
	echo "	CadQuery Sweep Makefile"; \
	echo "	------------------------"; \
	echo "	make install     Install local patched CadQuery from deps/cadquery"; \
	echo "	"; \
	echo "	Setup (recommended):"; \
	echo "	   direnv (auto .venv):"; \
	echo "	     echo 'layout python3' > .envrc && direnv allow"; \
	echo "	"; \
	echo "	   OR manually:"; \
	echo "	     python -m venv .venv && source .venv/bin/activate"; \
	echo "	"
endef

.PHONY: help install

help:
	@if [ "$(VENV_ACTIVE)" != "True" ]; then \
		echo "ERR: You are NOT in a virtual environment ($(PYTHON))"; \
		echo "     Install `direnv` Run one of the setup options above before installing."; \
		$(call usage); \
	else \
		echo "OK:  Virtual environment detected!"; \
		if [ "$(PYTHON_OK)" != "True" ]; then \
			echo "     But Python >= 3.10 is required (found $(PYTHON_VERSION)) update Python in venv!"; \
		else \
			echo "     Found $(PYTHON_VERSION) which is 3.10 you are good to go!"; \
		fi \
	fi

install:
	@if [ "$(PYTHON_OK)" != "True" ]; then \
		echo "❌ Python >= 3.10 is required (found $(PYTHON_VERSION))"; \
		exit 1; \
	fi

	@if [ "$(VENV_ACTIVE)" != "True" ]; then \
		echo "❌ Refusing to install into system Python ($(PYTHON))"; \
		echo "   Please activate a virtual environment first."; \
		exit 1; \
	fi

	@if [ ! -d "$(CADQUERY_DIR)" ]; then \
		echo "❌ Directory $(CADQUERY_DIR) not found."; \
		echo "👉 Make sure you've cloned this repo with submodules:"; \
		echo "   git clone --recurse-submodules ..."; \
		exit 1; \
	fi

	@cd "$(CADQUERY_DIR)" && git checkout "$(CADQUERY_BRANCH)"
	pip install -e "$(CADQUERY_DIR)"
	@echo "✅ Installed patched CadQuery from $(CADQUERY_DIR)"
