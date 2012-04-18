Groups
------

TODO: could we just not use operators from python and use eval to do this?

The fabric command introduces the concept of a group. A group is a
named array of strings. Groups are convenient to define simple nameing
schemes defined for the user for a number of objects that can be
identified by its name.

Example:

Let us assume you like to define a number of resources for your project and put them in the group MyResources. You can do this as follows::

  > fg-fabric
  fabric> group create "MyResources"
  fabric> group default "MyResources"
  fabric> group add "host1.university.edu"
  fabric> group add "host2.university.edu"

This series of commands has now created a group that contains the strings host1.university.edu and host2.university.edu.

If commands in fabric have the -group otion, the group can be passed allong instead of explicitly defining all the  names in that group.

Example:

Let us assume you like to rain an operating system onto this group, you can do this with

  fabric> rain -image imagename -group "MyResources"

Group commands

::
  fabric group create <name>

    creates a group with the given name

::
  fabric group delete <name>

    deletes a group with the given name

::
  fabric group join <name_a> <name_b> <name_c>

    joins group a and be and puts them in a group with the name_c

::
   fabric group replace <name_a> <name_b> 

    replaces the group a with group b

:: 
   fabric group list

     prints the group members

:: 
   fabric group empty <name>

     creates an empty group

:: 
   fabric groug default <name>

     all group commands such as adding deleting and so forth are
     applied to the group set with default

:: 
   fabric group get <i> of <name> 

     returns the ith obgect of name

:: 
   fabric group set <i> in <name> to <value>


     sets the ith object in the group to name

:: 
   fabric group load <filename>

     loads the group from a file

:: 
   fabric group load

     load without parameter loads the groups from ~/.futuregrid/futuregrid.cfg
     
:: 
   fabric group save <filename>

     saves the group from a file

:: 
   fabric group load

     save without parameter saves the groups from
     ~/.futuregrid/futuregrid.cfg existing groups in that file will be
     deleted. So be careful if you want to keep your old groups. In
     doubt use a named file.


Alternative Syntax

  possibly we need to use python/ipython instead of cmd2?

  a = []
  a = ["hostname1.university.edu", "hostname2.university.edu"] 
  b = ["hostname3.university.edu", "hostname4.university.edu"] 
  
  c = a + b

  print c

  load group a
  save group a
