{% set nb_title = resources.get('title', '') %}
{% set nb_basename = resources.get('basename', '') %}
{% set home = resources.get('context', {}).get('home', '.') %}


<!DOCTYPE html>
<html>
	<head><meta charset="utf-8" />
	

    <title>{{ nb_title }}</title>

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
	<!-- Load mathjax -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS_HTML"></script>
	<!-- MathJax configuration -->
	<script type="text/x-mathjax-config">
	MathJax.Hub.Config({
	tex2jax: {
	inlineMath: [ ['$','$'], ["\\(","\\)"] ],
	displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
	processEscapes: true,
	processEnvironments: true
	},
	// Center justify equations in code and markdown cells. Elsewhere
	// we use CSS to left justify single line equations in code cells.
	displayAlign: 'center',
	"HTML-CSS": {
	styles: {'.MathJax_Display': {"margin": 0}},
	linebreaks: { automatic: true }
	}
	});
	</script>
	<!-- End of mathjax configuration --></head>
	<body>
		
		<!--Navigation bar-->
		
		<nav class="navbar navbar-expand-lg navbar-light bg-light">
			<a class="navbar-brand" href="{{ home }}/index.html">LS88 - Sports Analytics</a>
			<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
			</button>
			<div class="collapse navbar-collapse" id="navbarSupportedContent">
				<ul class="navbar-nav mr-auto">
					<li class="nav-item">
						<a class="nav-link" href="{{ home }}/syllabus.html">Syllabus</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="{{ home }}/demos.html">Demos</a>
					</li>
					<!-- <li class="nav-item dropdown">
							<a class="nav-link dropdown-toggle" data-toggle="dropdown">HW</a>
							<div class="dropdown-menu">
									<a class="dropdown-item" href="#">Data8 Review</a>
									<a class="dropdown-item" href="#">Baseball Statistics</a>
									<a class="dropdown-item" href="#">4th Down Bot</a>
							</div>
					</li>
					<li class="nav-item">
							<a class="nav-link" href="{{ home }}/lectures.html">Lectures</a>
					</li> -->
				</ul>
			</div>
		</nav>
		<!--end of Navigation bar-->
		
		<div id="bodyContent">
			<div class="container" id="main-container">
				<nav>
					<div class="nav nav-tabs" id="nav-tab" role="tablist">
						<a class="nav-item nav-link active" id="nav-ds-tab" data-toggle="tab" href="#nav-ds" role="tab" aria-controls="nav-ds" aria-selected="true"><pre>datascience</pre></a>
						<a class="nav-item nav-link" id="nav-pd-tab" data-toggle="tab" href="#nav-pd" role="tab" aria-controls="nav-pd" aria-selected="false">Pandas</a>
					</div>
				</nav>
				<div class="tab-content" id="nav-tabContent">
					<div class="tab-pane fade show active" id="nav-ds" role="tabpanel" aria-labelledby="nav-ds-tab">
						<div class="row">
							<div class="col-2">
								<nav id="ds-toc" class="sticky-top"></nav>
							</div>
							<div class="col-10">
								<div tabindex="-1" id="ds-notebook" class="border-box-sizing"  data-spy="scroll">
									<div class="container" id="ds-notebook-container"></div>
								</div>
							</div>
						</div>
					</div>
					<div class="tab-pane fade" id="nav-pd" role="tabpanel" aria-labelledby="nav-pd-tab">
						<div class="row">
							<div class="col-2">
								<nav id="pd-toc" class="sticky-top"></nav>
							</div>
							<div class="col-10">
								<div tabindex="-1" id="pd-notebook" class="border-box-sizing"  data-spy="scroll">
									<div class="container" id="pd-notebook-container"></div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</body>

	<script>
	$('#ds-notebook-container').load('{{ nb_basename }}_(ds).html');
	$('#pd-notebook-container').load('{{ nb_basename }}_(pandas).html');
	</script>

	<script type="text/javascript">
	$(function() {
	var navSelector = '#ds-toc';
	var $myNav = $(navSelector);
	Toc.init({$nav: $('#ds-toc'), $scope: $('#ds-notebook')});
	Toc.init({$nav: $('#pd-toc'), $scope: $('#pd-notebook')});
	});
	</script>
</html>