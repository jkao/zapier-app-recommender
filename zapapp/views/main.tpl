<!DOCTYPE html>
<html>

  <head>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta charset="utf-8">
    <title>Zapier App Recommender</title>

    <meta name="description" content="Zapier app recommender">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" type="text/css" href="//cdnjs.cloudflare.com/ajax/libs/960gs/0/960.min.css">
    <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Oswald">
    <link rel="stylesheet" type="text/css" href="static/global-logos.css">
    <link rel="stylesheet" type="text/css" href="static/app.css">

    <!--[if lt IE 9]>
    <script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.2/html5shiv.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>
    <!-- content -->
    <div class="container_12">
      <div class="content container_10 prefix_1 suffix_1">
        <h1 class="hero">Zapier App Recommender</h1>

        <form class="finder" action="/search" method="get">
          <h3>Find me an app to...</h3>
          <input
             type="text"
             name="query"
             placeholder="accept recurring payments"
             autofocus="autofocus"
             autocomplete="off" />
        </form>

        <div class="recommendations">
          <div class="loading">Our gnomes are searching...</div>
          <div class="empty">Oh no! We couldn't find anything 😢</div>
          <div class="body">
            <div class="entries"><!-- entries get populated here --></div>
          </div>

        </div>
      </div>
    </div>

    <!-- entry template -->
    <div class="entry template">
      <a class="link" href="https://zapier.com/zapbook/dropbox" target="_blank">
        <div class="entry-content">
          <div class="grid_2 left">
            <div class="header">Dropbox</div>
            <div class="image"><div class="logo"></div></div>
          </div>
          <div class="grid_6 right">
            <div class="summary">Dropbox lets you store your files online, sync them to all your devices, and share them easily. Get started for free, then upgrade for more space and security features.</div>
          </div>
          <div class="clear"></div>
        </div>
      </a>
    </div>

    <div class="attribution"><a href="https://twitter.com/j_ckao" target="_blank">@j_ckao</a></div>

    <!-- scripts -->
    <script src="//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="/static/app.js"></script>
  </body>

</html>
