function load_navbar() {
	document.getElementById("navBar").innerHTML="<nav class='navbar navbar-expand-lg navbar-light bg-light'><a class='navbar-brand' href='#'>LS88 - Sports Analytics</a><button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarSupportedContent' aria-controls='navbarSupportedContent' aria-expanded='false' aria-label='Toggle navigation'><span class='navbar-toggler-icon'></span>
		</button>

		<div class="collapse navbar-collapse" id="navbarSupportedContent">
			<ul class="navbar-nav mr-auto">
				<li class="nav-item">
					<a class="nav-link" href="#">Home</a>
				</li>

				<li class="nav-item">
					<a class="nav-link" href="./policy.html">Policies</a>
				</li>

				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Demos</a>
					<div class="dropdown-menu" aria-labelledby="navbarDropdown">
						<a class="dropdown-item" href="./Demo+-+Pythagorean+Expectation+-+The+Relationship+between+Runs+and+Wins+%2528DS%2529.html">1 - Pythagorean Expectation</a>
						<a class="dropdown-item" href="./Demo+-+Offensive+Metrics+in+Baseball+%2528DS%2529.html">2 - Offensive Metrics in Baseball</a>
						<a class="dropdown-item" href="#">3 - PER</a>
						<a class="dropdown-item" href="#">4 - ESV</a>
						<a class="dropdown-item" href="#">5 - Four Factors</a>
						<a class="dropdown-item" href="#">6 - The Hot Hand</a>
					</div>
				</li>

				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">HW</a>
					<div class="dropdown-menu" aria-labelledby="navbarDropdown">
						<a class="dropdown-item" href="#">1 - Data8 Review</a>
						<a class="dropdown-item" href="#">2</a>
						<a class="dropdown-item" href="#">3 - 4th Down Bot</a>
					</div>
				</li>

				<li class="nav-item">
					<a class="nav-link" href="./lectures.html">Slides</a>
				</li>

				<li class="nav-item">
					<a class="nav-link" href="./project/project.pdf">Project</a>
				</li>

				<li class="nav-item">
					<a class="nav-link disabled" href="#">Solutions</a>
				</li>

			</ul>
		</div>
	</nav>"
}