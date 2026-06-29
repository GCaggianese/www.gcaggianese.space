![banner](./website/assets/img/banner.png)

# 康青旭 — Personal Website

This site serves as a personal public PKM and way to show off I really do
something.  The content is organized following the PARA method (Projects, Areas,
Resources, Archives). 

- **Posts**: You can see all posts in a disorganized way.
- **Projects**: Ongoing (or finished) projects organized in the categories I'm
  working in.
- **Areas**: Ongoing Areas of my life, studies, blogs, etc. 
- **Resources**: Useful stuff and write-ups.

## Built With

- 🌙 [Moonrise Jekyll Theme](https://github.com/TolgaTatli/Moonrise)
- ☄️ Powered by [Jekyll](https://jekyllrb.com/), written in
  [Emacs](https://www.gnu.org/software/emacs/).

## How This Site Is Structured

The editable site lives in `website/`. Jekyll builds it into static HTML under
`website/_site/`.

The important directories are:

- `website/_config.yml`: main Jekyll configuration.
- `website/_config-web.yml`: production-oriented configuration.
- `website/_config-test.yml`: local/test configuration.
- `website/_posts/`: most content, including regular posts and organizational
  pages.
- `website/_layouts/`: page templates used by the front matter.
- `website/_includes/`: shared Liquid fragments such as navigation, metadata,
  scripts, and social links.
- `website/_data/navigation.yml`: top-level navigation links.
- `website/assets/`: images, CSS entry point, JavaScript, fonts, and other
  static files.
- `website/_sass/`: Sass partials used by `website/assets/css/main.scss`.

This repository intentionally keeps the generated `_site` directory local to the
Jekyll project. Treat source files, configs, layouts, includes, assets, and front
matter as the source of truth.

## Content Model

The site is organized as a personal PKM using the PARA method:

- **Posts**: regular writing, shown together in the posts index.
- **Projects**: ongoing or finished projects.
- **Areas**: ongoing areas of study, life, notes, and practice.
- **Resources**: reusable references, write-ups, and technical notes.

Most content is stored in `website/_posts/`, even when the file is not a normal
blog post. Jekyll still treats these files as posts, but the layouts and front
matter decide how each item appears in the final site.

The main front matter flags are:

```yaml
project: true
area: true
resource: true
resource-programming: true
```

The list layouts iterate through `site.posts` and filter by these flags. For
example, the projects index shows posts with `project: true`; the areas index
shows posts with `area: true`; resources use `resource: true` or more specific
resource flags.

Subcategories can be represented with dedicated layouts and parent pages. For
example, a project category such as Advent of Code can have its own project page
and then link to a list of related posts.

## Languages

Multilingual support is handled by `jekyll-polyglot`.

The configured languages are:

```yaml
languages: ["en", "es", "zh_TW"]
default_lang: "en"
lang_from_path: false
```

The source of truth for a page or post language is the `lang` value in front
matter:

```yaml
lang: en
```

```yaml
lang: es
```

```yaml
lang: zh_TW
```

During the build, Polyglot exposes the active language as `site.active_lang`.
Layouts use that value to show language-specific labels and to filter content:

```liquid
{% if post.lang == site.active_lang %}
```

This means a list page only shows posts whose `lang` matches the currently built
language. For example, the English projects page lists English project posts,
and the Spanish projects page lists Spanish project posts.

The home pages are explicit source files:

- `website/index.markdown`: English home, permalink `/`.
- `website/es/index.markdown`: Spanish home, permalink `/es`.
- `website/zh_TW/index.markdown`: Traditional Chinese home, permalink
  `/zh_TW`.

Translated pages can share the same logical permalink. Polyglot places
non-default language versions under the language prefix during generation.

Existing language behavior should be preserved unless something actually breaks.
Some links are assembled manually in layouts and includes, so changes to
language routing should be made carefully and verified with a Jekyll build.

## Adding Content

For a regular post, add a Markdown file under `website/_posts/` with normal
Jekyll post naming and front matter:

```yaml
---
layout: post
title: "Post title"
lang: en
permalink: /some/path.html
---
```

For a project, area, or resource page, use the appropriate layout and category
flag:

```yaml
---
layout: post
title: "Project write-up"
lang: en
project: true
permalink: /project/example.html
---
```

If a page is an organizational node rather than a regular article, use the
layout that matches that section, such as `project_AoC2025`, `resource_python`,
or another existing specialized layout.

## Local Build

Run Jekyll from inside `website/`:

```bash
bundle exec jekyll build --config _config-test.yml
```

For local serving:

```bash
bundle exec jekyll serve --config _config-test.yml
```

The build may print Sass deprecation warnings from the inherited theme. These
warnings do not currently prevent the site from building.

## REUSE And Licensing

The repository follows the REUSE pattern. License metadata is kept in separate
`.license` files instead of front matter whenever possible. This avoids
conflicts with Jekyll and keeps Markdown front matter focused on site behavior.

When adding a new content file or asset, also add the matching `.license` file.
For example:

```text
website/_posts/example.markdown
website/_posts/example.markdown.license
website/assets/example.png
website/assets/example.png.license
```

## License

- **Source code**: All source code for this website is licensed under the Apache
  License 2.0. You can use, modify, and redistribute it under it's terms. See
  the [full license](https://spdx.org/licenses/Apache-2.0.html) for details.


- **Site content**: Except where otherwise noted, all original content by Germán
  Caggianese (康青旭) is licensed under [Creative Commons Attribution 4.0
  International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). This
  means you can share and adapt the content for any purpose, even commercially,
  as long as you provide attribution.  Third-party content (quotes, citations,
  embedded media) remains under its original license.

- **There are some exceptions**: For more accurate information about licensing,
  please check the individual files.
  
- **REUSE Compliant**: This website, all of it's source code, posts, media, etc.
  is REUSE Compliant. For more information please check [REUSE
  software](https://reuse.software/).
