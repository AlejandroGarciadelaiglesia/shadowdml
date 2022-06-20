**Shadow Daemon** is a collection of tools to **detect**, **record** and **prevent** **attacks** on *web applications*.
Technically speaking, Shadow Daemon is a **web application firewall** that intercepts requests and filters out malicious parameters.
It is a modular system that separates web application, analysis and interface to increase security, flexibility and expandability.

This is the main component that handles the analysis and storage of requests.

# Documentation
For the full documentation please refer to [shadowd.zecure.org](https://shadowd.zecure.org/).

# Installation
## Preparation
Use cmake to configure and prepare the project. It is a good idea to create a separate directory for this.
A typical installation might look like this.

    mkdir build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=Release ..

## Compilation
If cmake is successful it creates a makefile. Use it to compile and install the project.

    make shadowd
    make install

## Database
Install and configure a database server. At the moment shadowd officially supports PostgreSQL and MySQL.
Afterwards create a new user and database for shadowd and import the correct layout.

If you are using PostgreSQL you can use `psql` to import the layout.

    psql -Ushadowd shadowd < /usr/share/shadowd/pgsql_layout.sql

If you are using MySQL you can use `mysql` to import the layout. The user requires the `CREATE ROUTINE` privilege.

    mysql -ushadowd -p shadowd < /usr/share/shadowd/mysql_layout.sql

# Configuration
The installer copies the configuration file to */etc/shadowd/shadowd.ini*. The file is annotated and should be self-explanatory.

# Machine learning functionalities
This functionality allows to distinguish any GET or POST parameter between four possible classes: legitimate request, cross site scripting, shell injection and sql injection

If the user want to use a machine learning functionality based on a support vector machines algorithm, it is needed to deploy an API REST in python in the local machine of the shadowd project

First is needed to install python and then install dependencies needed:

    pip3 install -r requirements.txt

After that, it is needed to update the 0.0.0.0 ip address in all ocurrences in the Blacklist.cpp file for the private ip of the machine where the API REST will be deployed.

Finally, execute the following script in the apiml folder:

    ./launch.sh

