Educational Data Mining Research Project: Piazza
Emily Chou
Marjan Salamati-Pour


I. Introduction 
With an end goal of researching the correlation between student activity on Piazza and academic performance, we developed and wrote two scripts that facilitate and aid the process of retrieving and analyzing data extracted from Piazza discussion forums. The first script, name anon.py, is used to parse an XML file and replace all names, emails, and urls  with user specified alternate versions, which essentially anonymizes the file for research use so that students’ personal information is protected while analyzing the data. The second script, named statistics.py, provides the first step towards extracting data from the file and displaying it in a clear, easily interpreted format. Specifically, the script outputs an activity log with information such as the number and date of posts pertaining to a user specified student. These two scripts are the starting points to being able to properly analyze data from Piazza and draw useful conclusions from the research.

II. Design 
Our approach to designing these two scripts differ according to their respective purposes:
anon.py -- This script is written in Python and serves to parse through the entire file containing raw, XML data and anonymize student names, emails, and urls. It takes either a csv or xml file that contains the real names and corresponding emails of all students in the class as input, and uses this information to replace all mentioned personal information in the main, data file. All links that have the string ‘http’ included will have it’s unique id replaced with another string such as ‘someurl’, though the origin of the url will be preserved (i.e. youtube, google, etc.).  Using dictionaries to store all first names, last names, and emails extracted from the input file with all the origin student information, we first create an anonymized version of the information by called Python’s hash function and appending that unique key to a general string indicating the type of string we are currently working with (i.e. ‘FIRST’ or ‘EMAIL’). If there are collisions in this process (i.e. if there are two students named ‘Bob’ in the class), we notify the researcher of this by printing out a statement with the speicifc names causing the collision and replace its anonymized versions with ‘FIRST?’. This data will no longer be relevant in the research process as we have no idea which ‘Bob’ the information relates to. Now that we have handled collisions and have a mapping of the original name and it’s corresponding anonymized version, we iterate through these dictionaries and search for each original name in the data file, replacing any matches with its anonymized version. We chose to have this file contain all anonymization methods so that the user can simply pass in a user’s file, content file, and the names of the output files, which would store the anonymized versions of each. This way, anonymizing data can be done quickly and easily through the command line for all the Piazza data from a single class. This design choice was suggested to us so that the scripts could be reused by anyone. 
	A more general decision we made was which library to use to parse the xml files. We found that the ElementTree XML API for Python was the most intuitive and useful way of parsing the given files. We were able to both iterate through all the tags in the file, access individual tags, and then find specific strings/replace at that string’s index. Writing to output files is also simple so the original files can still be accessed, or overwritten, depending on whether we were anonymizing or creating an anonymized copy.
statistics.py -- This script is also written in Python and serves to output an activity log of an individual student that contains information on how many posts the student created, followed up on, or updated, the date of these posts, and the unique id of the post so that it’s content can be easily retrieved if needed. The design behind this script is similar to anon.py in that it searches for strings in the data file matching the student’s unique Piazza id (obtained through the same user file mentioned in anon.py, which contains all original information of the class’s students) and extracts the data corresponding to that id. Because each post outlined in the XML data file will have the unique id of the owner as one of it’s neighboring element’s, we are able to find this information simply by parsing each element until we find one with the desired information, such as ‘date’. We hope this file can be the first stepping stone in beginning research on the data files as it provides basic yet very relevant information on student activity and participation on the discussion forum. 
III. Refactoring
There was quite a bit of refactoring done throughout this quarter as we honed our techniques and went from getting the basic functionality working to improving the overall design of our scripts. Instead of having one big main method, we split up the file into a few methods, including helper functions for better code reusability and readability. Now main calls on functions and assigns the parameters passed in as more intuitive variable names. Other variable names in script were also vague or unclear, so they were renamed in order for the reader to easily understand what the code does, in addition to the commenting and documentation throughout the files. For example, when a data tag is searched for, and the object within that tag is returned, it is stored in “dataItem”. Objects of tags usually have “item” in their name. Specific elements within those objects are then named accordingly; initially we had shorter, less descriptive variable names which have since been improved.

anon.py -- The method called for parsing the file depended on the filetype passed in (xml vs csv). The findandrep() is called to anonymize names and emails, and then writeMapping() to create a hashmap for retrieving the mapping between anonymized data and the original names/emails. 
Then replace() was a method written to call the functionality which shortens urls.The replace() method has been refactored significantly, because the original was hard to read and had many repetitive lines of code that were used for each type of different url, such as google, youtube, google docs, etc. The final result does not need to take into account the type of url, as it finds any link that starts with “http”, then replaces the unique parts of the url with whatever the user passes in as the third parameter. This parameter can be changed easily in the main function, but for now it is just “somelink”. (http://youtube.com/somelink)
Some other refactoring occurred when discovering that middle names were in some users files, so the findandrep() function and writeMapping() functions were improved to accommodate that. Now the middle names are anonymized and available in a hashmap as well. 
Our hashmaps were changed from just mapping emails and full names to the email hash values, to an output file that holds separate hashmaps for emails, first and last names, and first or last names (separately). Collisions are now printed to allow the user to know where there was ambiguity, whereas initially we just replaced any names which collided with the first occurrence of that name’s anonymization from the users file.

statistics.py -- Although there was not as much refactoring done with this file since it was written after having the anonymization script done, we still ran into different problems and edge cases such as needing to iterate through nested elements using the ElementTree. Previously, each element was separate and thus easily traversed through one by one. However, now each post we find has children and grandchildren elements that contain information such as the date or id of the post within them. Thus, we need to have nested loops to iterate through nested data. Despite this, we were able to create the script and fix bugs and edge cases in a much shorter period of time as we were able to use all the tactics, Python knowledge, and good design practices we learned while creating the anonymization script. 

IV. Future Goals
Now that we have an anonymization script for xml and csv files, and an script that prints out a user’s statistics for a given class file, we would like to build off the statistics script so that we can extract different types of data. Distinguishing between students who only post questions versus students who also respond to questions and post followups is definitely a goal we would like to achieve. From here, tracking the progress of each student in responding to posts as well as creating new posts, then correlating that with individual demographic information is something that could be looked into. Identifying when exactly students are posting the most questions (i.e. right before exams as opposed to all throughout the quarter) is something we would like to find out, and whether or not the time they post correlates with their grades. Additionally, we would like to format the activity log generated by statistics.py is a more readable and appealing platform, instead of just the terminal so that it is very user friendly as this is likely to be a quite useful tool for professors. Parsing JSON, not only XML files, is also something to finish up, in order to allow the user to choose what type of file they want to pass in.

V. Guide to Using the Scripts
Below is an outline of how to utilize the scripts we have developed and the specific Python libraries used. Any further questions can be sent to e8chou@ucsd.edu. 



How to Use
Python script name, description, and command line arguments, as well as the names of any output files
anon.py

Description
anon.py is a script to parse XML or CSV file and anonymize all names, emails, and urls.

It solves collisions by replacing with ?FIRST? or ?LAST?,and the unique number of the collision

Arguments

 sys.argv[0] => this script (anon.py)

 sys.argv[1] => users.xml or csv file with firstname, lastname, and  email of all students (the input file)

Note: csv file should be formatted as firstname,lastname,email on separate rows

 sys.argv[2] => anonymized version of argument 1, if xml file (the outfile)

 sys.argv[3] => xml file that is to be anonymized (the input file) class_content.xml or any file with the matching users of argument 1

 sys.argv[4] => anonymized version of argument 3 (the output file)

Output

 mapping.txt => mapping of anonymized names and original names

 If there are collisions, it will print a collision statement with the corresponding anonymized name statistics.py

Description
statistics.py is an activity log script that outputs the number of contributions, id of each post, date of each post, and the number of each type of contribution given a specific user.

The type of contribution is either a follow up, updating of a post, or creation of a post

Arguments

 sys.argv[0] => this script (statistics.py)

 sys.argv[1] => first name of the specific user to analyze

 sys.argv[2] => last name of the specific user to analyze
 
 sys.argv[3] => users.xml : firstname, lastname, and email of all students (the input file) 

 sys.argv[4] => class_content.xml: the content input file 
 
Output

 Prints out the number of posts created, followed up, updated, the date of the post, and info in the post

Python Libraries
string - Common string operations
operator - Standard operators as functions
Mathematical operations and object comparisons
re - Regular expression operations
sys - System-specific parameters and functions
sys.argv[0] is the file name
csv - CSV File reading and writing
xml.etree.ElementTree - The ElementTree XML API
The ElementTree class can be used to wrap an element structure, and convert it from and to XML. An Element is a container storing hierarchical data structures in memory. We used the ElementTree for parsing XML
The tree Element holds the parsed xml file data structures. Then the root container holds the elements in the outermost tag of the file. 
For the class_content.xml file, this is the <contents type="array"> tag, so that root contains the array of all tags nested within this tag.








