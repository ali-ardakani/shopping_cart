<div align="center">
<!-- Title: -->
<h1>Shopping Cart</h1>
<!-- Description: -->
<h3>Simple shopping cart application built with FastAPI.<h3>
</div>
<!-- Table of Contents: -->
<h4>Table of Contents</h4>
<ul>
<li><a href="#about">About</a></li>
<li><a href="#getting-started">Getting Started</a></li>
<li><a href="#usage">Usage</a></li>
</ul>
<!-- About: -->
<h2 id="about">About</h2>
<p>This is a simple shopping cart application built with FastAPI. It uses a SQLite database to store the data and JWT tokens for authentication.</p>
<!-- Getting Started: -->
<h2 id="getting-started">Getting Started</h2>
<p>Follow these steps to get started:</p>
<ol>
<li>Clone the repository</li>
</ol>
<ol start="2">
<li>Change into the project directory</li>
</ol>
<ol start="3">
<li>Install Docker</li>
</ol>
<ol start="4">
<li>Run the following command to run the application:</li>
</ol>
<pre><code>docker-compose up --build -d</code></pre>
<!-- Usage: -->
<h2 id="usage">Usage</h2>
<p>Once the application is running, you can access the API documentation at <a href="http://localhost:8000/docs">http://localhost:8000/docs</a>.</p>
<p>Here is a list of the available endpoints:</p>
<!-- User Endpoints: -->
<li>User Endpoints</li>
<ul>
<li><a href="http://localhost:8000/docs#/user/register">POST /user/register</a></li>
<li><a href="http://localhost:8000/docs#/user/delete">DELETE /user/delete</a></li>
<li><a href="http://localhost:8000/docs#/user/token">POST /user/token</a></li>
<li><a href="http://localhost:8000/docs#/user/logout">POST /user/logout</a></li>
</ul>
<li>Product Endpoints</li>
<ul>
<li><a href="http://localhost:8000/docs#/product/create">POST /product/create</a></li>
<li><a href="http://localhost:8000/docs#/product/delete">DELETE /product/delete</a></li>
<li><a href="http://localhost:8000/docs#/product/update">PUT /product/update</a></li>
<li><a href="http://localhost:8000/docs#/product/info">GET /product/info</a></li>
<li><a href="http://localhost:8000/docs#/product/list">GET /product/list</a></li>
<li><a href="http://localhost:8000/docs#/product/list_active">GET /product/list_active</a></li>
<li><a href="http://localhost:8000/docs#/product/add_to_cart">POST /product/add_to_cart</a></li>
<li><a href="http://localhost:8000/docs#/product/remove_from_cart">POST /product/remove_from_cart</a></li>
<li><a href="http://localhost:8000/docs#/product/shopping_cart">GET /product/shopping_cart</a></li>
<li><a href="http://localhost:8000/docs#/product/shopping_cart_paid">POST /product/shopping_cart_paid</a></li>
</ul>


<!-- Test application: -->
<h2 id="test">Test application</h2>
<p>After the application is running, you can run the tests with the following command:</p>
<pre><code>docker-compose exec app python main.py test</code></pre>
<p>Or you can run the specific tests app with the following command:</p>
<pre><code>docker-compose exec app python main.py test user</code></pre>

<!-- Note: -->
<h4>Note</h4>
<p>For the sake of simplicity, the application is not production ready. It is only meant to be used for learning purposes.</p>
</br>
<li>TODO</li>
<ul>
<li>Implement payment system</li>
<li>Implement product inventory</li>
<li>Implement postgreSQL database <span>(currently using SQLite)</span></li>
