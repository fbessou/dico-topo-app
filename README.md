
<h1>The <a target="_blank" href="https://dicotopo.cths.fr/">DicoTopo</a> application API<image height="45" align="right" src="https://github.com/user-attachments/assets/f65ff1c0-ac0f-410d-8fe8-1bc0d6a3f2fe"/></h1>

![Static Badge](https://img.shields.io/badge/node-22.9-blue?style=for-the-badge&logo=Node.js)
![Static Badge](https://img.shields.io/badge/python-3.10.12-blue?style=for-the-badge&logo=python)
![Static Badge](https://img.shields.io/badge/sqlite-3-blue?style=for-the-badge&logo=sqlite)

![Static Badge](https://img.shields.io/badge/Flask-2.0.2-blue?logo=flask)
![Static Badge](https://img.shields.io/badge/SQLAlchemy-1.3-blue?logo=Sqlalchemy)
![Static Badge](https://img.shields.io/badge/elasticsearch-8.12-blue?logo=elasticsearch)

## Description

This repository contains the API service code for [https://dicotopo.cths.fr](https://dicotopo.cths.fr).

## Prerequisite - Install Elasticsearch

### Install Elasticsearch _and_ its ICU plugin
  
:warning: Use an ES version compatible with [requirements.txt](./requirements.txt)  
:information_source: Below commands are run independently/outside virtual environments (`deactivate`)  
  - Elasticsearch: refer to your organisation instructions or [Elasticsearch guidelines](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html#elasticsearch-install-packages)  
  - [ICU plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html): check if ICU is installed with `uconv -V`, otherwise:  
    <pre><code><b><i>path/to/elasticsearch_folder</i></b>/bin/elasticsearch-plugin install analysis-icu</code></pre>

<details>
  <summary>Local deployment</summary>

  With docker (security disabled):
   <pre><code>
  docker run --name <b><i>es-project_name</i></b> -d -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" elasticsearch:8.12.1
  docker exec <b><i>es-project_name</i></b> bash -c "bin/elasticsearch-plugin install analysis-icu"
  docker restart <b><i>es-project_name</i></b>
  </code></pre>

</details>

## Install

- Clone the GitHub repository in your projects folder:
  ```bash
  cd path/to/projects_folder/
  git clone https://github.com/chartes/encpos-app.git
  ```

<details>
  <summary>- Clone the GitHub repository in your projects folder:</summary>
  
  ```bash
  cd path/to/projects_folder/
  git clone https://github.com/chartes/encpos-app.git
  ```
</details>

- Set up the virtual environment in the app folder:
  ```bash
  cd path/to/projects_folder/encpos-app
  python3 -m venv venv
  source venv/bin/activate
  pip3 install -r requirements.txt
  ```

  
  For servers requiring uWSGI to run Python apps (remote Nginx servers):
  - check if uWSGI is installed `pip3 list --local`
  - install it in the virtual env if it's not: `pip3 install uWSGI`.

  *NB : cette commande peut nécessiter d'installer wheel :*  
  - pour vérifier si wheel est installé : `pip3 show wheel`  
  - pour l'installer le cas échéant : `pip3 install wheel`


- Install Elasticsearch and create indices _if they are not available_:  
Follow the ES installation & initial indexing instructions [below](#indexing)  

2) Start the server in debug mode:
```
python flask_app.py
```
3) Then visit http://127.0.0.1:5003/dico-topo/api/1.0?capabilities to get infos about the API capabilities


more info about the configuration of ES:  https://jolicode.com/blog/construire-un-bon-analyzer-francais-pour-elasticsearch


How to reindex all indexable data, referencing a localhost api:
```
python manage.py db-reindex --host=http://localhost --delete=1  
```
