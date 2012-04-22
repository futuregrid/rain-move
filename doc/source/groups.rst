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
~~~~~~~~~~~~~~

Creating a group with the given name::

  fabric group create <name>


Deleting a group with the given name::

  fabric group delete <name>


Joining group a and b and putting them in a group with the name_c::

  fabric group join <name_a> <name_b> <name_c>


Replacing the group a with group b::

   fabric group replace <name_a> <name_b> 

Printing the group members::
 
   fabric group list

Creating an empty group::
 
   fabric group empty <name>

All group commands such as adding deleting and so forth are
applied to the group set with default:: 

   fabric groug default <name>

Returning the ith obgect of name::
 
   fabric group get <i> of <name> 

Setting the ith object in the group to name:: 

   fabric group set <i> in <name> to <value>

Loading the group from a file::
 
   fabric group load <filename>


Loading without parameter loads the groups from ~/.futuregrid/futuregrid.cfg::
 
   fabric group load

Saving the group from a file:: 

   fabric group save <filename>


Save without parameter saves the groups from ~/.futuregrid/futuregrid.cfg existing groups in that file will be deleted. So be careful if you want to keep your old groups. In doubt use a named file:: 

   fabric group load

Using Python syntax to interface with groups is easily possible as follows::

   fabric group eval <string>

Thus the command::

  fabric group eval "
  a = [] \n
  a = ["hostname1.university.edu", "hostname2.university.edu"] \n
  b = ["hostname3.university.edu", "hostname4.university.edu"] \n
  c = a + b \n
  print c"

will create a group c with the strings in a and b combined.

