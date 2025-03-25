# safenet

This is a basic app that will help verify content filtering and network security settings.

## Overview

This application will attempt to access various sites, systems and networks to determine if your
network settings are behaving as expected.  Targets can be marked as "safe" or "unsafe" in the
config file, which `safenet` will use to determine correctness.

## Websites

Sites are checked using a `HEAD` request.

## Systems

Systems are checked using a simple ping.
