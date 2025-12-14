#!/usr/bin/env sh

cd website

cp _config-test.yml _config.yml

bundle exec jekyll serve
