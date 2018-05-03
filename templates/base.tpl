{%- block header -%}
<!DOCTYPE html>
<html>
  <head>

    {%- block html_head -%}
    <meta charset="utf-8" />

  	{# <title>LS88 - Sports Analytics</title> #}
    <title>{{ title }}</title>

  	<meta name="viewport" content="width=device-width, initial-scale=1.0">
  	<link rel="shortcut icon" type="image/x-icon" href="./assets/img/favicon.ico">
  	
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script>
    <script src="https://cdn.rawgit.com/afeld/bootstrap-toc/v1.0.0/dist/bootstrap-toc.min.js"></script>

    <script src='https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.22.1/moment.min.js'></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/3.9.0/fullcalendar.min.js'></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/3.9.0/gcal.js"></script>

    <script src="./assets/js/config.js"></script>
    <script src="./assets/js/calendar.js"></script>

      <!-- Stylesheets -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.rawgit.com/afeld/bootstrap-toc/v1.0.0/dist/bootstrap-toc.min.css">  
  	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/all.css">
    <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/3.9.0/fullcalendar.min.css' />

  	<link rel="stylesheet" href="./assets/css/style.css">

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