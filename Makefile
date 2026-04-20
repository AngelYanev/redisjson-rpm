NAME     := redisjson
VERSION  := $(shell awk '/^Version:/{print $$2}' $(NAME).spec)
RELEASE  := $(shell awk '/^Release:/{print $$2}' $(NAME).spec | sed 's/%{?dist}/.fc43/')
SRPM     := $(NAME)-$(VERSION)-$(RELEASE).src.rpm
MOCK_CFG ?= fedora-43-$(shell uname -m)

.PHONY: download srpm mock copr lint clean help

## Download source tarballs from spec URLs (spectool on Fedora/RHEL)
download:
	spectool -g -C . $(NAME).spec

## Build the SRPM (full vendor tarball; default)
srpm: download
	rpmbuild -bs \
	  --define "_sourcedir $(CURDIR)" \
	  --define "_srcrpmdir $(CURDIR)" \
	  $(NAME).spec

## Rebuild in mock
mock: srpm
	sudo mock -r $(MOCK_CFG) --rebuild $(SRPM)

## Submit SRPM to COPR (adjust project as needed)
copr: srpm
	copr-cli build @redis/redis $(SRPM)

## Run rpmlint on the spec
lint:
	rpmlint $(NAME).spec

## Remove generated artefacts
clean:
	rm -f *.tar.gz *.src.rpm
	rm -rf $(NAME)-*/

## Show this help
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/^## /  /'
