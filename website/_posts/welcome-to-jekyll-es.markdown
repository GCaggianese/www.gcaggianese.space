---
layout: post
title: "Bienvenido a Jekyll"
date: 2024-02-11 00:49:03 +0300
categories: jekyll update
lang: es
permalink: /welcome-to-jekyll
---

Vas a encontrar esta publicación en tu directorio `_posts`. Podés editarla y reconstruir el sitio para ver los cambios. Se puede reconstruir un sitio Jekyll de varias maneras, pero lo más común es correr `jekyll serve`, que levanta un servidor web y regenera el sitio automáticamente cuando se actualiza un archivo.

> Traducción de <a {% static_href %}href="/welcome-to-jekyll"{% endstatic_href %}>la publicación original en inglés</a>.

Jekyll requiere que los archivos de posts tengan este formato:

`YEAR-MONTH-DAY-title.MARKUP`

Donde `YEAR` es un número de cuatro dígitos, `MONTH` y `DAY` tienen dos dígitos, y `MARKUP` es la extensión que representa el formato del archivo. Después se incluye el front matter necesario.

Jekyll también soporta snippets de código:

{% highlight ruby %}
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}

Revisá la [documentación de Jekyll][jekyll-docs] para más información. Los bugs y feature requests van al [repo de Jekyll][jekyll-gh]. Si tenés preguntas, podés usar [Jekyll Talk][jekyll-talk].

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/

