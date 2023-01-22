---
# This Opinion Does Not Exist
>Manufactured Outrage
---
*Fun times with Generative AI*

## Authors

{% for author in authors %}
* [{{ author.name }}](authors/{{ author.id }}.md)
{% endfor %}

## Posts

{% for post in posts %}
{% if post.title %}
* [{{ post.year }}-{{ post.month }}-{{ post.day }} > {{ post.title }}](posts/{{ post.id }}.md)
{% endif %}
{% endfor %}
