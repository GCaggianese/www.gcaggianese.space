#!/usr/bin/env sh

find . -type f -name "*.html" -exec sed -i.bak '
/<a class="btn zoombtn" href="{{site\.url}}">/{
N
N
s|<a class="btn zoombtn" href="{{site\.url}}">\n *<i class="fa fa-home"><\/i>\n *<\/a>|{% if site.active_lang == "en" %}\n\n                    <a class="btn zoombtn" href="{{site.url}}">\n                        <i class="fa fa-home"><\/i>\n                    <\/a>\n\n                    {% else %}\n\n                    <a class="btn zoombtn" href="{{site.url}}/{{active_lang}}">\n                        <i class="fa fa-home"><\/i>\n                    <\/a>\n\n                    {% endif %}|
}' {} \;
