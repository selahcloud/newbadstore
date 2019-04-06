<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>:::Yoghourt::: A free template</title>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <meta name="author" content="web-kreation.com" />
  <meta name="keywords" content="Open Web Design, OWD, Free Web Template, Yoghourt, Web-Kreation" />
  <meta name="description" content="A free web template designed by Web-Kreation.com and released under the Creative Common Attribution v2.5." />
  <meta name="robots" content="index, follow, noarchive" />
  <meta name="googlebot" content="noarchive" />

  <!--The CSS-->
  <link href="css/stylesheet.css" rel="stylesheet" type="text/css" />

  <link rel="shortcut icon" href="favicon.ico" />


</head>

<body>
    <div id="container">
        <div id="wrapper">
            <div id="sidebar">
                <div id="sb_top">
                    <div class="sb_logo">
                      <!-- The logo - Change it to be your own -->
                      <a href="index.html" title="Home"><img src="images/logo.jpg" alt="Home" border="0" /></a>
                    </div>
                    <!-- ... and now the slogan: -->
                    <p>A free template for your website</p>
                </div>

                <div class="sb_content">

                  <!--##########-->
                  <!-- Start Menu -->
                  <ul id="navlist">
  		  			<li><a href="index.html">Home</a></li>
  		  			<li><a href="about.html">About</a></li>  
  		  			<li><a href="portfolio.html">Portfolio</a></li>
  		  			<li><a class="noborder" href="contact.php">Contact</a></li>
  	  			  </ul> <!-- /Menu -->

                  <h2>&nbsp;</h2>

                  <div class="copyright">
                    <p>&copy; All your copyright information here.</p>
                    <p>Valid <a href="http://validator.w3.org/check?uri=referer" title="validate XHTML">XHTML</a> &amp; <a href="http://jigsaw.w3.org/css-validator" title="validate CSS">CSS</a></p>
                  </div>

                </div> <!-- /sb_content -->
            </div> <!-- /sidebar -->


            <!-- Top -->
            <div id="header">
                   <input name="search" class="search" type="text" value="Search..." />
                   <a href="contact.php" name="Contact"><img src="images/contact.jpg"  alt="Contact" /> Contact</a>
            </div>


            <!-- Start main content -->
            <div id="content">
                <div id="introduction">
                    <h1>Contact Form</h1>
                    <p>Anything you would like to tell me? Don't hesitate to contact me. I will be glad to answer any of your questions.</p>
                </div> <!-- /introduction -->

                <div id="main">
                <p><b>Note:</b> open this page in your favorite web editor and find line 118: <br />
                <code>$to  =  "youremail@domain.com";</code> <br />
                 and change the email address to be yours.</p>

                <p>Please, do not use this contact form to contact me. The email is not valid!!! Instead, go to <a href="http://web-kreation.com/contact.php" title="Contact me">http://web-kreation.com/contact.php</a></p>
<!-- The contact form starts here-->
          <?php
               $error    = ''; // error message
               $name     = ''; // sender's name
               $email    = ''; // sender's email address
               $subject  = ''; // subject
               $message  = ''; // the message itself

          if(isset($_POST['send']))
          {
               $name     = $_POST['name'];
               $email    = $_POST['email'];
               $subject  = $_POST['subject'];
               $message  = $_POST['message'];

              if(trim($name) == '')
              {
                  $error = '<div class="errormsg">Please enter your name!</div>';
              }
          	    else if(trim($email) == '')
              {
                  $error = '<div class="errormsg">Please enter your email address!</div>';
              }
              else if(!isEmail($email))
              {
                  $error = '<div class="errormsg">You have enter an invalid e-mail address. Please, try again!</div>';
              }
          	    if(trim($subject) == '')
              {
                  $error = '<div class="errormsg">Please enter a subject!</div>';
              }
          	else if(trim($message) == '')
              {
                  $error = '<div class="errormsg">Please enter your message!</div>';
              }
              if($error == '')
              {
                  if(get_magic_quotes_gpc())
                  {
                      $message = stripslashes($message);
                  }

                  // the email will be sent here
                  // make sure to change this to be your e-mail
                  $to      = "youremail@domain.com";

                  // the email subject
                  // '[Yoghourt Template Contact Form] :' will appear automatically in the subject.
                  // You can change it as you want

                  $subject = '[Yoghourt Template Contact Form] : ' . $subject;

                  // the mail message ( add any additional information if you want )
                  $msg     = "From : $name \r\ne-Mail : $email \r\nSubject : $subject \r\n\n" . "Message : \r\n$message";

                  mail($to, $subject, $msg, "From: $email\r\nReply-To: $email\r\nReturn-Path: $email\r\n");
          ?>

                <!-- Message sent! (change the text below as you wish)-->
                <center>
                  <h1>Congratulations!!</h1>
                     <p>Thank you <b><?=$name;?></b>, your message is sent! <br />
                     I will get back to you as soon as I possible.</p>
                </center>
                <!--End Message Sent-->


          <?php
              }
          }

          if(!isset($_POST['send']) || $error != '')
          {
          ?>

          <!--Error Message-->
               <?=$error;?>


          <form  method="post" name="contFrm" id="contFrm" onsubmit="return jcap();" action="">


                    <p>Full Name<br />
          			<input name="name" type="text" class="box" id="name" size="60" value="<?=$name;?>" /></p>

          			<p>Email<br />
          			<input name="email" type="text" class="box" id="email" size="60" value="<?=$email;?>" /></p>

          			<p>Subject<br />
          			<input name="subject" type="text" class="box" id="subject" size="60" value="<?=$subject;?>" /></p>

               		<p>Message<br />
               		<textarea name="message" cols="70" rows="6"  id="message"><?=$message;?></textarea><br /><br /></p>




          			<!-- Submit Button-->
               		<input name="send" type="submit" class="button" id="send" value="Send Mail" onclick="return checkForm();" />

          </form>

          <!-- E-mail verification. Do not modify the code below this line -->
          <?php
          }

          function isEmail($email)
          {
              return(preg_match("/^[-_.[:alnum:]]+@((([[:alnum:]]|[[:alnum:]][[:alnum:]-]*[[:alnum:]])\.)+(ad|ae|aero|af|ag|ai|al|am|an|ao|aq|ar|arpa|as|at|au|aw|az|ba|bb|bd|be|bf|bg|bh|bi|biz|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|com|coop|cr|cs|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|edu|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gh|gi|gl|gm|gn|gov|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|in|info|int|io|iq|ir|is|it|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|mg|mh|mil|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|museum|mv|mw|mx|my|mz|na|name|nc|ne|net|nf|ng|ni|nl|no|np|nr|nt|nu|nz|om|org|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|pro|ps|pt|pw|py|qa|re|ro|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)$|(([0-9][0-9]?|[0-1][0-9][0-9]|[2][0-4][0-9]|[2][5][0-5])\.){3}([0-9][0-9]?|[0-1][0-9][0-9]|[2][0-4][0-9]|[2][5][0-5]))$/i"
                      ,$email));
          }
          ?>

                </div> <!-- /main -->

            </div> <!-- /content -->

            <div id="footer">
                <div class="contentfoot">
                    <!-- Back to top button -->
                    <div class="backtotop"><a href="#container" title="Back to top">&nbsp;</a></div>

                    <!-- To use this template free you must keep the link below-->
                    Template design by <a href="http://web-kreation.com">Web-Kreation</a>
                </div> <!-- /contentfoot -->
            </div> <!-- /footer -->


        <br class="endOfSection" />
        </div> <!-- /wrapper -->

    </div> <!-- /container -->       

</body>
</html>