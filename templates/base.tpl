{%- block header -%}
<!DOCTYPE html>
<html>
  <head>

    {%- block html_head -%}
    <meta charset="utf-8" />

  	{# <title>LS88 - Sports Analytics</title> #}
    <title>{{ title }}</title>

  	<meta name="viewport" content="width=device-width, initial-scale=1.0">
  	<link rel="shortcut icon" type="image/x-icon" href="{{ home }}/assets/img/favicon.ico">
  	
  	<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
  	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
  	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>

      <!-- Stylesheets -->
  	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
  	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/all.css">
  	<link rel="stylesheet" href="{{ home }}/assets/css/style.css">

    {%- endblock html_head -%}
  </head>
  {%- endblock header -%}

  {% block body %}
    <body>
      
      <!--Navigation bar-->
      {{ navbar }}
      <!--end of Navigation bar-->
      
      <div id="bodyContent">
        <div class="container">
          <section id="content">
            {{ body_content }}
          </section>
        </div>
      </div>

    </body>
  {%- endblock body %}

</html>