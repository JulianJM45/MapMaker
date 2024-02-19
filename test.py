import webview

html_content = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="/favicon.ico">
    
    <title>Asynchronous Loading - outdooractive Developers</title>

    <!--[if lt IE 9]>
        <script src="/assets/js/html5shiv.js"></script>
        <script src="/assets/js/respond.min.js"></script>
        <![endif]-->

    <link href="/dist/css/bootstrap.css" rel="stylesheet" />
    <link href="/css/core.css" rel="stylesheet" />
    <link href="/css/syntax.css" rel="stylesheet" />


  </head>

  <body>
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <a title="outdooractive Developers" class="navbar-brand" href="/"><img src="/icons/outdooractive.developers.png" alt="Outdooractive Developers" /></a>
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
        </div>
        <div class="navbar-collapse collapse pull-right">
          <ul class="nav navbar-nav">
            <li><a href="/Overview">Overview</a></li>
            <li><a href="/API-Reference">API Reference</a></li>
            <li class="active"><a href="/Examples">Examples</a></li>
            <li><a href="/Articles">Articles</a></li>
    	<li><a href="/Contact/">Contact</a></li>
          </ul>
        </div>
      </div>
    </div>


    <div class="container">
      <div class="starter-template">
    
        <p>
          <a href="/Examples#Base-Maps"><span class="glyphicon glyphicon-expand" aria-hidden="true"></span> Find more Examples here</a>
    </p>
        <div class="panel panel-primary">
          <div class="panel-heading" style="overflow:hidden">
            <h3 style="float:left;" class="panel-title pull-left">Asynchronous Loading (Map-API)</h3>
            <h2 class="panel-title pull-right">
              <a title="Version reduced to minimal set of HTML" href="/Examples/Map-API/Base-Maps/Map.async.minimal.html">
    	    <img alt="Version reduced to minimal set of HTML" src="/icons/icon_html.png" />
              </a>
              <a title="Read Example Description" href="#description">
    	    <img alt="Read Example Description" src="/icons/icon_description.png" />
              </a>
            </h2>
          </div>
          <div class="panel-body examples-body">
            <div id="map_canvas" style="width: 100%; height: 600px;"></div>
            <script type="text/javascript">
              function initOA() {
                  var map;
                  
                  // call the outdooractive maps api initialization method with a callback function
                  oa.api.maps(
                      function (oamaps, gm) {
                  
                  	// set map center, zoom level, map types and more
                  	var config = {
                              center : { lat: 47.54687, lng: 10.2928 },
                              zoom : 10,
                  
                              mapInit : {
                                  basemap: "osm",
                                  style:   "winter",
                                  overlay: "slope"
                              }
                  
                          };
                  
                  	// instatiate a new outdooractive map
                  	// params: dom id of map canvas div, configuration object
                  	map = oamaps.map( "map_canvas", config );
                  });
              }
            </script>
          </div>
        </div>
    
        <h1 id="description">Description</h1>
        <p>This example is based on the <a href="Map.html">simple map example</a>.
        The only difference is that the outdooractive API is loaded asynchronously after the page is loaded and rendered.
        It helps to improve user experience as the web page is available faster as it&#8217;s not blocked by loading and parsing the APIs.
        The APIs may be loaded asynchronously after page load (like this example does) or even after user interaction (e.g. if the map is opened inside a lightbox or js/css tab).</p>
        
        <div class="highlight"><pre><code class="javascript"><span class="kd">function</span> <span class="nx">initOA</span><span class="p">()</span> <span class="p">{</span>
    <span class="kd">var</span> <span class="nx">map</span><span class="p">;</span>
    
    <span class="c1">// call the outdooractive maps api initialization method with a callback function</span>
    <span class="nx">oa</span><span class="p">.</span><span class="nx">api</span><span class="p">.</span><span class="nx">maps</span><span class="p">(</span>
        <span class="kd">function</span> <span class="p">(</span><span class="nx">oamaps</span><span class="p">,</span> <span class="nx">gm</span><span class="p">)</span> <span class="p">{</span>
    
    	<span class="c1">// set map center, zoom level, map types and more</span>
    	<span class="kd">var</span> <span class="nx">config</span> <span class="o">=</span> <span class="p">{</span>
                <span class="nx">center</span> <span class="o">:</span> <span class="p">{</span> <span class="nx">lat</span><span class="o">:</span> <span class="mf">47.54687</span><span class="p">,</span> <span class="nx">lng</span><span class="o">:</span> <span class="mf">10.2928</span> <span class="p">},</span>
                <span class="nx">zoom</span> <span class="o">:</span> <span class="mi">10</span><span class="p">,</span>
    
                <span class="nx">mapInit</span> <span class="o">:</span> <span class="p">{</span>
                    <span class="nx">basemap</span><span class="o">:</span> <span class="s2">&quot;osm&quot;</span><span class="p">,</span>
                    <span class="nx">style</span><span class="o">:</span>   <span class="s2">&quot;winter&quot;</span><span class="p">,</span>
                    <span class="nx">overlay</span><span class="o">:</span> <span class="s2">&quot;slope&quot;</span>
                <span class="p">}</span>
    
            <span class="p">};</span>
    
    	<span class="c1">// instatiate a new outdooractive map</span>
    	<span class="c1">// params: dom id of map canvas div, configuration object</span>
    	<span class="nx">map</span> <span class="o">=</span> <span class="nx">oamaps</span><span class="p">.</span><span class="nx">map</span><span class="p">(</span> <span class="s2">&quot;map_canvas&quot;</span><span class="p">,</span> <span class="nx">config</span> <span class="p">);</span>
    <span class="p">});</span>
<span class="p">}</span>
</code></pre></div>
        
        <p>The event <code>window.load</code> calls the function <code>loadScripts()</code> that loads the Outdooractive javascript API
        by adding script-tags to the html dom.</p>
        
        <p>The jsonp callback of the outdooractive javascript API script tag&#8217;s url is set to <code>initOA</code>.
        The callback function <code>initOA()</code> calls the the outdooractive maps api initialization method <code>oa.api.maps()</code>
        that receives a function instantiating the final map.</p>
    
    
      </div>
      <footer>
        <div class="row">
          <ul>
            <li><a href="https://www.outdooractive.com">outdooractive.com</a></li>
            <li><a href="/Overview/Guidelines.html#terms-and-conditions" title="Terms and conditions">Terms and conditions</a></li>
            <li><a href="/rss.xml" title="Rss Feed">rss</a></li>
          </ul>
        </div>
      </footer>
    
    </div>


    <!-- load Outdooractive Javascript API -->
    <script type="text/javascript" 
            src="https://api-oa.com/jscr/oa_head.js?proj=api-dev-oa&amp;key=yourtest-outdoora-ctiveapi&amp;lang=en&amp;callback=initOA"></script>


    <script src="https://code.jquery.com/jquery.js"></script>
    <script src="/dist/js/bootstrap.min.js"></script>
    <script>
      (function() {
      var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
      ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
      var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();
      var _gaq = _gaq || [];
      
      _gaq.push(
      ['_setAccount', 'UA-2468980-12'],
      ['_setAllowHash', false],
      ['_gat._anonymizeIp'],
      ['_setDomainName', 'outdooractive.com']
      );
    
      _gaq.push(['_trackPageview']); 
    </script>

  </body>
</html>
"""

webview.create_window("Webview Example", html=html_content, width=800, height=600)
webview.start()