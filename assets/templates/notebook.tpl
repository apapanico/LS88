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
    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>

    <!-- Stylesheets -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/all.css">
    <link rel="stylesheet" href="/LS88/assets/css/style.css">
    <link rel="stylesheet" href="/LS88/assets/css/table.css">
    <link rel="stylesheet" href="/LS88/assets/css/ipy_base.css">
    <link rel="stylesheet" href="/LS88/assets/css/ipy_nb.css">
    <link rel="stylesheet" href="/LS88/assets/css/ipy_tree.css">
    <link rel="stylesheet" href="/LS88/assets/css/ipy_syntax.css">


    <!-- Loading mathjax macro -->
    {{ mathjax() }}
    {%- endblock html_head -%}
  </head>
  {%- endblock header -%}

  {% block body %}
    <body>
      
      <!--Navigation bar-->
      <div id="nav-placeholder"></div>
      <script>
      $(function(){
      $("#nav-placeholder").load("/LS88/nav.html");
      });
      </script>
      <!--end of Navigation bar-->
      
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