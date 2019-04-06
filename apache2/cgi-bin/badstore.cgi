#!/usr/bin/perl -w

#############################################################################
# BadStore.cgi v1.2.3s
# The CGI program file for BadStore.net
#
# Copyright 2004-6 - Kurt R. Roemer
# Developed and Maintained by:  Kurt R. Roemer, CISSP
# Last Modified:  10 May 2006 - kroemer@netcontinuum.com
# Visit www.badstore.net/downloads for the latest version
#
# WARNING! - This is an insecure program used for demo and
# security training purposes only!  This is not a real store!
# See the Disclaimer for complete information on this program
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#############################################################################

### Specify required PERL modules ###
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use CGI qw(:standard :html4);
use Digest::MD5 qw(md5_hex);
use MIME::Base64;

### Setup Global Variables ###
$time = time;
$ipaddr = $ENV{'REMOTE_ADDR'};

### Get submitted data from URL or FORM ###
$query=new CGI;
$action=$query->param('action');

### Setup Header and Footer ###
#open (BSHEADER, '../data/header.txt') or die "Cannot open footer file\n";
#open (BSHEADER, '../htdocs/BlackSpring/index.html') or die "Cannot open footer file\n";
open (BSHEADER, '../htdocs/yoghourt/badstore_header.html') or die "Cannot open footer file\n";
@header=<BSHEADER>;
close (BSHEADER);
open (BSFOOTER, '../data/footer.txt') or die "Cannot open footer file\n";
@footer=<BSFOOTER>;
close (BSFOOTER);

### Determine action from URL or FORM data ###

if ($action eq 'whatsnew')
{
   &whatsnew;

} elsif ($query->url_param('action') eq 'cartadd') {
   &cartadd;

#} elsif ($action eq 'cartremove') {
#   &cartremove;

#} elsif ($action eq 'cartchangeqty') {
#   &cartqty;

} elsif ($action eq 'cartview') {
   &cartview;

} elsif ($query->url_param('action') eq 'order') {
   &order;

} elsif ($query->url_param('action') eq 'viewprevious') {
   &viewprevious;

} elsif ($query->url_param('action') eq 'submitpayment') {
   &submitpayment;

} elsif ($action eq 'guestbook') {
   &guestbook;

} elsif ($query->url_param('action') eq 'doguestbook') {
   &doguestbook;

} elsif ($action eq 'aboutus') {
   &aboutus;

} elsif ($action eq 'loginregister') {
   &loginregister;

} elsif ($query->url_param('action') eq 'login'){
   &authuser;

} elsif ($query->url_param('action') eq 'register'){
   &authuser;

} elsif ($action eq 'search') {
   &search;

} elsif ($action eq 'supplierlogin') {
   &supplierlogin;

} elsif ($action eq 'supplierproc') {
   &supplierproc;
   
} elsif ($query->url_param('action') eq 'supplierportal') {
   &supplierportal;

} elsif ($query->url_param('action') eq 'supupload') {
   &supupload;

} elsif ($action eq 'admin') {
   &admin;

} elsif ($query->url_param('action') eq 'adminportal') {
   &adminportal;

} elsif ($action eq 'myaccount'){
  &myaccount;

} elsif ($query->url_param('action') eq 'moduser'){
  &moduser;

} elsif ($query->url_param('action') eq 'survey'){
  &survey;

} else {
   &home;
}

exit;


sub start_page {
   my %args = ();
   
   if(@_ == 1) {
	  $args{-title} = shift;
   } else {
	  %args = (@_);
   }
   
   $args{-title} ||= '';
   if($args{-script}) {
	  $args{-script} = "<script type=\"text/javascript\" src=\"" . $args{-script}{-src} . "\"></script>";
   } else {
	  $args{-script} = '';
   }
   
   my $s = qq|
   <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
	  <html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
	  <head>
		<title>$args{-title}</title>
		$args{-script}
		<meta http-equiv="Content-type" content="text/html;charset=utf-8" />
		<link rel="stylesheet" type="text/css" href="/css/global.css" media="all" />
	  </head>
	  <body>|;
   
   return $s . "@header";
}

sub end_page {
   my $s = "@footer" . end_html;
   return $s;
}

############
### Home ###
############

sub home
{
	&printheaders;
	print start_page("Welcome to BadStore.net v1.2.3s - The most insecure store on the 'Net!"),
	h1("<font color=#004b2c>Welcome to BadStore.net!</font>"),
	#p(img({-src=>'/images/store1.jpg',-border=>'0'})),
	p(img({-src=>'/yoghourt/images/store4.jpg',-border=>'0'})),
	end_page();
}

##################
### What's New ###
##################

sub whatsnew
{
	local (@data);
        system ("/usr/bin/wget http://127.0.0.1/cgi-bin/initdbs.cgi");
	### Connect to the SQL Database ###
	my $dbh = DBI->connect("DBI:mysql:database=badstoredb;host=localhost", "root", "",{'RaiseError' => 1})
		or die "Cannot connect: " . $DBI::errstr;

	### Prepare and Execute SQL Query ###
	my $sth = $dbh->prepare( "SELECT itemnum, sdesc, ldesc, price FROM itemdb WHERE isnew = 'Y'")
                or die "Couldn't prepare statement: " . $dbh->errstr;
          $sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;

	&printheaders;
	print start_page("What's New at BadStore.net");
	if ($sth->rows == 0) {
      	print h2("No new items! "),"$sth.\n\n";
      } else {
		print start_form( -action=>'/cgi-bin/badstore.cgi?action=cartadd');
		### Read the matching records and print them out ###
		print h2("The following are new items:"),'<table cellspacing="0" cellpadding="0" class="products">';
		print Tr( th('ItemNum'),th('Item'),th('Description'),th('Price'),th('Image'),th('Select'));



			my $count = 1; 
			print qq| <div id="mylinks"> |;
          		while (@data = $sth->fetchrow_array()) {
			
				$image='/images/' . $data[0] . '.jpg';

				my ($x, $y) = ($data[2] =~ /^(.{17})(.*)/);
				$x .= "...";
				print qq| <div class="link" > 
		  			<div id="prod">
		   			   <img height="135" width="120" id="prod" alt="" src="$image" title="$data[2]"/>
		 			</div>
					<div> $data[1]</div>
					<div> $x </div>
					<div> <b> <font size="2" color="red"> \$$data[3] </font> </b>
					  <INPUT type=checkbox name='cartitem' value=$data[0]> 
					</div>
		  
		    
					</div> |;
				
				$count++;

				#$image='/images/' . $data[0] . '.jpg';
				#print Tr( td( \@data ),td({-align=>CENTER},"<IMG SRC=$image>"),td({-align=>CENTER},"<INPUT type=checkbox name='cartitem' value=$data[0]>") );
			}
			print "</div>"; #mylinks

		print "</table>\n\n", p, "<Center>", submit('Add Items to Cart'), "   ", reset(), "</Center>", end_form;
		}

	### Close statement handles ###
	$sth->finish;

	### Disconnect from the databases ###
	$dbh->disconnect;

	print end_page();
}

##############
### Search ###
##############

sub search
{
	local (@data, $squery, $temp, $sql);
	$squery=$query->param('searchquery');

	### Connect to the SQL Database ###
	my $dbh = DBI->connect("DBI:mysql:database=badstoredb;host=localhost", "root", "",{'RaiseError' => 1})
		or die "Cannot connect: " . $DBI::errstr;

	### Prepare and Execute SQL Query ###
	#$sql="SELECT itemnum, sdesc, ldesc, price FROM itemdb WHERE '$squery' IN (itemnum,sdesc,ldesc)";

	### The below is deliberately included for sqlmap to work! ### Neeraj April 2010
	$sql="SELECT itemnum, sdesc, ldesc, price FROM itemdb WHERE sdesc = '$squery'";

	my $sth = $dbh->prepare($sql)
                or die "Couldn't prepare SQL statement: " . $dbh->errstr;
	$temp=$sth;
      	$sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;


	if ($sth->rows == 0) {
		$sql="SELECT itemnum, sdesc, ldesc, price FROM itemdb WHERE sdesc like '%$squery%' OR ldesc like '%$squery%' or itemnum = '$squery'";
	}
	my $sth = $dbh->prepare($sql)
                or die "Couldn't prepare SQL statement: " . $dbh->errstr;
	$temp=$sth;
      	$sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;



	&printheaders;
	print start_page("BadStore.net - Search Results");
	print comment('Search code developed by Bobby Jones - summer intern, 1996');
	print comment('Comment the $sql line out after troubleshooting is done');

          if ($sth->rows == 0) {
            print h2("No items matched your search criteria: "), $sql, $sth->errstr;
          } else {
	### Read the matching records and print them out ###
	print h2("The following items matched your search criteria:"),
    start_form( -action=>'/cgi-bin/badstore.cgi?action=cartadd'),"<TABLE BORDER=1>",
	Tr( th('ItemNum'),th('Item'),th('Description'),th('Price'),th('Image'),th('Add to Cart'));
          while (@data = $sth->fetchrow_array()) {
		$image='/images/' . $data[0] . '.jpg';
		print Tr( td( \@data ),td({-align=>CENTER},"<IMG SRC=$image>"),td({-align=>CENTER},"<INPUT type=checkbox name='cartitem' value=$data[0]>") );
		}
	print "</TABLE>\n\n", p, "<Center>", submit('Add Items to Cart'), "   ", reset(), "</Center>", end_form;
	}

	### Close statement handles ###
	$sth->finish;

	### Disconnect from the databases ###
	$dbh->disconnect;
	print end_page();
}

#########
# Admin #
#########

sub admin
{
	&printheaders;
	print start_page("Private Administration Portal for BadStore.net"),
	h2("Secret Administration Menu"), p;

	print start_form(-action=>'/cgi-bin/badstore.cgi?action=adminportal'),
	p, h2("Where do you want to be taken today?"),
	popup_menu(-name=>'admin', -values=>['View Sales Reports','Reset User Password','Add User','Delete User','Show Current Users','Troubleshooting','Backup Databases']),
	submit('Do It'), end_form,
	end_page();
}

################
# Admin Portal #
################

sub adminportal
{
	local ($aquery, $email, $newpasswd, @data, $stemp, @s_cookievalue, $passwd, $fullname, $role);
	&printheaders;
	print start_page("Private Administration Portal for BadStore.net"),
	h1("Secret Administration Portal"), p;
	$aquery=$query->param('admin');

	### Read SSOid Cookie ###
	$stemp=cookie('SSOid');
	$stemp=decode_base64($stemp);
	@s_cookievalue=split(":", ("$stemp"));
	$email=shift(@s_cookievalue);
	$passwd=shift(@s_cookievalue);
	$fullname=shift(@s_cookievalue);
	if ($fullname eq '') {
		$fullname="{Unregistered User}";
	}
	$role=shift(@s_cookievalue);

	### Check SSO Cookie for Admin Role ###
	if ($role eq 'A') {

	### Connect to the SQL Database ###
	my $dbh = DBI->connect("DBI:mysql:database=badstoredb;host=localhost", "root", "",{'RaiseError' => 1})
	or die "Cannot connect: " . $DBI::errstr;
	
		### Prepare the Sales Report ###
		if ($aquery eq 'View Sales Reports') {
		my $sth = $dbh->prepare("SELECT * FROM orderdb ORDER BY 'orderdate','ordertime'")
			or die "Couldn't prepare statement: " . $dbh->errstr;
		$sth->execute() or die "Couldn't execute SQL statement: " .$sth->errstr;

		print h2("<Center>BadStore.net Sales Report",p,&getdate,"</center>"), 
		"<TABLE BORDER=1>",
		Tr(th('Date'),th('Time'),th('Cost'),th('Count'),th('Items'),th('Account'),th('IP'),th('Paid'),th('Credit_Card_Used'),th('ExpDate'));
		while (@data=$sth->fetchrow_array()){
			$data[9]=~ s/(\d\d\d\d)[\-\s]?/$1-/g;
			$data[9]=~ s/-$//;
			print Tr(td(font({face=>'Arial', size=>'-2'},$data[1])),td(font({face=>'Arial', size=>'-2'},$data[2])),td(font({face=>'Arial', size=>'-2'},$data[3])),td(font({face=>'Arial', size=>'-2'},$data[4])),td(font({face=>'Arial', size=>'-2'},$data[5])),td(font({face=>'Arial', size=>'-2'},$data[6])),td(font({face=>'Arial', size=>'-2'},$data[7])),td(font({face=>'Arial', size=>'-2'},$data[8])),td(font({face=>'Arial', size=>'-2'},$data[9])),td(font({face=>'Arial',size=>'-2'},$data[10])));
		}
		print "</TABLE>\n\n",p;

		} elsif ($aquery eq 'Reset User Password') {

			### Reset User Password ###
			### Prepare and Execute SQL Query ###
			my $sth = $dbh->prepare( "SELECT email FROM userdb")
	            	    or die "Couldn't prepare statement: " . $dbh->errstr;
		      $sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;
			while (@data=$sth->fetchrow_array()) {
				@ids=(@ids, $data[0]);
			}
			print start_form( -action=>'/cgi-bin/badstore.cgi?action=moduser'),
			p, "Reset password for: ",
			popup_menu(-name=>'email', -values=>[@ids]),
			submit(-name=>'DoMods',-value=>'Reset User Password'), end_form;
	
			### Close statement handles ###
			$sth->finish;

     		} elsif ($aquery eq 'Troubleshooting') {

			### Print CGI Environment ###
			print h2("CGI Environment Variables"), "<TABLE BORDER=1>";

			my %env_info = (
		  	    SERVER_SOFTWARE     => "the server software",
			    SERVER_NAME         => "the server hostname or IP address",
			    GATEWAY_INTERFACE   => "the CGI specification revision",   
			    SERVER_PROTOCOL     => "the server protocol name",
			    SERVER_PORT         => "the port number for the server",
			    REQUEST_METHOD      => "the HTTP request method",
			    PATH_INFO           => "the extra path info",
			    PATH_TRANSLATED     => "the extra path info translated",
			    DOCUMENT_ROOT       => "the server document root directory",
			    SCRIPT_NAME         => "the script name",
			    QUERY_STRING        => "the query string",
			    REMOTE_HOST         => "the hostname of the client",
			    REMOTE_ADDR         => "the IP address of the client",
			    AUTH_TYPE           => "the authentication method",
			    REMOTE_USER         => "the authenticated username",
			    REMOTE_IDENT        => "the remote user is (RFC 931): ",
			    CONTENT_TYPE        => "the media type of the data",
			    CONTENT_LENGTH      => "the length of the request body",
			    HTTP_ACCEPT         => "the media types the client accepts",
			    HTTP_USER_AGENT     => "the browser the client is using",
			    HTTP_REFERER        => "the URL of the referring page",
			    HTTP_COOKIE         => "the cookie(s) the client sent"
			);

			# Add additional variables defined by web server or browser
			foreach $name ( keys %ENV ) {
			    $env_info{$name} = "an extra variable provided by this server"
		        unless exists $env_info{$name};
			}
			print Tr( th('Variable Name'),th('Description'),th('Value'));
			foreach $name ( sort keys %env_info ) {
		    		my $info = $env_info{$name};
		   		my $value = $ENV{$name} || "<I>Not Defined</I>";
				print Tr( td(font({face=>'Arial', size=>'-2'}, $name )),td(font({face=>'Arial', size=>'-2'}, $info )), td(font({face=>'Arial', size=>'-2'}, $value )));
			}
			print "</TABLE>",p,
			h2("Recent Apache Error Log"),p,
			`tail /usr/local/apache2/logs/error_log`,
			p, h2("Apache Access Log"),p,
			`cat /usr/local/apache2/data/userdb`;

			} elsif ($aquery eq 'Add User') {

			### Add a User ###
			print start_form(-method=>'POST',-action=>'/cgi-bin/badstore.cgi?action=moduser'),
			"Email Address:  ",textfield(-name=>'email',-size=>40),p,
			hidden(-name=>'password',-default=>[md5_hex('Welcome')]),
			"Password Hint:  ",popup_menu(-name=>'pwdhint',-values=>['green','blue','red','orange','purple','yellow']),p,			
			"Full Name:  ",textfield(-name=>'fullname',-size=>50),p,
			"Role:  ",textfield(-name=>'role',-size=>1),p,
			submit(-name=>'DoMods',-value=>'Add User'), reset(), end_form,hr;

			} elsif ($aquery eq 'Delete User') {
			### Delete User ###
			### Prepare and Execute SQL Query ###
			my $sth = $dbh->prepare( "SELECT email FROM userdb")
	            	    or die "Couldn't prepare statement: " . $dbh->errstr;
		      $sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;

			while (@data=$sth->fetchrow_array()) {
				@ids=(@ids, $data[0]);
			}

			print start_form(-action=>'/cgi-bin/badstore.cgi?action=moduser'),
			p, "Delete User: ",
			popup_menu(-name=>'email', -values=>[@ids]),
			submit(-name=>'DoMods',-value=>'Delete User'), end_form;
	
			### Close statement handles ###
			$sth->finish;

			} elsif ($aquery eq 'Show Current Users') {

			### Show Current Users ###
			### Prepare and Execute SQL Query ###
			my $sth = $dbh->prepare( "SELECT * FROM userdb")
	            	    or die "Couldn't prepare statement: " . $dbh->errstr;
		      $sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;
			print "<TABLE BORDER=1>",
			Tr(th('Email Address'),th('Password'),th('Pass Hint'),th('Full Name'),th('Role'));	
			while (@data=$sth->fetchrow_array()) {
				print Tr(td(font({face=>'Arial', size=>'-2'},$data[0])),td(font({face=>'Arial', size=>'-2'},$data[1])),td(font({face=>'Arial', size=>'-2'},$data[2])),td(font({face=>'Arial', size=>'-2'},$data[3])),td(font({face=>'Arial', size=>'-2'},$data[4])));
			}
			print "</TABLE>";
			} elsif ($aquery eq 'Backup Databases') {
			### Backup the Tables ###
			my $sth = $dbh->prepare( "SELECT * FROM orderdb INTO OUTFILE '/usr/local/apache2/htdocs/backup/orderdb.bak'")
	            	    or die "Couldn't prepare statement: " . $dbh->errstr;
		      	$sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;
			my $sth = $dbh->prepare( "SELECT * FROM userdb INTO OUTFILE '/usr/local/apache2/htdocs/backup/userdb.bak'")
	            	    or die "Couldn't prepare statement: " . $dbh->errstr;
		      	$sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;
			print h2("Database backup compete - files in www.badstore.net/backup");
			}
		### Disconnect from the databases ###
		$dbh->disconnect;

	} else {
		### Not an Admin user ###
		print h2("Error - $fullname is not an Admin!"),
        "Something weird happened - you tried to access the ",
		"Adminstrative Portal, but you are not an Administrative User.", p,
		"You must login as an Admin to access this resource.", p,
		"Use your browser's Back button and go to Login.", p, p, p,
		h3("(If you're trying to hack - I know who you are:   $ipaddr)");
	}
	print end_page();
}

#############
# Guestbook #
#############

sub guestbook
{
	&printheaders;
	print start_page("BadStore.net - Sign our Guestbook"),
	h2("Sign our Guestbook!"),
	p,
	"Please complete this form to sign our Guestbook.  The email field is not required, but helps us contact you to respond to your feedback.  Thanks!",
	p, "<TABLE BORDER=0 CELLLPADDING=10>";
	print start_form(-method=>'POST', -action=>'/cgi-bin/badstore.cgi?action=doguestbook');
	print Tr( td('Your Name:'), td('<INPUT TYPE=text NAME=name SIZE=30>'));
	print Tr( td('Email:'), td('<INPUT TYPE=text NAME=email SIZE=40>'));
    print Tr( td({-valign=>TOP},'Comments:'), td('<TEXTAREA NAME=comments COLS=60 ROWS=4></TEXTAREA>'));
    print Tr(td(''),td('<input type="submit" value="Add Entry" /> <input type="reset" value="Reset" />'));
	print "</TABLE>\n\n",
	end_form,
	end_page();
}

################
# Do Guestbook #
################

sub doguestbook
{
	local($timestamp, $name, $email, $comments, %fields);
	my ($dataFile) = "/usr/local/apache2/data/guestbookdb";
	
	$timestamp=&getdate;
	$name=$query->param('name');
	$email=$query->param('email');
	$comments=$query->param('comments');
	chomp($comments);

    &saveFormData(\%fields, $dataFile);

	&printheaders;
	print start_page("Welcome to the BadStore.net Guestbook");

    print h1("Guestbook");
    &readFormData($dataFile);
	print end_page();
}

sub saveFormData {
    my($hashRef) = shift;
    my($dbfile) = shift;

    open(FILE, ">>$dbfile") or die("Unable to open Guestbook data file $dbfile: $!\n");
    print FILE ("$hashRef->{'timestamp'}$timestamp~");
    print FILE ("$hashRef->{'name'}$name~");
    print FILE ("$hashRef->{'email'}$email~");
    print FILE ("$hashRef->{'comments'}$comments");
    print FILE ("\n");
    close(FILE);
}

sub readFormData {
    my($dbfile)    = shift;

    open(FILE, "<$dbfile") or die("Unable to open Guestbook data file.");
    while (<FILE>) {
        my($timestamp, $name, $email, $comments) = split(/~/, $_);

        print("$timestamp: <B>$name</B> <A HREF=mailto:$email>$email</A>\n");
        print("<OL><I>$comments</I></OL>\n");
        print("<HR>\n");
    }
    close(FILE);
}

###############################
### Get and format the date ###
###############################

sub getdate
{
   local ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst,$date);
   local (@days, @months);

   @days = ('Sunday','Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday');

   @months = ('January','February','March','April','May','June','July','August','September','October','November','December');

   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($time);

   if ($hour < 10){ $hour = "0$hour"; }
   if ($min < 10){ $min = "0$min"; }
   if ($sec < 10){ $sec = "0$sec"; }

   $year += 1900;
   $date = "$days[$wday], $months[$mon] $mday, $year at $hour\:$min\:$sec";

   return $date;
}

###############
# Add to Cart #
###############

sub cartadd
{
	local($temp, @contents, $cookievalue);

	### Check for existing cookie and setup an empty cart ###
	if ($cartcookie eq "")
		{
		($sessid)=($time);
		$cartitems=0;
		$cartcost=0;
		@contents=$query->param('cartitem');
		}

	chomp(@contents);
	### Check for zero update value ###
	if ($contents[0] eq ""){
		&printheaders;
		print start_page("BadStore.net - Cart Error"), h1("Cart Error - Zero Items"), 
		"Something weird happened - you tried to add no items to the cart!",p,
		"Use your browser's Back button and try again.", p, p, p,
		h3("(If you're trying to hack - I know who you are:   $ipaddr)"),
		end_page();

	} else {
		### Connect to the SQL Database ###
		my $dbh = DBI->connect("DBI:mysql:database=badstoredb;host=localhost", "root", "",{'RaiseError' => 1})
			or die "Cannot connect: " . $DBI::errstr;

		foreach $temp (@contents) {
			$cartitems = $cartitems + 1;
			my $sth = $dbh->prepare( "SELECT price FROM itemdb WHERE itemnum = '$temp'")
            		or die "Couldn't prepare statement: " . $dbh->errstr;
          		$sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;

          		if ($sth->rows == 0) {
            		die "Item number not found: " . $sth->errstr;
          		} else {
			### Update cart cost ###
			$cartcost = $cartcost + $sth->fetchrow_array();
			}
		}

		### Create initial CartID cookie
		$cookievalue=join(":", ($sessid, $cartitems, $cartcost, @contents));
		$cartcookie=cookie( -name=>'CartID', -value=>$cookievalue, -path=>'/');
		print "Set-Cookie: $cartcookie\n";

	&home
	}
}

###############
# Place Order #
###############

sub order
{
	local (@data, $temp, $stemp, @cookievalue, $s_cookievalue, $email, $price, $id, $items, $cost, $cartitems, $cartcookie, $ccard, $expdate, $cardType, $cardholderName);


	### Read SSOid Cookie ###
	$stemp=cookie('SSOid');
	$stemp=decode_base64($stemp);
	@s_cookievalue=split(":", ("$stemp"));
	$email=shift(@s_cookievalue);

	### Read CartID Cookie ###
	$temp=cookie('CartID');
	@cookievalue=split(":", ("$temp"));
	$id=shift(@cookievalue);
	$items=shift(@cookievalue);
	$cost=shift(@cookievalue);
	$price='$' . sprintf("%.2f", $cost);
	$cartitems=join(",", @cookievalue);
	#$email=$query->param('email');

	### Expire the Cookie ###
	$cartcookie=cookie( -name=>'CartID', -value=>'', -expires=>'-1d', -path=>'/');
	print "Set-Cookie: $cartcookie\n";

	### Get the hidden fields ###
	$ccard=$query->param('ccard');
	$expdate=$query->param('expdate');


	
	&printheaders;
	print start_page("BadStore.net - Place Order"),
	h1("Your Order Has Been Placed"), p;

	### Check for Empty Cart ###
	if ($items < "1") {
		print p("You have no items in your cart. Order something already!");
	} else {

		### Connect to the SQL Database ###
		my $dbh = DBI->connect("DBI:mysql:database=badstoredb;host=localhost", "root", "",{'RaiseError' => 1})
			or die "Cannot connect: " . $DBI::errstr;


		if ($query->param('paymentMethod') eq "useExisting") {
			my $sth = $dbh->prepare("SELECT * FROM userdb WHERE email='$email' ");
			eval {
		     		$sth->execute();
				1;
			} or do {
				print "Location: /cgi-bin/badstore.cgi?action=supplierlogin\n\n";
			};

			if ($sth->rows == 0) {
				&printheaders;
				print start_page("BadStore.net - Login Error"),
    		    		h2("UserID and Password not found!"),
				"Use your browser's Back button and try again.",
				end_page();
				exit;
    	 		} else {
				### Login credentials are valid ###
				@data=$sth->fetchrow_array();
				$ccard=$data[5];
				$expdate = $query->param('expdateXX');
			}
			$sth->finish;
		}


	### Add ordered items to Order Database ###
	$dbh->do("INSERT INTO orderdb (sessid, orderdate, ordertime, ordercost, orderitems, itemlist, accountid, ipaddr, cartpaid, ccard, expdate) VALUES ('$id', CURDATE(), CURTIME(), '$price', '$items', '$cartitems', '$email', '$ipaddr', 'Y', '$ccard', '$expdate')")
	or die "Couldn't prepare SQL statement for order: " . $dbh->errstr;

		print p("You have just bought the following:");

		### Prepare and Execute SQL Query ###
		my $sth = $dbh->prepare( "SELECT itemnum, sdesc, ldesc, price FROM itemdb WHERE itemnum IN ($cartitems)")
           		or die "Couldn't prepare statement: " . $dbh->errstr;
     		$sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;
     		if ($sth->rows == 0) {
           		die "Item number not found: " . $sth->errstr;
     		} else {
		### Read the matching records and print them out ###
		print '<table cellspacing="0" cellpadding="0" class="products">',
		Tr( th('ItemNum'),th('Item'),th('Description'),th('Price'),th('Image'));
          	while (@data = $sth->fetchrow_array()) {
			$image='/images/' . $data[0] . '.jpg';
			print Tr( td( \@data ),td({-align=>CENTER},"<IMG SRC=$image>") );
			}
		print "</table>\n\n", p("Purchased: $items items at $price. Thank you for shopping at BadStore.net!");
		}
	### Close statement handles ###
	$sth->finish;


	if (($query->param('paymentMethod') ne "useExisting") && ($query->param('rememberCard') eq 'remember')) {
		$cardType = $query->param('cardType');
		$cardholderName = $query->param('cardholderName');
		my $test_str = "UPDATE userdb SET prefcard = '$ccard', cardtype = '$cardType', expdate = '$expdate', cardholdername = '$cardholderName' WHERE email='$email'";
		my $sth = $dbh->prepare("UPDATE userdb SET prefcard = '$ccard', cardtype = '$cardType', expdate = '$expdate', cardholdername = '$cardholderName' WHERE email='$email'");
     		$sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;
		$sth->finish;

	}

	### Disconnect from the databases ###
	$dbh->disconnect;
	}
	print end_page();
}

##################
# Submit Payment #
##################

sub submitpayment
{
	local($stemp, @s_cookievalue, $email, $passwd, $fullname, $ccard, $expdate);

	### Read SSOid Cookie ###
	$stemp=cookie('SSOid');
	$stemp=decode_base64($stemp);
	@s_cookievalue=split(":", ("$stemp"));
	$email=shift(@s_cookievalue);
        $passwd=shift(@s_cookievalue);
	&printheaders;
	print start_page(-title=>"BadStore.net - Place Order", -script=>{-language=>'JavaScript',-src=>'/cardvrfy.js'}),
	h1("Thanks for ordering from BadStore.net!");

	print start_form( -action=>'/cgi-bin/badstore.cgi?action=order', -onSubmit=>'');

	### If already logged in, fill out email, say Welcome ###
	if ($email eq '') {
	    	print "Email Address: ", textfield(-name=>'email', -size=>15, -maxlength=>40);
	} else {
		print "Welcome, <b>$email</b>",
		hidden(-name=>'email', -default=>[$email]);
	}

	print "<br> <br>";
	### Connect to the SQL Database ###
	my $dbh = DBI->connect("DBI:mysql:database=badstoredb;host=localhost", "root", "",{'RaiseError' => 1})
		or die "Cannot connect: " . $DBI::errstr;

	### Prepare, Evaluate and Execute SQL Query ###
	my $sth = $dbh->prepare("SELECT * FROM userdb WHERE email='$email' AND passwd='$passwd' ");
	eval {
	     	$sth->execute();
		1;
	} or do {
		print "Location: /cgi-bin/badstore.cgi?action=supplierlogin\n\n";
	};

	if ($sth->rows == 0) {
		&printheaders;
		print start_page("BadStore.net - Login Error"),
        	h2("UserID and Password not found!"),
		"Use your browser's Back button and try again.",
		end_page();
		exit;
     	} else {
		### Login credentials are valid ###

		@data=$sth->fetchrow_array();
		$prefcard=$data[5];
		$prefcard_display = substr($prefcard, 12, 4);
	}



	print qq|
		   <table width="90%" cellspacing="5" cellpadding="0" border="0" align="center">
        <tr>
            
            <td colspan="2" > <b> Pay with existing card </b> </td>
            <td> <b> Credit Card No. </b> </td>
            <td> <b> Cardholder's Name </b> </td>
            <td> <b> Expiration Date </b> </td>            
        </tr>
  		|; 

	if (($prefcard ne "-") && ($prefcard ne '')) {
		print qq|
    	    <tr>
            <td width="30" > <input id="0" type="radio" checked="true" value="useExisting" name="paymentMethod" title="select existing card"</td>
            <td> $data[6] </td>
            <td>  ****-$prefcard_display </td>
            <td> $data[8]</td>
            <td> <input type="text" size="4" name="expdateXX" value=$data[7] /> </td>
	    </tr>
		|;

	} else {
		print qq|
		     <tr>
            		<td colspan="5" align="center">
                		<p> No existing card on record </p>
            		</td>
        	     </tr>
		|;
	}

	print qq|
        <tr>
            <td colspan="5">
                <b>Pay with new card</b>
            </td>
        </tr>
        
        <tr>
            <td width="30" > <input id="0" type="radio" checked="false" value="useNew" name="paymentMethod" title="select new card"</td>
            <td>
                <select name="cardType">
                <option value="">Select card type</option>
                <option value="Visa">Visa</option>
                <option value="Master">MasterCard</option>
                <option value="American Express">American Express</option>
                <option value="Discover">Discover</option>
                </select>
            </td>

            <td>  <input type="text" maxlength="16" size="16" name="ccard"/> </td>
            <td> <input type="text" maxlength="16" size="16" name="cardholderName"/> </td>
            <td> <input type="text" size="4" name="expdate"/> </td>
        </tr>

	<tr>
            <td colspan="5">
                <b>Remember Card<input id="0" type="checkbox" value="remember" name="rememberCard" title="Remember card"</b>
            </td>
        </tr>


   </table>
  		|; 


 	print p,
      "<Center>BadStore.net Accepts the following Payment Methods",p,
	img{src=>'/images/visa.jpg'},"        ",img{src=>'/images/mastercard.jpg'},"        ",img{src=>'/images/discover.jpg'},"        ",img{src=>'/images/amex.jpg'},p,
 	submit(-name=>'subccard', -value=>'Place Order'),
	end_form;


#   	print p,
#    	"Credit Card Number: ", textfield(-name=>'ccard', -size=>16, -maxlength=>16),"     Expiration Date: ",textfield(-name=>'expdate',-size=>4),p,p,hr,p,
#      "<Center>BadStore.net Accepts the following Payment Methods",p,
#	img{src=>'/images/visa.jpg'},"        ",img{src=>'/images/mastercard.jpg'},"        ",img{src=>'/images/discover.jpg'},"        ",img{src=>'/images/amex.jpg'},p,
# 	submit(-name=>'subccard', -value=>'Place Order'),
#	end_form;

	print end_page();
}


########################
# View Previous Orders #
########################

sub viewprevious
{
	local ($email, @data, $stemp, @s_cookievalue, $passwd, $fullname, $role);

	### Read SSOid Cookie ###
	$stemp=cookie('SSOid');
	$stemp=decode_base64($stemp);
	@s_cookievalue=split(":", ("$stemp"));
	$email=shift(@s_cookievalue);
	$passwd=shift(@s_cookievalue);
	$fullname=shift(@s_cookievalue);
	$role=shift(@s_cookievalue);


	#if ($fullname eq '{Unregistered User}') {
	if ($fullname eq '') {
		print $query->redirect('/cgi-bin/badstore.cgi?action=loginregister&redirectto=' . $ENV{'REQUEST_URI'});
		print h2('You are not logged in!'), p,
		"Use your browser's Back button and select Login.";
		print $ENV{'REQUEST_URI'};
	} else {
		&printheaders;
		print start_page("BadStore.net - View Previous Orders"),
		h1("You have placed the following orders:"), p;
		### Connect to the SQL Database ###
		my $dbh = DBI->connect("DBI:mysql:database=badstoredb;host=localhost", "root", "",{'RaiseError' => 1})
			or die "Cannot connect: " . $DBI::errstr;

		my $sth = $dbh->prepare( "SELECT orderdate, ordercost, orderitems, itemlist, ccard FROM orderdb WHERE accountid = '$email' ORDER BY orderdate,ordertime")
                or die "Couldn't prepare statement: " . $dbh->errstr;
        	$sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;

     		if ($sth->rows == 0) {
               print p('You have no previous orders!'), p("Use your browser's Back button and select Login.");
     		} else {

		print "<TABLE BORDER=1>",
		Tr( th('Order Date'),th('Order Cost'),th('# Items'),th('Item List'),th('Card Used'));
          	while (@data = $sth->fetchrow_array()) {
			$data[4]=~ s/(\d\d\d\d)[\ \s]?/$1 /g;
			$data[4]=~ s/ $//;			
			print Tr( td( \@data ));
			}
		print "</TABLE>\n\n", p,
		"<Center><i>Thank you for shopping at BadStore.net!</i></Center>";
		}

	### Close statement handles ###
	$sth->finish;

	### Disconnect from the databases ###
	$dbh->disconnect;
	}

	print end_page();
}

############
# About Us #
############

sub aboutus
{
	&printheaders;
	print start_page('BadStore.net - About Us'),
	h2("About Us!"), p,
	img{src=>'/images/seal.jpg', align=>'RIGHT'},
	p, "We value your comments, so click here and tell us what you think!  ", p,
	a({-href=>'mailto:spam@badstore.net'}, 'Send us an email!'), " with subject 'Howdy' and whatever you want to say",
	p,
	"We may be a small site, but we really care about your on-line security.  That's why we undergo a Security Seal certification every few years or so.  The Security Seal is a stringent process where we have to fill out filecabinets full of paperwork to illustrate our security process.  Believe me, it's alot of work.", p,
	end_page();
}

##################
# Supplier Login #
##################

sub supplierlogin
{
	&printheaders;
	
	print start_page('Supplier Portal Login - BadStore.net');
	print "<h2>Welcome Supplier - Please Login</h2>";
	print '<form method="post" action="/cgi-bin/badstore.cgi?action=supplierportal">',
	'<table cellspacing="0" cellpadding="0">',
	  '<tr><td width="100">Email Address:</td><td><input type="text" name="email" size="15" maxlength="40" /></td></tr>',
	  '<tr><td>Password:</td><td><input type="password" name="passwd" size="8" maxlength="8" /></td></tr>',
	  '<tr><td></td><td><input type="submit" value="Login" /></td></tr>',
     '</table>',
    '</form>';
	
	#h1("Welcome Supplier - Please Login:"), hr, p,
	#start_form(-method=>'POST', -action=>'/cgi-bin/badstore.cgi?action=supplierportal'),
	#" Email Address:  ", textfield(-name=>'email', -size=>15, -maxlength=>40), p,
	#" Password:  ", password_field(-name=>'passwd', -size=>8 -maxlength=>8),p,
	#submit("Login"), end_form,
	
	
	print end_page();
}




###################
# Supplier Procedure #
###################
sub supplierproc
{
   &printheaders;
	
   print start_page('Supplier Pricing Upload Procedure - BadStore.net');
   print "<h2>Supplier Pricing Upload Procedure</h2>";
   
   print q|
   <p>To save our administrative staff some work, we have implemented a page where you, our Valued Suppliers, can upload your new pricelist.  This lets you manage your product descriptions and pricing without us having to do anything.  We hope that you will like this procedure as much as we like it.</p>
   <p>It was really an easy, quick little application for us to develop.  It only took an hour, in fact.</p>

   <h3>Here's how it works:</h3>
   <p>When you successfully LOGIN to the Supplier Portal (See the "Supplier Login" link on the main page), You will be presented with a form where you fill in the file you want to upload (from your PC) and the name you want it stored under on the site.  It's as simple as that.</p>
   <p>We recommend that your description file be an html file (AcmeWidget.html), and if you want your corporate logo, do another upload for it, too!</p>
   <p>Thanks for being a valued supplier and thanks for using this portal that saves us work!</p>
   <p>- Your BadStore.net management team</p>
	|;

   print end_page();
}

###################
# Supplier Portal #
###################

sub supplierportal
{
	local($email, $passwd);
	$email=$query->param('email');
	$passwd=$query->param('passwd');
	chomp($email);
	chomp($passwd);
	$passwd=md5_hex($passwd);

	### Connect to the SQL Database ###
	my $dbh = DBI->connect("DBI:mysql:database=badstoredb;host=localhost", "root", "",{'RaiseError' => 1})
		or die "Cannot connect: " . $DBI::errstr;

	### Prepare, Evaluate and Execute SQL Query ###
	my $sth = $dbh->prepare("SELECT * FROM userdb WHERE email='$email' AND passwd='$passwd' ");
	eval {
	     	$sth->execute();
		1;
	} or do {
		print "Location: /cgi-bin/badstore.cgi?action=supplierlogin\n\n";
	};

	&printheaders;
	print start_page("Welcome to the BadStore.net Supplier Portal"),
	h1("Welcome Supplier");
     	
	if ($sth->rows == 0) {
           		print p("UserID and Password not found! Use your browser's Back button and try again."),
     	} else {
		# Login credentials are valid
		print h2("Upload Price Lists"), h3("Filename on local system: "),
   		start_multipart_form(-method=>'POST', -action=>'/cgi-bin/badstore.cgi?action=supupload', -enctype=>'multipart/form-data'),
    		filefield(-name=>'uploaded_file', -size=>50, -maxlength=>80), br, br,
		h3("Filename on BadStore.net: "), textfield(-name=>'newfilename', size=>25, -maxlength=>50),
  		submit('Upload'), end_form;

	        print hr, p, h2("View Pricing File on BadStore.net: "),
                start_multipart_form(-method=>'POST', -action=>'/cgi-bin/badstore.cgi?action=supupload', -enctype=>'multipart/form-data'),
                h3("Pricing file to View on BadStore.net: "), textfield(-name=>'viewfilename', size=>25, -maxlength=>50), "&nbsp",
                submit('View'), end_form, "<font face=Arial size=2><i>( For security purposes, a list of files on the server is not displayed. Please use your assigned naming convention to view your company's pricing file. )</i></font>"; 

	}

	print p("<strong>Coming Soon - Web Services!</strong>");
	### Close statement handles ###
	$sth->finish;

	### Disconnect from the databases ###
	$dbh->disconnect;
	print end_page();
}

###################
# Supplier Upload #
###################

sub supupload
{
	(local $host);
	&printheaders;
	print start_page("BadStore.net - Supplier Upload");

	$referer  = $ENV{HTTP_REFERER};
	$host = $ENV{HTTP_HOST};

	### Check for valid referer from Supplier Portal
	if ($referer and $referer !~ m|^http://$hostname/| ) {

                $aquery=$query->param('uploaded_file');
                if ($aquery eq "") {
                	print h1("View a pricing file");
                	$viewfilename = $query->param('viewfilename');
                	open (FILE, "../data/uploads/$viewfilename") or die "Can't open $viewfilename for viewing: $!\n";
               		while (<FILE>) {
                       		print;
                	}
                	close (FILE);
                	print p, h2("Thanks for viewing your pricing file!"), p;
        	} else {
                	print h1("Upload a pricing file");

			$newfilename = $query->param('newfilename');
			$filename = $query->param('uploaded_file'); 
			$filename =~ s/.*[\/\\](.*)/$1/;
			chomp($filename); 
			$upload_filehandle = $query->upload('uploaded_file'); 
			open (OUT, ">../data/uploads/$newfilename") or die "Can't open $newfilename for appending: $!\n";
			while (<$upload_filehandle>) 
			{ 
				print OUT;
			}
			close OUT; 
			print p, h2("Thanks for uploading your new pricing file!"), p, 
			h3("Your file has been uploaded: $newfilename"), p,
		}
	} else {
		### Invalid referer ###
		print h1("An Error Has Occurred"),
		h3("Uploads are only accepted by authenticating to the Supplier Portal!")
	}
	end_page();
}

######################
# View Cart Contents #
######################

sub cartview
{
	local (@data, $temp, @cookievalue, $price, $id, $items, $cost, $cartitems);

	&printheaders;
	print start_page("BadStore.net - View Cart Contents"),
	h1("Keep Shopping!"), p;

	### Read CartID Cookie ###
	$temp=cookie('CartID');
	@cookievalue=split(":", ("$temp"));
	$id=shift(@cookievalue);
	$items=shift(@cookievalue);
	$cost=shift(@cookievalue);
	$price='$' . sprintf("%.2f", $cost);
	$cartitems=join(",", @cookievalue);

	### Check for Empty Cart ###
	if ($items < "1") {
		print p("You have no items in your cart. Order something already!");
	} else {
		### Connect to the SQL Database ###
		my $dbh = DBI->connect("DBI:mysql:database=badstoredb;host=localhost", "root", "",{'RaiseError' => 1})
			or die "Cannot connect: " . $DBI::errstr;

         print p("Cart Contains: $items items at $price. The following items are in your cart:");

		### Prepare and Execute SQL Query ###
		my $sth = $dbh->prepare( "SELECT itemnum, sdesc, ldesc, price FROM itemdb WHERE itemnum IN ($cartitems)")
           		or die "Couldn't prepare statement: " . $dbh->errstr;
     		$sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;
     		if ($sth->rows == 0) {
           		die "Item number not found: " . $sth->errstr;
     		} else {
		### Read the matching records and print them out ###
		print start_form( -action=>'/cgi-bin/badstore.cgi?action=submitpayment'),'<table cellspacing="0" cellpadding="0" class="products">',
		Tr( th('ItemNum'),th('Item'),th('Description'),th('Price'),th('Image'),th('Order'));
          	while (@data = $sth->fetchrow_array()) {
			$image='/images/' . $data[0] . '.jpg';
			print Tr( td( \@data ),td({-align=>CENTER},"<IMG SRC=$image>"),td({-align=>CENTER},"<input type=checkbox checked name='cartitem' value=$data[0]>") );
			}
		print "</table>\n\n", p, "<Center>", submit('Place Order'), "   ", reset(), "</Center>", end_form;
		}
	### Close statement handles ###
	$sth->finish;

	### Disconnect from the databases ###
	$dbh->disconnect;
	}
	print end_page();
}

#####################
### Print headers ###
#####################

sub printheaders
{
	print "Content-type: text/html\n";
	print "Server: Apache/1.3.20 Sun Cobalt (Unix) mod_ssl/2.8.4 OpenSSL/0.9.6b PHP/4.0.6 mod_auth_pam_external/0.1 FrontPage/4.0.4.3 mod_perl/1.25\n";
	print "ETag: CPE1704TKS\n";
	print "Cache-Control: no-cache\n";
	print "Pragma: no-cache\n\n";
}

#####################
# Login or Register #
#####################

sub loginregister
{
   &printheaders;
   print start_page('BadStore.net - Register/Login');
   $redirectpage = $query->param('redirectto');

	open (MYFILE, '>>/tmp/data.txt');
	print MYFILE "redirectto 1 = ";
	print MYFILE $redirectpage;

    	chomp($redirectpage);

	print MYFILE "redirectto 2 = ";
	print MYFILE $redirectpage;
	close (MYFILE);

   print qq|
   <h2>Login to Your Account or Register for a New Account</h2>
   <h3>Login to Your Account</h3>
   <form method="post" action=/cgi-bin/badstore.cgi?action=login&redirectto=$redirectpage>
     <table cellspacing="0" cellpadding="0">
       <tr>
         <td width="100">Email Address:</td>
         <td><input type="text" name="email" size="20" maxlength="40" /></td>
       </tr>
       <tr>
         <td>Password:</td>
         <td><input type="password" name="passwd" size="8" maxlength="8" /></td>
       </tr>
       <tr>
         <td></td>
         <td><input type="submit" value="Login" /></td>
       </tr>
      </table>
   </form>
   <hr />
   <h3>Register for a New Account</h3>
   <form method="post" action="/cgi-bin/badstore.cgi?action=register">
     <table cellspacing="0" cellpadding="0">
       <tr>
         <td width="100">Full Name:</td>
         <td><input type="text" name="fullname" size="25" maxlength="40" /></td>
       </tr>
       <tr>
         <td>Email Address:</td>
         <td><input type="text" name="email" size="20" maxlength="40" /></td>
       </tr>
       <tr>
         <td>Password:</td>
         <td><input type="password" name="passwd" size="8" maxlength="8" /></td>
       </tr>
       <tr>
         <td>Password Hint:</td>
         <td>
           What's Your Favorite Color?:
           <select name="pwdhint">
             <option value="green">Green</option>
             <option value="blue">Blue</option>
             <option value="red">Red</option>
             <option value="orange">Orange</option>
             <option value="purple">Purple</option>
             <option value="yellow">Yellow</option>
           </select>
           <br />
           <em>(The Password Hint is used as a security measure to help recover a forgotten password.  You will need both your email address and this hint to access your account if you forget your current password.)</em>
         </td>
       </tr>
       <tr>
         <td></td>
         <td>
            <input type="hidden" name="role" value="U" />
            <input type="submit" value="Register" />
         </td>
       </tr>
      </table>
   </form>
   |;
   
   print end_page();
   #&printheaders;
   #print start_page('BadStore.net - Register/Login'),
   #h2("Login to Your Account or Register for a New Account"), hr,
   #h3("Login to Your Account"),
   #start_form(-method=>'POST', -action=>'/cgi-bin/badstore.cgi?action=login'),
   #p,"Email Address:  ", textfield(-name=>'email', -size=>20, -maxlength=>40), p,
   #p,"Password:  ", password_field(-name=>'passwd', -size=>8 -maxlength=>8),p,
   #submit("Login"), end_form, hr,
   #h3("Register for a New Account"),
   #start_form(-method=>'POST', -action=>'/cgi-bin/badstore.cgi?action=register'),
   #p,"Full Name:  ", textfield(-name=>'fullname', -size=>25, -maxlength=>40), p,
   #p,"Email Address:  ", textfield(-name=>'email', -size=>20, -maxlength=>40), p,
   #p,"Password:  ", password_field(-name=>'passwd', -size=>8 -maxlength=>8),p,
   #"Password Hint - What's Your Favorite Color?:  ",popup_menu(-name=>'pwdhint',-values=>['green','blue','red','orange','purple','yellow']),p,
   #"<font face=Arial size=2><i>(The Password Hint is used as a security measure to help recover a forgotten password.  You will need both your email address and this hint to access your account if you forget your current password.)</i></font>",p,
   #hidden(-name=>'role', -default=>['U']),
   #submit("Register"), end_form, p,
   #end_page();
}

##############
# My Account #
##############

sub myaccount
{
	local($aquery, $email, $passwd, $pwdhint, $fullname, $role, $newpasswd, $vnewpasswd, $encpasswd);
 
	### Read SSOid Cookie ###
	$stemp=cookie('SSOid');
	$stemp=decode_base64($stemp);
	@s_cookievalue=split(":", ("$stemp"));
	$email=shift(@s_cookievalue);
	$passwd=shift(@s_cookievalue);
	$fullname=shift(@s_cookievalue);
	$role=shift(@s_cookievalue);

	&printheaders;
	print start_page(-title=>'BadStore.net - My Account Services',-script=>{language=>'JavaScript',-src=>'/frmvrfy.js'});

	if ($fullname eq '') {
		$fullname="{Unregistered User}";
		print h2(' Welcome, as an ',$fullname,' you can:'),p,
		"Login To Your Account / Register for A New Account - <A HREF='/cgi-bin/badstore.cgi?action=loginregister'>Click Here</A><BR>", p,
		" Reset A Forgotten Password", p,
		start_form(-method=>'POST', -action=>'/cgi-bin/badstore.cgi?action=moduser'),
		"<font face=Arial size=2> Please enter the email addess and password hint you chose when the account was created:</font>",p,
		" Email Address:  ", textfield(-name=>'email', -size=>15),p,
		" Password Hint - What's Your Favorite Color?:  ",popup_menu(-name=>'pwdhint',-values=>['green','blue','red','orange','purple','yellow']),p,
		"<font face=Arial size=2><i> (The Password Hint was chosen when you registered for a new account as a security measure to help recover a forgotten password...)</i></font>",p,
		submit(-name=>'DoMods',-value=>'Reset User Password'), end_form;

	} else {
		print h2("Welcome, ",$fullname),
		"<h5>Update your account information:</h5>",
		start_form(-method=>'POST', -action=>'/cgi-bin/badstore.cgi?action=moduser', -onSubmit=>'return DoPwdvrfy(this);'),
		" Current Full Name:  ", $fullname,p,
		" New Full Name =  ",textfield(-name=>'fullname', -size=>25, -maxlength=>40),p,br,
		" Current Email Address:  ", $email,p,
		" New Email Address =  ",textfield(-name=>'newemail', -size=>20, -maxlength=>40),p,br,
		" Change Password:  ", password_field(-name=>'newpasswd', -size=>8 -maxlength=>8),"  Verify:  ", password_field(-name=>'vnewpasswd', -size=>8 -maxlength=>8),p,br,
		hidden(-name=>'role', -default=>[$role]),
		hidden(-name=>'email',-default=>[$email]),
		submit(-name=>'DoMods',-value=>'Change Account'), end_form, p;
	}
	print end_page();
}

sub survey
{

	# Not implemented in Perl here
	# Used for demo'ing RFI attacks - see the PHP code
}


##########################
# Modify User Attributes #
##########################

sub moduser
{
	local($aquery, $email, $passwd, $pwdhint, $fullname, $role, $newpasswd, $encpasswd, $vnewpasswd, $newemail);
	$aquery=$query->param('DoMods');
	$email=$query->param('email');
	$passwd=$query->param('passwd');
	$pwdhint=$query->param('pwdhint');
	$fullname=$query->param('fullname');
	$role=$query->param('role');
	$vnewpasswd=$query->param('vnewpasswd');
	$newemail=$query->param('newemail');
	chomp($email);
	chomp($passwd);
	chomp($pwdhint);
	chomp($fullname);
	chomp($role);
	$newpasswd="Welcome";
	$encpasswd=md5_hex($newpasswd);
	$vencpasswd=md5_hex($vnewpasswd);
	&printheaders;

	### Connect to the SQL Database ###
	my $dbh = DBI->connect("DBI:mysql:database=badstoredb;host=localhost", "root", "",{'RaiseError' => 1})
		or die "Cannot connect: " . $DBI::errstr;

	### Reset User Password ###
	if ($aquery eq 'Reset User Password') {
		print start_page('BadStore.net - Reset Password for User');
		### Prepare and Execute SQL Query ###
		my $sth=$dbh->prepare("UPDATE userdb SET passwd = '$encpasswd' WHERE email='$email'")
			or die "Could not update password: ".$dbh->errstr;
		$sth->execute() or die "Couldn't execute SQL statement: ".$sth->errstr;
	
		print h2('The password for user:  ', $email,p, ' ...has been reset to: ',$newpasswd),

	}elsif ($aquery eq 'Add User'){
		print start_page('BadStore.net - Add User');
		$dbh->do("INSERT INTO userdb (email, passwd, pwdhint, fullname, role) VALUES ('$email','$encpasswd','$pwdhint', '$fullname', '$role')")
			or die "Couldn't prepare SQL statement for Registration: " . $dbh->errstr;
		print h2("User:  ",$fullname," has been added.");

	}elsif ($aquery eq 'Delete User'){
		print start_page('BadStore.net - Delete User');
		$dbh->do("DELETE FROM userdb WHERE email='$email'")
			or die "Couldn't prepare SQL statement for Registration: " . $dbh->errstr;
		print h2("User:  ",$email," has been deleted.");

	### Change Account Information ###
	}elsif ($aquery eq 'Change Account'){
		print start_page('BadStore.net - Update User Information');
		$dbh->do("UPDATE userdb SET fullname='$fullname' WHERE email='$email'")
			or die "Couldn't prepare SQL statement: " .$dbh->errstr;
		$dbh->do("UPDATE userdb SET passwd='$vencpasswd' WHERE email='$email'")
			or die "Couldn't prepare SQL statement: " .$dbh->errstr;
		$dbh->do("UPDATE userdb SET email='$newemail' WHERE email='$email'")
			or die "Couldn't prepare SQL statement: " .$dbh->errstr;
		print h2(" Account Information for: "),
		" Full Name: ",$fullname,p," Email: ",$newemail,p," Password: ",$vnewpasswd,p,
		h3(" Has been updated!");
	}
	print end_page();

	### Disconnect from the databases ###
	$dbh->disconnect;
}

#############
# Auth User #
#############

sub authuser
{
	local(@data, $email, $passwd, $pwdhint,$fullname, $role, $redirecturl);
	$email=$query->param('email');
	$passwd=$query->param('passwd');
	$pwdhint=$query->param('pwdhint');
	$redirecturl=$query->param('redirectto');
	$fullname=$query->param('fullname');
	$role=$query->param('role');
	chomp($email);
	chomp($passwd);
	chomp($pwdhint);
	chomp($fullname);
	chomp($role);
	chomp($redirecturl);
	$passwd=md5_hex($passwd);

	open (MYFILE, '>>/tmp/data.txt');
	print MYFILE "redirectto = ";
	print MYFILE $redirecturl;
	close (MYFILE);


	### Connect to the SQL Database ###
	my $dbh = DBI->connect("DBI:mysql:database=badstoredb;host=localhost", "root", "",{'RaiseError' => 1})
		or die "Cannot connect: " . $DBI::errstr;

	### Logging into existing account ###
	if ($query->url_param('action') eq 'login') {

		### Prepare and Execute SQL Query to Verify Credentials ###
		my $sth = $dbh->prepare("SELECT * FROM userdb WHERE email='$email' AND passwd='$passwd'")
      		or die "Couldn't prepare statement: " . $dbh->errstr;
     		$sth->execute() or die "Couldn't execute SQL statement: " . $sth->errstr;

		if ($sth->rows == 0) {
			&printheaders;
			print start_page("BadStore.net - Login Error"),
           		h2("UserID and Password not found!"),
			"Use your browser's Back button and try again.",
			end_page();
			exit;
     		} else {
		### Login credentials are valid ###

			@data=$sth->fetchrow_array();
			$fullname=$data[3];
			$role=$data[4];

		### Close statement handles ###
		$sth->finish;
		}
	} else {

		### Register for a new account as a normal user ###
		### Add ordered items to Order Database ###
		$dbh->do("INSERT INTO userdb (email, passwd, pwdhint, fullname, role) VALUES ('$email', '$passwd','$pwdhint', '$fullname', '$role')")
			or die "Couldn't prepare SQL statement for Registration: " . $dbh->errstr;
	}

	### Set SSO Cookie ###
		$cookievalue=join(":", ($email, $passwd, $fullname, $role));
		$cookievalue=encode_base64($cookievalue);
		$cartcookie=cookie( -name=>'SSOid', -value=>$cookievalue, -path=>'/');
		print "Set-Cookie: $cartcookie\n";

	### Disconnect from the databases ###
	$dbh->disconnect;
	
	#print $query->redirect("/cgi-bin/badstore.cgi?action=viewprevious");	
	print $query->redirect($redirecturl);	
	if ($redirecturl eq '') {
		&home;
	} else {
		print $query->redirect($redirecturl);	
	}
}
