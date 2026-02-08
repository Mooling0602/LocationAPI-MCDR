#!/bin/sh
make gettext
sphinx-intl update -p build/gettext -l zh_CN
