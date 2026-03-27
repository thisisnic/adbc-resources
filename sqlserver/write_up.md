# Testing it out - connecting to SQL Server from Python

I wanted to test out the pain of connecting to databases, so I could test out the experience with and without ADBC.

## Running SQL Server in a Container

First step, get hold of SQL server. I'm on Linux, so I decided to run it in a Docker image.  

I use the instructions at https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver17&tabs=cli&pivots=cs1-bash

I install it by running

```
docker pull mcr.microsoft.com/mssql/server:2022-latest
```

 I use 2022 because after originally trying with 2025 I got some indecipherable error message but I didn't think was worth the booking for the sake of a tutorial.

Next, I run it by calling

```
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Mypassword123!" \ -p 1433:1433 --name sql1 --hostname sql1 \ -d \ mcr.microsoft.com/mssql/server:2022-latest
```

Now I try to connect to the container:
```
docker exec -it sql1 "bash"
```

It worked! So now I want to connect to it and run queries.

## Adding some data to the database

I need to add some data to the database first. So let's try that.  Here's some example code.

```
docker exec sql1 /opt/mssql-tools18/bin/sqlcmd \ -S localhost -U sa -P "Mypassword123!" -No \ -Q " CREATE TABLE products ( id INT PRIMARY KEY, name NVARCHAR(50), price FLOAT ); INSERT INTO products VALUES (1, 'Widget A', 9.99); INSERT INTO products VALUES (2, 'Widget B', 14.99); INSERT INTO products VALUES (3, 'Widget C', 4.49); INSERT INTO products VALUES (4, 'Widget D', 24.99); INSERT INTO products VALUES (5, 'Widget E', 1.99); "
```

It worked! So now let's query it.

## Installing ODBC

I'm using the instructions found online at:

https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver17&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline

Here we go.  First.

```
if ! [[ "18.04 20.04 22.04 24.04 25.10" == *"$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)"* ]];
then
    echo "Ubuntu $(grep VERSION_ID /etc/os-release | cut -d '"' -f 2) is not currently supported.";
    exit;
fi

# Download the package to configure the Microsoft repo
curl -sSL -O https://packages.microsoft.com/config/ubuntu/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)/packages-microsoft-prod.deb
# Install the package
sudo dpkg -i packages-microsoft-prod.deb
# Delete the file
rm packages-microsoft-prod.deb

# Install the driver
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get install -y unixodbc-dev
```

But wait, I want to make sure it's really as hard as I think.  This seems like a lot.  When I've been writing R code to connect to databases in the past, it's not been this bad.  Instead I'm going to have a look at using Python libraries that already exist - surely they'll do all of this setup for me, right??

## Installing mssql-python

https://learn.microsoft.com/en-us/sql/connect/python/mssql-python/python-sql-driver-mssql-python-quickstart?view=sql-server-ver17&tabs=windows%2Cazure-sql

Installing system dependencies went fine

```
apt-get install -y libltdl7 libkrb5-3 libgssapi-krb5-2
```

The I set up the venv and dependencies

```
(sqlserver) nic@Inspiron-14-Plus-7440:~/adbc-resources/sqlserver$ uv pip install mssql-python
Resolved 15 packages in 1.65s
Prepared 8 packages in 2.43s
Installed 15 packages in 13ms
 + azure-core==1.39.0
 + azure-identity==1.25.3
 + certifi==2026.2.25
 + cffi==2.0.0
 + charset-normalizer==3.4.6
 + cryptography==46.0.6
 + idna==3.11
 + msal==1.35.1
 + msal-extensions==1.3.1
 + mssql-python==1.4.0
 + pycparser==3.0
 + pyjwt==2.12.1
 + requests==2.33.0
 + typing-extensions==4.15.0
 + urllib3==2.6.3

```

Now dotenv for some reason
```
uv pip install python-dotenv
```

I now create `app.py` containing the following code

```

"""
Connects to a SQL database using mssql-python
"""

from os import getenv
from dotenv import load_dotenv
from mssql_python import connect

load_dotenv()

conn = connect(getenv("SQL_CONNECTION_STRING"))

SQL_QUERY = """
SELECT
*
FROM 
products;
"""

cursor = conn.cursor()
cursor.execute(SQL_QUERY)

rows = cursor.fetchall()
for row in rows:
    print(row)

```

In the create .env with this string:
```
SQL_CONNECTION_STRING="Server=localhost,1433;Database=master;Uid=sa;Pwd=Mypassword123!;Encrypt=yes;TrustServerCertificate=yes;"
```

OK, so this wasn't too bad tbh.  The string is a bit weird, but once it's done it's done. So now, let's have a look at running our query.

## Running the query

I try to run the app.py file from the command line

```
python3 app.py
```

And now we have our first error:

```
(sqlserver) nic@Inspiron-14-Plus-7440:~/adbc-resources/sqlserver$ python3 app.py
Traceback (most recent call last):
  File "/home/nic/adbc-resources/sqlserver/app.py", line 10, in <module>
    conn = connect(getenv("SQL_CONNECTION_STRING"))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/nic/adbc-resources/sqlserver/.venv/lib/python3.12/site-packages/mssql_python/db_connection.py", line 46, in connect
    conn = Connection(
           ^^^^^^^^^^^
  File "/home/nic/adbc-resources/sqlserver/.venv/lib/python3.12/site-packages/mssql_python/connection.py", line 319, in __init__
    self._conn = ddbc_bindings.Connection(
                 ^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: [Microsoft][ODBC Driver 18 for SQL Server]Neither DSN nor SERVER keyword supplied

```
Err, huh?  I did pass in in the server in my `.env` file though.

At this point i'm bored of reading tutorials, these days I ask AI for everything, and so go take this to Claude.  It tells me I'm actually missing the `DRIVER` keyword, which is why the ODBC layer isn't finding the `SERVER` keyword...sure.  To be fair, I got the connection string from Claude, so it's not entirely off the hook.  Let's try again.

I update my `.env` file, upon Claude's suggestion to contain:

```
SQL_CONNECTION_STRING="DRIVER={ODBC Driver 18 for SQL Server};Server=localhost,1433;Database=master;Uid=sa;Pwd=Mypassword123!;Encrypt=yes;TrustServerCertificate=yes;"
```

This should work now, right?  Nope...

```
(sqlserver) nic@Inspiron-14-Plus-7440:~/adbc-resources/sqlserver$ python3 app.py
Traceback (most recent call last):
  File "/home/nic/adbc-resources/sqlserver/app.py", line 10, in <module>
    conn = connect(getenv("SQL_CONNECTION_STRING"))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/nic/adbc-resources/sqlserver/.venv/lib/python3.12/site-packages/mssql_python/db_connection.py", line 46, in connect
    conn = Connection(
           ^^^^^^^^^^^
  File "/home/nic/adbc-resources/sqlserver/.venv/lib/python3.12/site-packages/mssql_python/connection.py", line 240, in __init__
    self.connection_str = self._construct_connection_string(connection_str, **kwargs)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/nic/adbc-resources/sqlserver/.venv/lib/python3.12/site-packages/mssql_python/connection.py", line 363, in _construct_connection_string
    parsed_params = parser._parse(connection_str)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/nic/adbc-resources/sqlserver/.venv/lib/python3.12/site-packages/mssql_python/connection_string_parser.py", line 271, in _parse
    raise ConnectionStringParseError(errors)
mssql_python.exceptions.ConnectionStringParseError: Connection string parsing failed:
  Reserved keyword 'driver' is controlled by the driver and cannot be specified by the user
```

Back to Claude...

> "Interesting — `mssql_python` is not standard pyodbc, it's Microsoft's own library that handles the driver internally. So **don't include `DRIVER`** — your original connection string was actually the right format."

Claude, I don't care it's interesting, I just want my code to work!

Claude is now convinced that my original code is wrong, but when I paste it in it says it's correct and that maybe it's the quotes in the .env file. Sure.  I remove them and try again.  nope, same error.

 Claude asks me to add in some debug code  to print out values, and I oblige.

 `print(repr(getenv("SQL_CONNECTION_STRING")))`
  
  Then, same error and it complains that my .env file is wrong.  Not my fault, Claude!!

Once again I update it.

```
SQL_CONNECTION_STRING=Server=localhost,1433;Database=master;Uid=sa;Pwd=Mypassword123!;Encrypt=yes;TrustServerCertificate=yes;
```

Finally, it works!   Still at this point I'm not entirely convinced. I mean I got the string from Claude, right? and I guess it would have just put extra quote marks in around the original one or something?

But then I go back to the original tutorial and see there are quote marks in there, so clearly issues.

 I know this isn't the only way of doing it though and I want to have a look using the pyodbc library instead.  I'm going to nuke to current directory and start again.

## Using pyODBC

This time I'm looking at the instructions found in https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Linux

First thing I notice: there's a lot of stuff in this file.

So, step 1: create a temporary text file for definining the ODBC DSN.  Sure.  I call it `dsn.txt` and add the text (which I totally asked Claude to generate as I had no idea)

```
[MSSQLServerDatabase] 
Driver = ODBC Driver 18 for SQL Server 
Description = Connect to my SQL Server instance 
Trace = No 
Server = localhost,1433 
Database = master 
Encrypt = yes 
TrustServerCertificate = yes
```

The next step says I can find the driver version by inspecting the system-wide "odbcinst.ini" file, which I absolutely do not have in the location suggested there, but yay for Claude remembering from our earlier experiment, I guess.

Then I have to do a load of...stuff... to create a system DSN.  Again, no idea what this means.

```
sudo odbcinst -i -s -f dsn.txt -l
```

Oh, but it fails as I don't have odbcinst installed. Hmm.  I re-read the instructions and realise I need to install the drivers. I guess the Microsoft instructions installed them for that package, or something?  I'm kinda bored again, so I ask Claude, to get an understanding - truncated below.

> No — `mssql_python` bundles its own driver internally and bypasses the system ODBC stack entirely. That's why it rejected the `DRIVER=` keyword too — it doesn't use it.
>For `pyodbc` you need the system-level pieces installed separately:
>**1. Install unixODBC** (provides `odbcinst`):
>**2. Install the Microsoft ODBC Driver 18:**

*sighs* This is frustrating.

So, back to the driver installation I avoided earlier then.  Here we go:

```
if ! [[ "18.04 20.04 22.04 24.04 25.10" == *"$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)"* ]];
then
    echo "Ubuntu $(grep VERSION_ID /etc/os-release | cut -d '"' -f 2) is not currently supported.";
    exit;
fi

# Download the package to configure the Microsoft repo
curl -sSL -O https://packages.microsoft.com/config/ubuntu/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)/packages-microsoft-prod.deb
# Install the package
sudo dpkg -i packages-microsoft-prod.deb
# Delete the file
rm packages-microsoft-prod.deb

# Install the driver
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get install -y unixodbc-dev
```

OK, so a lot of stuff installs, hooray.  I re-run `sudo odbcinst -i -s -f dsn.txt -l` and it works!

Now let's make a new version of app.py and give it a whirl.  I use the `.env` approach again to store the username and password; this time I don't need to specify the rest as I did the DSN setup.

```
"""
Connects to a SQL database using mssql-python
"""

from os import getenv
from dotenv import load_dotenv
from pyodbc import connect

load_dotenv()

conn =connect(f'DSN=MSSQLServerDatabase;UID={getenv("SQL_UID")};PWD={getenv("SQL_PASSWORD")}')

SQL_QUERY = """
SELECT
*
FROM 
products;
"""

cursor = conn.cursor()
cursor.execute(SQL_QUERY)

rows = cursor.fetchall()
for row in rows:
    print(row)

```

It works!  But all this DSN stuff is so weird to me; why do I need to do that to query a database?  It feels weird, it feels like too much.  Why can't I just set it up and send code?

### Using ADBC

And now, let's see how it looks using ADBC. I would like this to be nicer.

I'm gonna nuke my other setups first just to be sure it's not using any of my prevbious work.

```
sudo apt remove msodbcsql18
sudo apt remove unixodbc unixodbc-dev
sudo rm /etc/apt/sources.list.d/mssql-release.list
sudo apt-key del $(sudo apt-key list | grep -B1 "Microsoft" | head -1)
# Clean up 
sudo apt autoremove 
sudo apt update
sudo rm /etc/odbc.ini # system-wide
```

Bye!!

I go to https://docs.adbc-drivers.org/drivers/mssql/

I already have dbc set up (though it's really quick if you don't), and so I created a new virtual env and  ran

`dbc install mssql`

```
nic@Inspiron-14-Plus-7440:~/adbc-resources/sqlserver/adbc$ dbc install mssql
[✓] searching
[✓] downloading
[✓] installing
[✓] verifying signature

Installed mssql 1.3.1 to /home/nic/adbc-resources/sqlserver/adbc/.venv/etc/adbc/drivers

```

Yay, it worked, very easily.  

I will admit one piece of friction when I tried running

```
nic@Inspiron-14-Plus-7440:~/adbc-resources/sqlserver/adbc$ uv pip install abdc-driver-manager
  × No solution found when resolving dependencies:
  ╰─▶ Because abdc-driver-manager was not found in the package registry and you require abdc-driver-manager, we can conclude that your requirements are unsatisfiable.
```

I absolutely did have to ask Claude, which pointed out to me that I'd typed A**B**CD instead of A**D**BC.  I think I will not be alone in this mistake. 

I update my app.py 

```
"""
Connects to a SQL database using mssql-python
"""

from os import getenv
from dotenv import load_dotenv
from adbc_driver_manager import dbapi

load_dotenv()

conn = dbapi.connect(
  driver="mssql",
  db_kwargs={
      "uri": f'mssql://{getenv("SQL_UID")}:{getenv("SQL_PASSWORD")}@localhost:1433'
  }
)




SQL_QUERY = """
SELECT
*
FROM 
products;
"""

cursor = conn.cursor()
cursor.execute(SQL_QUERY)

rows = cursor.fetchall()
for row in rows:
    print(row)

```


I needed to install pyarrow as it's an optional dependency, but necessary here for printing out the rows, but then...it just worked.

I'll admit I did have an issue which I almost didn't mention out of embarassment - I'm a novice Python user and forgot to activate my venv on a first run, and so mssql was installed to a different venv and so I got an error saying it wasn't installed.  This was me, not adbc though!

And on reflection, I like that this happened - now the DB drivers are project dependencies and not system dependencies.  This makes a lot more sense to me theoretically, than setting up these system-wide DSN files!!

## Conclusion

 I've got to admit it, I did start this off with a bit of scepticism about how good ADBC would be, because honestly my previous experience querying databases has been on platforms when everything was already set up for me. this is fine when this is the case but what about when it isn't? that's when things get a lot trickier. 

the ODBC setup here would have been easily enough to trip me up. I definitely prefer using the Microsoft package because I didn't have to do all the weird things with the DSN, and I appreciate that pyodbc is potentially a generic connector but honestly all that config was just weird and kind of annoying.

  it genuinely felt wrong to me in a lot of ways. I still don't really understand why I need to set up all this system level config just to send sequel queries to a database to be honest.
 
 But with ADBC it really was that much better!

 and I'm somewhat delighted that I'm done with this experiment, experience the visceral misery of ODBC config and hopefully never have to do it again :)
