<html>
<head>
<title>Customer Survey</title>
</head>


<body>

<font color=#E0F8F7 size=6> Customer Survey </font>

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
           
        <P>Which products do you shop online? 
        <P>
        <OL>
          <LI>
            <INPUT type=checkbox value=pepperoni name=topping>
             Electronics
          <LI>
            <INPUT type=checkbox value=sausage name=topping>
             Furniture
          <LI>
            <INPUT type=checkbox value=anchovies name=topping>
             Jewellery</LI>
        </OL>
	Which Credit card(s) do you use for online transactions:
        <P>
            <UL>
              <LI>
                <INPUT type=radio value=mastercard name=paymethod>
                 Mastercard
              <LI>
                <INPUT type=radio value=visa name=paymethod>
                 Visa
              <LI>
                <INPUT type=radio value=americanexpress name=paymethod>
                 American 
    Express</LI>
            </UL>
 How did you learn about our online store?
        <P>
        <DL>
          <DD>
            <INPUT type=radio CHECKED value=yes name=callfirst>
             <I>Yes</I> 
          <DD>
            <INPUT type=radio value=no name=callfirst>
             <I>No</I></DD>
        </DL>
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
