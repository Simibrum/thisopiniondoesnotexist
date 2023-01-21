# {{post.title}}
{% if lead_image %}
![{{ lead_image.caption }}](../images/{{ lead_image.id }}.png)
{% endif %}\
{{ post.day }}-{{ post.month }}-{{ post.year }}\
By [{{ author.name }}](../authors/{{ author.id }}.md)

{{ post.content }}

{% if body_image %}
![{{ body_image.description }}](../images/{{ body_image.id }}.png)
{% endif %}



