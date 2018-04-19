{%- extends 'basic.tpl' -%}
{% from 'mathjax.tpl' import mathjax %}

{%- block header -%}
<!DOCTYPE html>
<html>
  <head>
    {%- block html_head -%}
    <meta charset="utf-8" />
    {% set nb_title = nb.metadata.get('title', '') or resources['metadata']['name'] %}
    <title>{{nb_title}}</title>

    {%- if "widgets" in nb.metadata -%}
    <script src="https://unpkg.com/jupyter-js-widgets@2.0.*/dist/embed.js"></script>
    {%- endif-%}

    <script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>

    {{ navbar_head }}

    <!-- Custom stylesheet, it must be in the same directory as the html file -->
    <link rel="stylesheet" href="../../../assets/css/notebook.css">

  <!-- Loading mathjax macro -->
    {{ mathjax() }}
  {%- endblock html_head -%}
  </head>
  {%- endblock header -%}

  {% block body %}

    {{ navbar }}

    <body>
      <div tabindex="-1" id="notebook" class="border-box-sizing">
        <div class="container" id="notebook-container">
    {{ super() }}
        </div>
      </div>
    </body>

  {%- endblock body %}

{% block footer %}
  {{ super() }}
</html>
{% endblock footer %}
