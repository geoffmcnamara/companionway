//  gwm added 

// fonts
//<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Architects Daughter">
//<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Tangerine|Open+Sans:300">
//<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Philosopher">
//<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Open+Sans:300italic,300,400,600">
//<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Vollkorn">

// jquery scripting 
 src="//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"

// quick n dirty fade down code - needs jquery
  $(document).ready(function(){
    $('#fadeInDown')
    .css('display', "none")
    .slideDown(1000)
    .animate(
      { opacity: 1 },
      { queue: false, duration: 1000 }
    );
  });

