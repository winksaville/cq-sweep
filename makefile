# ========== Config ==========
ENV_NAME = cq-sweep
MIN_PYTHON = 3.10
MAX_PYTHON = 3.13
DEPS_DIR = deps
DEFAULT_LOCAL_CADQUERY = $(DEPS_DIR)/cadquery
LOCAL_CADQUERY ?=

# ========== Check if mamba is installed ==========
ifeq (, $(shell which mamba))
$(error "❌ 'mamba' not found. Please install Mambaforge: https://github.com/conda-forge/miniforge#mambaforge")
endif

# ========== Default target ==========
.DEFAULT_GOAL := help

help:
	@echo ""
	@echo "CadQuery Sweep Environment Setup"
	@echo "--------------------------------"
	@echo "Usage:"
	@echo "  make                  Run full environment check and setup"
	@echo "  make clone-local      Clone CadQuery fork into ./deps/cadquery (or override with LOCAL_CADQUERY=...)"
	@echo "  make install-local    Install local CadQuery into the environment (auto-detects ./deps/cadquery)"
	@echo "  make verify           Check if CadQuery is installed correctly"
	@echo "  make activate         Print command to activate the conda environment"
	@echo "  make clean            Remove the environment"
	@echo ""

all: check-py check-cq create

check-py:
	@echo "Checking Python version..."
	@PYV=$$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'); \
	MIN=$(MIN_PYTHON); MAX=$(MAX_PYTHON); \
	awk -v v="$$PYV" -v min="$$MIN" -v max="$$MAX" 'BEGIN { \
	  split(v, a, "."); \
	  split(min, b, "."); \
	  split(max, c, "."); \
	  if ((a[1]<b[1] || (a[1]==b[1] && a[2]<b[2])) || \
	      (a[1]>c[1] || (a[1]==c[1] && a[2]>=c[2]))) { \
	    print "❌ Python " v " is outside allowed range [" min ", " max ")"; \
	    print "👉 Please install Python >= " min " and < " max; \
	    exit 1; \
	  } \
	  print "✅ Python version " v " is within the allowed range [" min ", " max ")"; \
	}'

check-cq:
	@echo "Checking if cadquery >= 2.6 is available from conda-forge..."
	@OUT=$$(mamba search -c conda-forge cadquery 2>/dev/null | grep -E '2\.6(\.|$$)' || true); \
	if [ -z "$$OUT" ]; then \
		echo "❌ cadquery >= 2.6 is not available on conda-forgey."; \
		echo "  either install:"; \
		echo "    1: 👉 install in $(DEFAULT_LOCAL_CADQUERY):"; \
		echo "       git clone https://github.com/winksaville/cadquery && cd cadquery && git checkout add-viewup-to-vis-show"; \
		echo "       make install-local"; \
		echo ""; \
		echo "    2: 👉 install anywhere else and supply LOCAL_CADQUERY:"; \
		echo "       make install-local LOCAL_CADQUERY=/path/to/your/cadquery"; \
		exit 1; \
	fi

create:
	@echo "Creating environment $(ENV_NAME)..."
	@conda env create -f environment.yml || conda env update -n $(ENV_NAME) -f environment.yml

install-local:
	@echo "Installing local CadQuery..."
	@if [ -z "$(LOCAL_CADQUERY)" ]; then \
		PATH_TO_CQ=$(DEFAULT_LOCAL_CADQUERY); \
	else \
		PATH_TO_CQ=$(LOCAL_CADQUERY); \
	fi; \
	echo "→ Installing from: $$PATH_TO_CQ"; \
	conda run -n $(ENV_NAME) pip install -e "$$PATH_TO_CQ"

verify:
	@echo "Verifying CadQuery installation in $(ENV_NAME)..."
	@conda run -n $(ENV_NAME) python -c "import cadquery; print('✅ CadQuery version:', cadquery.__version__)" || \
	echo "❌ CadQuery not found or import failed."

clone-local:
	@echo "Cloning CadQuery to local directory..."
	@if [ -z "$(LOCAL_CADQUERY)" ]; then \
		DEST=$(DEFAULT_LOCAL_CADQUERY); \
	else \
		DEST=$(LOCAL_CADQUERY); \
	fi; \
	echo "→ Cloning into: $$DEST"; \
	mkdir -p "$$(dirname $$DEST)"; \
	git clone https://github.com/winksaville/cadquery "$$DEST"; \
	cd "$$DEST" && git checkout add-viewup-to-vis-show; \
	echo "✅ Clone complete. To use it:"; \
	echo "   make install-local LOCAL_CADQUERY=$$DEST"

activate:
	@echo "Run: conda activate $(ENV_NAME)"

clean:
	conda remove -n $(ENV_NAME) --all -y
