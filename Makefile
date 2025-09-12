# Makefile for safenet

BASEDIR ?= $(PWD)
SRCDIR ?= $(BASEDIR)
DISTDIR ?= $(BASEDIR)/dist

APPNAME ?= safenet
APPVER ?= 0.3.0

GOOS ?= $(shell go env GOOS)
GOARCH ?= $(shell go env GOARCH)

APPEXE = $(APPNAME)-cli
ifeq ($(GOOS),windows)
	APPEXE = $(APPNAME)-cli.exe
endif


.PHONY: all
all: init preflight build

.PHONY: init
init:
	cd $(SRCDIR) && go mod download
	cd $(SRCDIR) && go mod tidy


.PHONY: build
build: build-exe build-image


.PHONY: build-exe
build-exe: init
	mkdir -p $(DISTDIR)
	cd $(SRCDIR) && \
	CGO_ENABLED=0 GOOS=$(GOOS) GOARCH=$(GOARCH) go build \
		-ldflags "-X main.version=$(APPVER) -s -w" \
		-o $(DISTDIR)/$(APPEXE)


.PHONY: build-image
build-image: init
	docker image build --tag "$(APPNAME):dev" "$(BASEDIR)"


.PHONY: release
release: preflight
	git tag "v$(APPVER)" main
	git push origin "v$(APPVER)"


.PHONY: run
run: init
	cd $(SRCDIR) && go run main.go check


.PHONY: runc
runc: build-image
	docker container run --rm --tty --network=host \
		-v $(BASEDIR)/safenet.yaml:/safenet.yaml \
		"$(APPNAME):dev" check


.PHONY: lint
lint:


.PHONY: style
style:
	cd $(SRCDIR) && go fmt


.PHONY: static-checks
static-checks: style lint


.PHONY: preflight
preflight: static-checks


.PHONY: clean
clean:
	cd $(SRCDIR) && go clean


.PHONY: clobber
clobber: clean
	rm -Rf "$(SRCDIR)/dist"
	cd $(SRCDIR) && go clean -modcache
