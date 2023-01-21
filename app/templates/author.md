
# {{author.name}}
{{author.age}} - {{author.gender}}
{% for paragraph in author.bio.split('\n\n') %}
{{ paragraph }}
{% endfor %}
{% if image %}
![{{ author.photo_description }}](../images/{{ image.id }}.png)

Caption: {{ image.caption }}
{% endif %}

