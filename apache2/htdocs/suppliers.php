<html>
<head>
<title>Supplier Survey</title>
</head>


<body>

<font color=#E0F8F7 size=6> Supplier Survey </font>

<font color=#E0F8F7 size=3> 

<table width="480" border="0" align="center">
  <tr>
    <td height="627" colspan="2">
      <P>
      <P>
      <FORM action=index.php method=post>
        <H3 align=left><FONT face=arial,helvetica> Your information will be kept completely confidential </FONT></H3>
        Name: 
        <INPUT name=name>
         
        <P>Email: 
          <INPUT name=email>

<P>
<?php echo "1) How did you learn about our online store?"; ?>
<P>
<INPUT TYPE = 'Radio' Name ='q1'  value= 'A' ><?php echo "Friend/Relative"; ?>
<P>
<INPUT TYPE = 'Radio' Name ='q1'  value= 'B' ><?php echo "Web"; ?>
<P>
<INPUT TYPE = 'Radio' Name ='q1'  value= 'C' ><?php echo "Advertisement"; ?>

<P>

<P>
<?php echo "2) What was the MAIN reason you want to be a supplier to BADSTORE?"; ?>
<P>
<INPUT TYPE = 'Checkbox' Name ='q'  value= 'A' ><?php echo "Profit margin"; ?>
<P>
<INPUT TYPE = 'Checkbox' Name ='q'  value= 'B' ><?php echo "Ease of doing business"; ?>
<P>
<INPUT TYPE = 'Checkbox' Name ='q'  value= 'C' ><?php echo "Availability of our product requirements"; ?>

<P>

<P>
<?php echo "3) How easy was it to upload your price lists?"; ?>
<P>
<INPUT TYPE = 'Radio' Name ='q2'  value= 'A' ><?php echo "Somewhat easy"; ?>
<P>
<INPUT TYPE = 'Radio' Name ='q2'  value= 'B' ><?php echo "Easy"; ?>
<P>
<INPUT TYPE = 'Radio' Name ='q2'  value= 'C' ><?php echo "Somewhat difficult"; ?>

<P>

<P>
<?php echo "4) Are you a first time supplier to our site?"; ?>
<P>
<INPUT TYPE = 'Radio' Name ='q4'  value= 'A' ><?php echo "Yes";  ?>
<P>
<INPUT TYPE = 'Radio' Name ='q4'  value= 'B' ><?php echo "No"; ?>

<P>



<P>
<?php echo "5) Overall, how was your business experience with our online store?"; ?>
<P>
<INPUT TYPE = 'Radio' Name ='q5'  value= 'A' ><?php echo "Good"; ?>
<P>
<INPUT TYPE = 'Radio' Name ='q5'  value= 'B' ><?php echo "Average"; ?>
<P>
<INPUT TYPE = 'Radio' Name ='q5'  value= 'C' ><?php echo "Bad"; ?>

<P>

<P>
<?php echo "6) Do you think you will be supplying for our online store again?"; ?>
<P>
<INPUT TYPE = 'Radio' Name ='q6'  value= 'A' ><?php echo "Yes"; ?>
<P>
<INPUT TYPE = 'Radio' Name ='q6'  value= 'B' ><?php echo "No"; ?>

<P>

<INPUT type=submit value="Submit Survey ">
</FORM>
</td>
</tr>
</table>
</font>
<br/>
<?php echo "We thank you for your valuable time spent on the survey"?>
<br/>

</body>
</html>

