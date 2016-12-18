//I wanted to change the header on the theme for my web site
//to display a slide down and in header.

//The script needed to be a combination of two jquery animations.
 src="//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"

// add id=fadeInDown to a <div> to invloke this.
//```javascript
<script src="//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
    $('#fadeInDown')
    .css('display', "none")
    .slideDown(2000)
    .animate(
      { opacity: 1 },
      { queue: false, duration: 2300 }
      );
    });
</script>
//```

