ENV_NAME = cq-sweep
PACKAGE = cadquery
RECIPE = deps/cadquery/conda

# Defaults for run target (can override with: make run p="..." t="...")
p ?= [(0,0,0),(10,0,10)]
t ?= [(0,0,1),(0,0,10)]

.PHONY: help setup build install run clean

## Show help
help:
	@echo "make setup                  # Init env, submodule, build, install"
	@echo "make build                  # Rebuild cadquery from deps/"
	@echo "make install                # Reinstall cadquery into env"
	@echo "make run [p=...] [t=...] -- [extra args]   # Run with optional overrides"
	@echo "make clean                  # Remove conda build cache"

## Initialize everything (submodule, environment, cadquery build/install)
setup:
	@echo "****** running setup..."
	@if [ ! -d deps/cadquery/cadquery ]; then \
		echo "Initializing cadquery submodule..."; \
		git submodule update --init; \
	fi
	@if ! micromamba env list | grep -q "^$(ENV_NAME)"; then \
		echo "Creating environment '$(ENV_NAME)'..."; \
		micromamba create -y -n $(ENV_NAME) -f deps/cadquery/environment.yml; \
	else \
		echo "Environment '$(ENV_NAME)' already exists."; \
	fi
	#$(MAKE) build
	#$(MAKE) install

## Build cadquery from local source
build:
	@echo "****** running conda-build..."
	PACKAGE_VERSION=2.6.dev0 GIT_DESCRIBE_TAG=2.6.dev0 GIT_BUILD_STR=0 conda-build $(RECIPE) --output-folder conda-bld

## Install locally built cadquery into environment
install:
	@echo "****** running micromamba install..."
	micromamba install -y -n $(ENV_NAME) -c file://$(PWD)/conda-bld $(PACKAGE)

## Run cq-sweep.py with default or overridden points and tangents
run:
	micromamba run -n $(ENV_NAME) ./cq-sweep.py --pts='$(p)' --tangents='$(t)' $(filter-out $@,$(MAKECMDGOALS))

## Clean local conda build cache
clean:
	rm -rf ~/conda-bld

