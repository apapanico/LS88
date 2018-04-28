{%- extends 'basic.tpl' -%}
{% from 'mathjax.tpl' import mathjax %}

{%- block header -%}
<!DOCTYPE html>
<html>
  <head>

    {%- block html_head -%}
    <meta charset="utf-8" />

    {% set nb_title = nb.metadata.get('title', '') or resources['metadata']['name'] %}
    {% set home = resources.get('context', {}).get('home', '.') %}

    <title>{{ nb_title }}</title>

    {%- if "widgets" in nb.metadata -%}
    <script src="https://unpkg.com/jupyter-js-widgets@2.0.*/dist/embed.js"></script>
    {%- endif-%}

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script>
    <script src="https://cdn.rawgit.com/afeld/bootstrap-toc/v1.0.0/dist/bootstrap-toc.min.js"></script>

      <!-- Stylesheets -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.rawgit.com/afeld/bootstrap-toc/v1.0.0/dist/bootstrap-toc.min.css">  
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/all.css">
    <link rel="stylesheet" href="{{ home }}/assets/css/style.css">
    <link rel="stylesheet" href="{{ home }}/assets/css/table.css">
    <link rel="stylesheet" href="{{ home }}/assets/css/ipy_base.css">
    <link rel="stylesheet" href="{{ home }}/assets/css/ipy_nb.css">
    <link rel="stylesheet" href="{{ home }}/assets/css/ipy_tree.css">
    <link rel="stylesheet" href="{{ home }}/assets/css/ipy_syntax.css">


    <!-- Loading mathjax macro -->
    {{ mathjax() }}
    {%- endblock html_head -%}
  </head>
  {%- endblock header -%}

  {% block body %}
    <body>
      
      <!--Navigation bar-->
      {% set navbar = resources.get('context', {}).get('navbar', '') %}
      {{ navbar }}
      <!--end of Navigation bar-->
      
      <div id="bodyContent">
        <div class="container" id="main-container">
          <div class="row">
            <div class="col-2">
                <nav id="toc" data-toggle="toc" class="sticky-top"></nav>
            </div>
            <div class="col-10">
              <div tabindex="-1" id="notebook" class="border-box-sizing">
                <div class="container" id="notebook-container" data-spy="scroll" data-target="#toc">
                  {{ super() }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </body>
  {%- endblock body %}

{% block footer %}
  {{ super() }}
</html>
{% endblock footer %}