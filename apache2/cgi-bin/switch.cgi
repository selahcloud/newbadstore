#!/usr/bin/perl -w

### Script to switch graphical images to show load balancing in BadStore.net v1.2.3s ###

### Specify required PERL modules ###
use CGI::Carp qw(fatalsToBrowser);

print "Content-type: text/html\n\n";

print "<HTML><HEAD><H1>BadStore.net - Switch Images</H1></HEAD><BODY><p><hr><p>\n";

### Switch graphical identity ###
if (-e "/usr/local/apache2/htdocs/images/Thumbs.db") {
	`rm /usr/local/apache2/htdocs/images/Thumbs.db `;
	`tar -C /usr/local/apache2/htdocs/images/ -xzvf /usr/local/apache2/data/origimages.tgz `;
	print "Original Graphics Loaded...\n";
} 
else {
	`tar -C /usr/local/apache2/htdocs/images/ -xzvf /usr/local/apache2/data/lbimages.tgz `;
	print "Alternate Graphics Loaded...\n";

}
print "</BODY></HTML>\n";