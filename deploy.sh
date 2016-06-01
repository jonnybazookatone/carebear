#!/bin/bash

# Create DB using postgres as owner -- would not do this if your have an important instance
createdb --username=postgres --host=localhost --port=5433 --owner=postgres carebear
