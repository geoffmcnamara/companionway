//  gwm added 

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

// 
//
var request = new XMLHttpRequest();
request.onload = function() {
    // get the file contents
    var fileContent = this.responseText;
    // split into lines
    var fileContentLines = fileContent.split( '\n' );
    // get a random index (line number)
    var randomLineIndex = Math.floor( Math.random() * fileContentLines.length );
    // extract the value
    var randomLine = fileContentLines[ randomLineIndex ];
    
    var splitLine=randomLine.split("-")
    // add the random line in a div
    document.getElementById('linequote').innerHTML = splitLine[0];
    document.getElementById('lineauthor').innerHTML = splitLine[1];
    document.getElementById('random-line').innerHTML = randomLine;
};
//request.open( 'GET', 'http://localhost:1313/lines.dat', true );
request.open( 'GET', '/lines.dat', true );
request.send();
