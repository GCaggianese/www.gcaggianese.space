---
layout: post
title: "歡迎使用 Jekyll"
date: 2024-02-11 00:49:03 +0300
categories: jekyll update
lang: zh_TW
permalink: /welcome-to-jekyll
---

你可以在 `_posts` 目錄中找到這篇文章。編輯它並重新 build site，就能看到變更。Jekyll 有多種 rebuild 方式，最常見的是執行 `jekyll serve`，它會啟動 web server，並在檔案更新時自動重新產生網站。

> 本文翻譯自<a {% static_href %}href="/welcome-to-jekyll"{% endstatic_href %}>英文原文</a>。

Jekyll 要求 blog post 檔名符合以下格式：

`YEAR-MONTH-DAY-title.MARKUP`

其中 `YEAR` 是四位數年份，`MONTH` 和 `DAY` 都是兩位數，`MARKUP` 是檔案格式的副檔名。之後加入必要的 front matter。

Jekyll 也支援 code snippets：

{% highlight ruby %}
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}

更多資訊請看 [Jekyll docs][jekyll-docs]。Bug 和 feature requests 可以提交到 [Jekyll repo][jekyll-gh]。有問題可以到 [Jekyll Talk][jekyll-talk] 詢問。

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/

