# Blackbalsam

![image](https://user-images.githubusercontent.com/306971/80292483-05426b00-8725-11ea-9ab3-0686c8a6c76a.png)

   * [Blackbalsam](https://blackbalsam.renci.org/blackbalsam/hub/login) is an open source data science environment with an initial focus on COVID-19 and North Carolina.
      * [Overview](#overview)
         * [Motivation](#motivation)
         * [Implementation Overview](#implementation-overview)
         * [Authentication](#authentication)
         * [Artificial Intelligence &amp; Analytics](#artificial-intelligence--analytics)
         * [Notebook Computing](#notebook-computing)
         * [Visualization](#visualization)
         * [Compute](#compute)
         * [Storage](#storage)
            * [NFS](#nfs)
            * [Object Store](#object-store)
            * [Alluxio Memory Cache](#alluxio-memory-cache)
      * [Data](#data)
         * [COVID-19](#covid-19)
   * [Architecture](#architecture)
      * [Prerequisites](#prerequisites)
      * [Installation](#installation)
         * [Authentication](#authentication-1)
         * [Environment Configuration](#environment-configuration)
         * [Executing the Install](#executing-the-install)
         * [Help](#help)
   * [About](#about)
   * [Next](#next)
   
## Overview

### Motivation

Data Science is impeded by operatoinal obstacles we can address. The discipline draws on numerous skill set but not everyone has all of the skills, and not everyone has those skills in the same degree. Once someone has created an interesting result, asking a collaborator to laboriously reproduce the steps the first researcher took is lost time. Similarly, each participant in a team needing to acquire the same data set is a source of error and a waste of time. In view of these realities, ready availability of tools and data in a common digital environment accomplishes a number of aims simultaneously:

* **Digital Lab**: It creates a digital laboratory so that each individual is not posed with the obstacle of assembling all the required computational and data instruments themselves from scratch.
* **Sharing**: Living in the cloud has acclimatized many of us to instant messaging a URL to a coworker many times a day. In prior times, email and installing software locally was the norm. When one person creates an interesting analysis, it should be possible to message a collaborator with a URL to that analysis.
* **Scale**: Setting up an analysis on one's laptop is very good but training machine learning models and analyzing large data sets increasingly requires computational scale, access to specialized hardware and accelerators, and the modern tools to access that scale.

Blackbalsam was developed to assemble a pragmatic digital data science laboratory to meet those needs.

### Implementation Overview

Blackbalsam's **interface** uses a JupyterHub notebook environment featuring artificial intelligence, visualization, and scalable computing capabilities. For **computation**, integration of the Jupyter environment with Apache Spark and Kubernetes allows users to dynamically create personal Spark clusters with user specified attributes. Plans to incorporate GPU nodes to enable deep learning scenarios are under way. These interface and compute capabilities are coupled to a tiered **storage** platform including networked filesystem, the Mino S3 compatible object store, and the Alluxio distributed memory cache. These provide access to COVID-19 data sets. The prototype runs at the [Renaissance Computing Institute](https://renci.org/) in an on premise cluster, is cloud ready, and is open source under the MIT License.

### Authentication
Authentication is provided via GitHub and OpenID Connect (OIDC). Whitelisted users can use their GitHub identity to login and start working immediately.

### Artificial Intelligence & Analytics
The Blackbalsam notebook includes Tensorflow, Keras, Gensim, PyTorch, scikit-learn, pandas, and numpy. Users can also easily create Spark clusters providing access to Spark's [MLlib](https://spark.apache.org/docs/latest/ml-guide.html) machine learning toolkit.

### Notebook Computing
JupyterHub provides the interface to the environment presenting a notebook providing Python and R kernels.

### Visualization
The Blackbalsam notebook includes [matplotlib](https://matplotlib.org/), [plotly](https://plotly.com/), and [seaborn](https://seaborn.pydata.org/). It also includes [bokeh](https://docs.bokeh.org/en/latest/index.html), [yellowbrick](https://www.scikit-yb.org/en/latest/), and [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) to handle more specialized needs including machine learning and geospatial visualization. This figure shows a Leaflet component in Jupyter:
![image](https://user-images.githubusercontent.com/306971/80293212-91579100-872b-11ea-9fe3-d8bd00414794.png)

And here's a county level US map using Pandas and Plotly:
![image](https://user-images.githubusercontent.com/306971/80328291-eb7c5300-880c-11ea-92f1-8ff9be9cd493.png)

### Compute
The Blackbalsam notebook is instrumented to allow dynamically launching a customized, personal Apache Spark cluster of a user specified topology through the Kubernetes API. In this figure, we see the notebook for loading the Python interface to Blackbalsam and creating a four worker Spark cluster. After creating the cluster, it uses Spark's resilient distributed dataset (RDD) interface and its functional programming paradigm to apply a functional operator to each loaded article.
![image](https://user-images.githubusercontent.com/306971/80293315-60c42700-872c-11ea-8b29-6a954bc54e80.png)

The mechanics of configuring and launching the cluster are handled transparently to the user. Exiting the notebook kernel deallocates the cluster. This figure shows the four 1GB Spark workers created by the previous steps.
![image](https://user-images.githubusercontent.com/306971/80293355-ae409400-872c-11ea-94d7-73b50e67bf7a.png)

Next, we create a Word2Vec word embedding using the provided Spark machine learning libraries:
![image](https://user-images.githubusercontent.com/306971/80293487-c664e300-872d-11ea-809f-454cdb1c395e.png)

### Storage
#### NFS
The network filesystem (NFS) is used to mount shared storage to each user notebook at /home/shared.

#### Object Store
The Minio object store provides an S3 compatible interface .
![image](https://user-images.githubusercontent.com/306971/80293124-8e0fd580-872a-11ea-8643-1bfbd0978368.png)

Minio supports distributed deployment scenarios which make it horizontally scalable. Minio also facilitates loading large objects into Apache Spark
![image](https://user-images.githubusercontent.com/306971/80295919-0a171700-8745-11ea-8060-d32d2fe71468.png)

#### Alluxio Memory Cache
Alluxio is a distributed memory cache interposed between multiple "under-filesystems" like NFS and analytic tools like Spark and its machine learning toolkit. It stores data in node memory, not only accelerating access but allowing failed workflows to restart and other interesting scenarios. It also supports using the Minio S3 object store as an under filesystem. Since Alluxio also supports an ACL based access control model, this creates some interesting possibilities for us to explore with regard to data sharing.

## Data 

### COVID-19 
The first Blackbalsam instance is the RENCI COVID-19 platform. See the descriptionof the [data corpus](https://github.com/stevencox/blackbalsam-covid-19-data) for information on how to request new data.

A Kubernetes periodic task exectues the data repository update script hourly.

# Architecture
Blackbalsam's design composes widely used open source systems including Docker, Kubernetes, Apache Spark, Jupyter and JupyterHub into a coherent environment.
![image](https://user-images.githubusercontent.com/306971/80694659-d0c30c00-8aa2-11ea-87be-13c4bb3c8ccf.png)

## Prerequisites

* Kubernetes v1.17.4
* kubectl >=v1.17.4
* Python 3.7.x
* The Linux [envsubst](https://www.gnu.org/software/gettext/manual/html_node/envsubst-Invocation.html) command
* Helm 2 (a JupyterHub dependency)

## Installation

### Authentication

Create a [GitHub OAuth app](https://developer.github.com/apps/building-oauth-apps/)

### Environment Configuration

Create a file in your home directory called `.blackbalsam` with contents like these:
```
jupyterhub_secret_token=<jupyter-hub-secret-token> 
jupyterhub_baseUrl=/blackbalsam/                  
public_ip=<public-ip-address>                    
github_client_id=<github-client-id>               
github_client_secret=<client-server-id>
github_oauth_callback=http://<your-domain-name>/blackbalsam/oauth_callback 
minio_access_key=<minio-access-key>
minio_secret_key=<minio-secret-key>   
```
Ensure you have kubectl configured to point to a Kubernetes cluster.

### Executing the Install
Clone the repository. Create a virtual environment, populate the environment, and run the installer.
```
git clone https://github.com/helxplatform/blackbalsam.git
python3 -m venv blackbbalsam-env
source blackbalsam-env/bin/activate
cd blackbalsam
bin/blackbalsam up
```

After a substantial pause, you should see output like this:
```
NOTES:
Thank you for installing JupyterHub!

Your release is named blackbalsam and installed into the namespace blackbalsam.

You can find if the hub and proxy is ready by doing:

 kubectl --namespace=blackbalsam get pod

and watching for both those pods to be in status 'Ready'.

You can find the public IP of the JupyterHub by doing:

 kubectl --namespace=blackbalsam get svc proxy-public

It might take a few minutes for it to appear!

Note that this is still an alpha release! If you have questions, feel free to
  1. Read the guide at https://z2jh.jupyter.org
  2. Chat with us at https://gitter.im/jupyterhub/jupyterhub
  3. File issues at https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues
```
Then, go to https://{your-domain}/blackbalsam/ to visit the application.

### Help
For information on the command line management interface, see the help option:
```
$ bin/blackbalsam data help
bin/blackbalsam is the command line interface for a Blackbalsam data science cluster.

Each of these commands include up, down, status, and restart.

  eg: bin/blackbalsam <command> [ up | down | status | restart ]

User Experience Services:
  hub   	Manage the JupyterHub and associated proxy mappings, storage, etc.

Storage Services:
  alluxio 	Manage Alluxio services and distributed workers.
  minio 	Manage Minio S3 interface. Creates a service called 'minio'.

Proxy Services:
  proxy 	Manage the programmable Ambassador edge proxy.

Data Services:
  data   	Install the periodic data update task for this cluster.
  data run	Run the periodic data update task now.
  data stop	Stop the running data update task if one exists

Secrets:
  secret  	Manage secrets based on environment conifguration.

General:
  up    	Execute configurations and start all services.
  down  	Stop all cluster services.
  restart	Stop and start all system components.
  status	Report on Kubernetes components and system services in detail.
  nodes 	Display detailed usage and status for cluster nodes.
  help  	Show this message.
```

# About

From [Wikipedia](https://en.wikipedia.org/wiki/Black_Balsam_Knob):

"Black Balsam Knob,[2] also known as Black Balsam Bald, is in the Pisgah National Forest southwest of Asheville, North Carolina, near milepost 420 on the Blue Ridge Parkway. It is the second highest mountain[3] in the Great Balsam Mountains. The Great Balsams are within the Blue Ridge Mountains, which are part of the Appalachian Mountains. It is the 23rd highest of the 40 mountains in North Carolina over 6000 feet.[4]"

Blackbalsam's authors are Steve Cox and PJ Linebaugh.

# Next

* [ ] **AI & ML**: 
  * [ ] Debug and fix the JupyterHub on Kubernetes bug preventing the use of multiple notebook profiles.
  * [ ] Create a separate AI notebook and configure GPU targeting.
  * [ ] Purchase and integrate GPU hardware.
* [ ] **Persistence**: 
  * [ ] Configure and test Alluxio to Minio interfaces
  * [ ] Configure and test Alluxio to NFS interfaces
  * [ ] Configure and test Spark Alluxio interface
* [ ] **Tools**: 
  * [ ] Create and document notebooks with examples of key features
  * [ ] Track user demand to prioritize and incorporate new capabilities.
* [ ] **Infrastructure**:
  * [ ] Get trusted certificates for the site and a development instance.
  * [ ] Establish a blackbalsam-dev namespace for development testing.
  * [ ] Crete an automated build and test pipeline.
  * [ ] Purchase and deploy new hardware.
  * [ ] Move management tools to Helm 3.

![image](https://user-images.githubusercontent.com/306971/80296143-80684900-8746-11ea-9ad7-e2dc69d6d71f.png)

