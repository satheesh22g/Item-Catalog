# Item Catalog
### Project Overview
> The Item Catalog project consists of developing an application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system. This project uses persistent data storage to create a RESTful web application that allows users to perform Create, Read, Update, and Delete operations

### What Will I Learn?
  * Develop a RESTful web application using the Python framework Flask
  * Implementing third-party OAuth authentication.
  * Implementing CRUD (create, read, update and delete) operations.

## Skills used for this project
- Python
- HTML
- CSS
- Bootstrap
- Flask
- Jinja2
- SQLAchemy

#### PreRequisites
  * [Python ~2.7](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)
  
#### Setup Project:
  1. Install Vagrant and VirtualBox
  2. Download or Clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
  3. Find the catalog folder and replace it with the content of this current repository, by either downloading or cloning it from
  [Here](https://github.com/satheeshg/itemcatalog).

### How to Run
1. Install VirtualBox and Vagrant
2. Clone this repo
3. Unzip and place the Item Catalog folder in your Vagrant directory
4. Launch Vagrant
```
$ Vagrant up 
```
5. Login to Vagrant
```
$ Vagrant ssh
```
6. Change directory to `/vagrant`
```
$ Cd /vagrant
```
7. Initialize the database
```
$ Python database_setup.py
```
8. Populate the database with some initial data
```
$ Python input_data.py
```
9. Launch application
```
$ Python project.py
```
10. Open the browser and go to http://localhost:5000

### JSON endpoints
#### Returns JSON of all States

```
/statess/JSON
```
#### Returns JSON of specific tourist place

```
/state/<int:state_id>/menu/<int:menu_id>/JSON
```
#### Returns JSON of touristplace

```
/state/<int:state_id>/menu/JSON
```


# catalog
# Item-Catalog
# Item-Catalog
# Item-Catalog
