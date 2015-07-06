# Command line tool for admin services in WSO2

Command line tool to play with admin services of a WSO2 server.

## Before starting

Make sure you edit repository/conf/carbon.xml file and make the following property to false

<code>&lt;HideAdminServiceWSDLs&gt;false&lt;/HideAdminServiceWSDLs&gt;</code>

This will enable accessing the WSDLs of admin services

## Tested with

1. Python 3.4.3
2. Suds-jurko - https://bitbucket.org/jurko/suds

## Example usage

<pre>
$ python3 wso2cmd.py
(WSO2) &gt;
</pre>

Then connect to the server,

<pre>
(WSO2) &gt; connect localhost:9443 admin admin
Connected to Application Server-5.2.1
(WSO2 - Application Server-5.2.1) &gt;
</pre>

Now authenticated to admin services. Can call any admin services from here on. Need to know the admin service name. You can find that out by starting the server with ./wso2server.sh -DosgiConsole and then doing

<pre>
&gt; listadminservices
</pre>

This will list down all available admin services of the server.

<pre>
(WSO2 - Application Server-5.2.1) &gt; call UserAdmin.&lt;TAB&gt;&lt;TAB&gt;
</pre>

This will list down all available operations for the admin service.

<pre>
(WSO2 - Application Server-5.2.1) > call UserAdmin.listUsers("*", -1)
[admin]
(WSO2 - Application Server-5.2.1) > call UserAdmin.addUser("testuser", "testpassword", ["admin", "Internal/everyone"], [], None)
None
(WSO2 - Application Server-5.2.1) > call UserAdmin.listUsers("*", -1)
[admin, testuser]
(WSO2 - Application Server-5.2.1) >
</pre>


