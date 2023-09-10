<h1 style="text-align: center;">Containers, Docker and Amazon ECS</h1>

<h2>Table of Content</h2>

- [1. Introduction](#1-introduction)
- [2. What even are containers and why do we use them?](#2-what-even-are-containers-and-why-do-we-use-them)
  - [Notes on OS Kernel isolation](#notes-on-os-kernel-isolation)
  - [Containers vs Container Images](#containers-vs-container-images)
    - [Side notes](#side-notes)
  - [Benefits of using container](#benefits-of-using-container)
- [3. Docker tutorial](#3-docker-tutorial)
  - [Explanations](#explanations)
  - [Docker commands](#docker-commands)
- [4. Amazon ECS tutorial](#4-amazon-ecs-tutorial)
  - [Prerequisites](#prerequisites)
  - [Tutorial walkthrough](#tutorial-walkthrough)
    - [Step 1: Push your Docker container image to ECR.](#step-1-push-your-docker-container-image-to-ecr)
    - [Step 2: Build the image and push it to ECR](#step-2-build-the-image-and-push-it-to-ecr)
    - [Step 3: Create the ECS cluster](#step-3-create-the-ecs-cluster)
    - [Step 4: Create a Task Definition](#step-4-create-a-task-definition)
    - [Step 5: Start a Service](#step-5-start-a-service)
    - [Step 6: Access the newly deployed API](#step-6-access-the-newly-deployed-api)
    - [Step 7: Cleaning Up](#step-7-cleaning-up)
  - [Congratulation!!!](#congratulation)
  - [Good to know:](#good-to-know)
- [Conclusion](#conclusion)
  - [Benefits of containers](#benefits-of-containers)
  - [Benefits of Container Orchestration services (ECS, Kubernetes, etc)](#benefits-of-container-orchestration-services-ecs-kubernetes-etc)
- [5. Acknowledgement](#5-acknowledgement)
- [6. References](#6-references)

## 1. Introduction

<p align="center">
    <img src="https://cdn.sanity.io/images/v6v65cpt/production/b0160daf2ecb6b5ee3a91d0aa5f8df7e151c34b7-960x614.png" width=700>
</p>

[*Figure 1: DevOps tech stack*](https://cdn.sanity.io/images/v6v65cpt/production/b0160daf2ecb6b5ee3a91d0aa5f8df7e151c34b7-960x614.png)

As a software developer, we are expected to be able to quickly learn various softwares and tools besides programming languages to support our work. If you're someone like me who at some point has heard of a technology called "containers" and either did not know where to start or found it too intimidating to even start using it, I hope this short article will help you get your feet wet.

## 2. What even are containers and why do we use them?

<p align="center">
    <img src="https://img.freepik.com/free-photo/shipping-industry-delivering-cargo-large-container-ship-generative-ai_188544-9112.jpg?w=2000" width=700>
</p>

[*Image source*](https://img.freepik.com/free-photo/shipping-industry-delivering-cargo-large-container-ship-generative-ai_188544-9112.jpg?w=2000)

If you do a quick Google search on "What are containers in software development?", it defines containers as "A container is a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another" ([*1*](https://www.docker.com/resources/what-container/)). Now, I must admit that the definition is as concise as it gets, but to beginners, it is still a bit vague to imagine how the technology works and what the use cases for it. I believe it is easier to understand these concepts by going through a scenario.

Imagine you are a Python data scientist working on a project. Your working machine has Python 3.10, with the packages (dependencies) `numpy==1.0.` and `pandas=1.7`. You got all your results and went ahead and handed them over to your supervisor to verify. The person clones your codes and attempts to run it on their machine, and an error pops up not even 2 seconds after running.

"No way!" - you exclaimed, "It worked on my machine! I tested it 10 times!"

Well, it turns out that your supervisor's machine (which is different from your own) is running Python 3.7, and certain features are deprecated, and certain of your codes are no longer compatible.

"Easy, we're just going to upgrade to Python 3.10" - you said, and your supervisor reluctantly agreed.

Your supervisor rerun the codes after the upgrade, surely it has to work now. To your anticipation, the codes work, but your supervisor told you that the results he had is different from yours. It turns out your supervisor's machine has the package `numpy==1.5` where a certain underlying algorithm has changed thus making your results no longer reproducible. 

All of this could have been avoided if you had used a virtual environment and package manager ([Conda](https://docs.conda.io/en/latest/) for example). This would create a virtual Python environment separate from your base Python environment and let you install the specific package version. Thus, any machine that has the Conda software can replicate the exact Python environment you have and install the exact packages you specified, which would ensure **reproducibility** of the software you built.

Now why did I mention this example? It is because the concept of a *container* or *containerized application* is very similar to a virtual environment, but with a **deeper level of virtualized isolation**:

- If a Python virtualenv just isolates different Python runtime and their dependencies (`numpy`,etc), a container virtualized **the filesystem** and any **softwares** you want to include in order for your application to work, including but not limited to: the programming language (node, Python, Java, etc), the packages that can be install with the package manager (npm, pip, etc), tools that can be downloaded via the Command Line Interface (wget, curl, etc).
- A container can contain all the source codes of your application (and it will be the case 99% of the time)
- Containers are isolated on a deeper level (OS Kernel level). An OS kernel is the most important program of any Operating System. It's a bridge between the software and hardware and handle the most vital low-level processes of the machine.

To really nail down the fundamentals of a container, let's go through an analogy

Let's say you want to cook a hard-boiled egg in your home's kitchen. Now you could just use all the kitchen tools in that kitchen, any eggs in the fridge, and cook your dish on the burner stovetop. But in order to cook the exact version of the dish (to the atomic scale), you decide to order a box that contains a specific type of egg (from a specific type of chicken, from a specific farm, you get the idea) instead of just any egg. The box also contains a specific type of pot that you want instead of any regular pot. After you have assembled everything provided to you inside that box, **you cook your stuff on your kitchen's stovetop**. The final dish will still be a boiled egg, but if you were to use the resources in your kitchen instead of the box, you would not arrive at that specific "version" of the disk.

From the analogy, the box that contains the specific resources represents the container with their specified resources. The stovetop represents the OS kernel, since although you used particular resources to cook, you still cook it on your own kitchen's stovetop, instead of from a "containerized" stovetop. Your kitchen represents the entire OS.

### Notes on OS Kernel isolation

When they say containers isolate the computing environment on the OS kernel level, they mean if you run a container intended for the Windows machine on a Mac machine, it wouldn't work because those 2 OSs have different Kernels (Windows kernel for Windows vs. XNU for MacOS).

You can relate back to the analogy, if someone were to use a kitchen with an oven instead of a stovetop, the dish cannot be cooked.

### Containers vs. Container Images

Up to this point, I have been using the term Containers interchangeably with Container Image because they're very similar, but with a few subtle differences. A Container Image is the **snapshot** of all the dependencies and filesystems of the containerized application. They are immutable, which means once they are created, they cannot be modified (hence, Image!). You can, however, create a version of a container image where in each version you modify some components of it. A Container Image can be thought of as an "executable".

When you obtain a Container Image and execute it, a Container is started. The Container is the actual virtualized compute environment where the containerized app is run.

It is also interesting to note that a container that is made for Linux kernel **might* be able to run on XNU (MacOS). This is due to the fact that Docker for Mac spins up an internal Linux Virtual Machine managed by the docker app [1](#references).

#### Side notes

A virtual machine is similar to a container but now it isolates the OS entirely, which means on 1 physical computer you can run multiple different OS with an isolated filesystem on top of your primary OS.

![](https://www.backblaze.com/blog/wp-content/uploads/2018/06/bb-bh-VMs-vs.-Containers-3.jpg)
[*Image source*](https://www.backblaze.com/blog/wp-content/uploads/2018/06/bb-bh-VMs-vs.-Containers-3.jpg)

### Benefits of using container

There are many benefits of using containers:

1. **Isolation**: Containers provide a high level of process and file system isolation. Each container runs in its own environment with its own file system, libraries, and dependencies. This isolation ensures that applications and services within containers do not interfere with each other.

2. **Portability**: Containers (or to be more specific, Container Image)encapsulate applications and their dependencies, making them highly portable across different environments. Developers can create a containerized application on their local machine and be confident that it will run consistently in other environments, such as development, testing, and production.

3. **Consistency**: Containers ensure consistency in the runtime environment. Since all dependencies are packaged within the container, you eliminate the "it works on my machine" problem. This consistency simplifies debugging and troubleshooting.

4. **Scalability**: Containers are lightweight and can be quickly started and stopped. This makes it easy to scale applications up or down in response to changing workloads. Container orchestration tools like Kubernetes help automate scaling and load balancing.

5. **Registry and Version Control**: Container Images can be stored on an image registry (Dockerhub, Amazon ECR), where you can share your images with others and they can pull and deploy your images on their computer.

## 3. Docker tutorial

The theory aside, now we're going to do the hands-on interesting part. In this section, we will be using Docker to run a container locally on our machine. The container will be running a simple Python FastAPI which displays the Iris Dataset when you hit the endpoint.

First of all, what is Docker?

Docker/Docker Desktop is the software that allows you to create, manage and run containers. There are other container software available for free, but Docker is the most well-supported.

If you want to follow hands-on this tutorial, make sure you have [Docker Desktop](https://docs.docker.com/engine/install/) installed. Docker Desktop will install the Docker engine (the brain behind this operation) and a nice desktop GUI. Make sure you have [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed while you're at it if you haven't already.

You can clone the [demo repository](https://github.com/nhantien/fast-api-container-demo) here `nhantien/fast-api-container-demo`.

Directory structure:

```
fast-api-container-demo
├── api
│   ├── Dockerfile
│   ├── application.py
│   ├── asgi.py
│   ├── requirements.txt
│   └── templates
│       └── table.html
└── doc
    ├── blog.md
    └── images

```

For our demo project, you should only be concerned with everything inside the `api/` directory. In short, we are creating a very simple FastAPI in Python that displays the Iris Dataset when you ping an endpoint.

You can now launch the Docker Desktop app, which will run the Docker daemon in the background. Also, open your bash shell and navigate into the `api/` directory.

Notice there's a file called `Dockerfile`. This is a very important file so I want you to pay close attention to it.

This file serves as the template to build your Container Image.

```
FROM --platform=linux/amd64 python:slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "application:app", "--port", "8000" , "--host", "0.0.0.0" ]
```

### Explanations

1. `FROM --platform=linux/amd64 python:slim`: 
A Dockerfile always starts with a `FROM` instruction, which tells Docker the base container image that your image is building on top. This is due to the fact that the Docker container utilized something called **layers**. Every instruction after `FROM` (`WORKDIR`, `COPY`, etc) creates new layers on top of the previous layers. Imagine a stack where the bottom-most is the `FROM` instruction. This allows Docker to cache existing layers and prevents you from building a brand new image every single time you make a tiny change. If you change an instruction, then it and every instruction downstream (below) have to be re-executed (thus those layers are rebuilt), which will take A LOT OF TIME. Consequently, if you already built the image from the Dockerfile and immediately rebuilt, nothing will be executed because all of those instructions are unchanged (assuming the instructions in the Dockerfile are unchanged). Here, `python:slim` is pointing to a specific Docker official base image for Python with the tag `slim`. The indicator `--platform=linux/amd64` means that the docker image being built is intended to be run on a Linux machine. However, I personally run it fine on my Macbook. If you're on Windows and find yourself running into trouble, try getting rid of that indicator and rebuild your image.

2. `WORKDIR /usr/src/app`:
This is equivalent to a `cd` command in Bash. It basically says to navigate to a directory `/usr/src/app`. If that directory does not exist inside the container, it will be created. Then it sets the current working directory inside the container to be that directory.

3. `COPY requirements.txt ./`:
This instruction will copy the file called `requirements.txt` from the current build context (the current folder) into the current WORKDIR of the container (`./` means current folder in the container, or you can specify `/usr/src/app` directly). Note that the build context is the current folder where you have `cd` in earlier from your computer's bash shell (`api/`).

4. `RUN pip install --no-cache-dir -r requirements.txt`:
This `RUN` command starts a shell session **inside the container** and runs the `pip install` bit, similar to how you run `pip install` on your own bash shell to install Python packages.

5. `COPY . .`:
Again, this command will copy all source code files (`.`) in the current build context of the host machine (`api/`) into the container's current WORKDIR. Notice how we copy the source code into the container only after we have installed the Python packages earlier. This is to take advantage of image layer caching as mentioned above. If your COPY instruction that transfers the source codes occurs before the RUN command that installs packages, then every time you make changes to the source code on your local machine and rebuild the image, you would have to reinstall everything in your container (takes a lot of time).

6. `EXPOSE 8000`:
This command exposes port 8000 of the container so that it can listen for **internal** traffic on that port. We chose 8000 since FastAPI defaults to port 8000.

7. `CMD [ "uvicorn", "application:app", "--port", "8000" , "--host", "0.0.0.0" ]`:
The `CMD` instruction tells the Docker engine to execute  the shell command inside the array when a container is launched. Notice how you have to break up the shell command into comma-separated chunks. The shell command here basically starts a uvicorn process for our FastAPI. If you were to run the command `uvicorn application:app --port 8000 --host "0.0.0.0"` right now on your own bash terminal instead it will launch the FastAPI in your browser on `0.0.0.0:8000`.

### Docker commands

To build your Docker image, run this on your bash terminal (make sure you're inside the `api/` directory). This command will build the image base on all the files (`.`) in the `api/` directory. The image name is `fast-api` with the tag `latest`

```bash
docker build -t fast-api:latest .
```

When the image is created, you can run a container from that image by running this command in your bash terminal. This command runs a container from the image we built earlier. `-d` means it's running in detached mode (the container is running in the background). `-p 8000:8000` map the **exposed port 8000 of the container** to **your computer port 8000**. You can map to your computer port 3000 or any other available port instead for example `-p 3000:8000`.

```bash
docker run -d -p 8000:8000 fast-api:latest
```

After that is done, you can navigate to `localhost:8000` on your browser and see the message: 

```json
{"Status":"200 (OK)","Message":"API deployed successfully!"}
```

*Bonus*: You can also hit the `localhost:8000/data` url to see the Iris Dataset displayed.

**Congratulations, you have successfully completed your first Docker demo!**

## 4. Amazon ECS tutorial

[Amazon ECS](https://aws.amazon.com/ecs/) is a container orchestrator service that allows you to automatically create, manage, and scale millions of containers for your microservice architecture. In the real world, millions of organizations build their services with containers since they are very maintainable and scalable. But the challenging aspect is to manage and scale millions of them automatically and gracefully handle disasters and service downtime. This is where container orchestrator like Amazon ECS comes into play.

![](https://devopedia.org/images/article/37/8935.1530784562.jpg)
*Figure 4: Example of container orchestrators* ([source](https://devopedia.org/images/article/37/8935.1530784562.jpg))

### Prerequisites

- An AWS account
- A VPC with Public subnet and internet gateway enabled.
- AWS CLI on your local computer

You can now hop straight onto the AWS console and start hacking!

### Tutorial walkthrough

#### Step 1: Push your Docker container image to ECR.

For ECS to build the container, it needs access to your image through ECR. ECR is basically the equivalent of Dockerhub to store Docker container images on the cloud.

Go to the ECR console:

1. Hit `Create repository`.
2. Select `Private` for `Visibility settings``.
3. Set `fast-api` as `Repository name`.
4. Hit `Create repository`.

#### Step 2: Build the image and push it to ECR

Your repository should now be created. Navigate to it by clicking on its name in the list of private repositories. To push an image locally to that repo:

1. Click on `View push commands` (on the top right of the page)
2. Follow the appropriate commands for your machine version. If you're stuck on the step where it authenticates your shell session to the ECR repo, try to specify `--profile` with the appropriate AWS CLI in the CLI calls to ECR.
3. After you're done the image will appear inside the repo with the size of approximately 103 MB.

#### Step 3: Create the ECS cluster

Now navigate to the ECS console:

1. On the `Cluster` tab, hit `Create cluster`. A cluster is just an abstraction over a group of managed containers.
2. For `Cluster name`, call it something like `fast-api-cluster`
3. For `Infrastructure`, select `AWS Fargate`. If you're familiar with EC2 then Fargate is serverless EC2, which means you're not paying for the cost of owning the instance like EC2. (We will discuss about EC2 vs. Fargate later).
4. Hit `Create`.

#### Step 4: Create a Task Definition

Your cluster should now be there. Now you need to create a Task definition, which is an abstraction over the deployment configurations of the containers in your cluster. On the left tab, navigate to `Task definitions`:

1. `Create new task definition`
2. Provide the `Task definition family`, call it `fast-api-task-def`
3. Under `Infrastructure requirements` > `Launch type`, choose `AWS Fargate`.
4. You can keep other settings under `Infrastructure requirements` with their default values.
**Note:** Task Role vs Task Execution Role. A **Task Role** is for the container running your code to be able to execute API calls to other AWS services programmatically with the SDK like [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html). **Task Execution Role** is for the ECS container agent (part of the ECS service) to manage the containers in your cluster.
5. Now we specify container-level configurations. Under `Container 1`, name it `fast-api-container`, then provide the `Image URI` with the correct URI from the ECR repo that we pushed earlier for our fast-api image.
6. Under container port, add a port mapping with port 8000, and keep other default details.
7. You can provide other configs such as memory and CPU reservations for the container, environment variables, etc. But for now, we'll keep the default settings.
8. Scroll down to the bottom and hit `Create`. The task definition should be created.

#### Step 5: Start a Service

We're very close to completion now. Navigate to the `Cluster` tab and select the `fast-api-cluster` we created earlier.

1. Select `Services` (not `Tasks`, we will discuss the differences later).
2. Create a new Service by clicking `Create`
3. Keep default values in `Environment` section
4. Under `Deployment configuration`, provide the `Family` of the task definition with `fast-api-task-def` we created earlier. Make sure the version of the task def is `Latest`.
5. Under `Service name`, call it `fast-api-service`
6. Under the `Networking` section, select the VPC in your account that has **public subnets and internet gateway enabled**. This is not the best security practice, but for the sake of the demo, we need this for the deployment to work.
7. Under `Security group`, create a new Security group. Provide the name and the description of the sg. Under `Inbound rules`, select `All traffic` for `Type`, and `Anywhere` for `Source`. Make sure you have `Public IP` turned on. Again, these settings are not best practices, but we'll proceed with this demo.
8. Scroll down the bottom and hit `Create`.

#### Step 6: Access the newly deployed API

You should see a Service being created. If the Service is successfully deployed, it will show green on the `Deployment and tasks` bar. Note that it might take a while to be deployed.

When it shows green:
1. Click on `fast-api-service` that was created.
2. If you check the `Logs` tab, you should see the Uvicorn's server logs
3. Click on the `Tasks` tab, then select the running Task with a random string.
4. You will see `Container details for fast-api-container` mini-tab, click on `Network bindings`, select the link with the IP address on port 8000 (e.g. `<ip-address>:8000`), and open it on a new browser tab.
5. You will see our FastAPI has been deployed.

#### Step 7: Cleaning Up

To stop clean-up, simply stop the Service, then delete the associated Cluster and Task Definition. Then go to ECR and delete the repository.

### Congratulation!!!

### Good to know:

- *Service* vs *Task*:
  - A Task is an abstraction over a group of containers doing a computation task. Think of it as similar to a Lambda Function but has a longer timeout, in fact, it has no timeout limit, It exits when an error occurs when the script you're running finished executing, or you abort the execution manually. It's suitable for a periodical, short-term task like fetching data from an API and storing it in a database.
  - A Service can be thought of as a long-running/long-term Task. It's suitable for web servers where it needs to be constantly run 24/7.

- *Fargate* vs *EC2* launch type:
  - *EC2* is essentially running your container cluster on an EC2 instance managed by you. So you should either have an EC2 instance already running or you're willing to have one provided for you. You will be charged for as long as the EC2 instance is still running, regardless of whether or not your cluster stops working/exits.
  - *Fargate* is serverless EC2. The infrastructure will be provided to you on demand without you managing anything and will be automatically reclaimed when your containers exit. That way you're not being charged for idle time.
  - In my opinion, Fargate is suitable for running short-term Tasks since it offloads a lot of the management involved in EC2. But For running long-term Service, it could be more cost-beneficial to run on EC2, however, you would need to decide whether the cost saving is worth the time managing your own EC2 fleets.

## Conclusion

Containers are one of the most popular tools for Software Engineers, and this demo is just a tiny fraction of what this technology can offer.
To sum it all up, here are all the benefits of containers and container orchestration services (we might not have seen all these benefits just yet since our demo deployment is so small in scale):

### Benefits of containers

1. **Isolation**: Containers provide process and filesystem isolation, ensuring that applications and their dependencies do not interfere with each other. This isolation helps prevent compatibility issues and simplifies dependency management.

2. **Portability**: Containers encapsulate applications and dependencies, making them highly portable across different environments, from development to production. This consistency minimizes "it works on my machine" problems.

3. **Resource Efficiency**: Containers share the host operating system's kernel and libraries, reducing resource overhead compared to traditional virtualization. This efficiency allows for higher resource utilization.

4. **Version Control**: Container images can be versioned, making it easy to track changes and roll back to previous versions if issues arise during deployment.

5. **Scaling**: Containers can be quickly started and stopped, making it easier to scale applications up or down in response to changing workloads.

6. **Microservices**: Containers are a natural fit for microservices architectures, where applications are broken into smaller, independently deployable services. Each service can run in its own container, simplifying deployment and scaling.

### Benefits of Container Orchestration services (ECS, Kubernetes, etc.)

1. **Orchestration**: Container orchestrators automate the deployment, scaling, and management of containerized applications. They ensure that containers are placed on the appropriate nodes, monitor their health, and replace failed containers.

2. **Load Balancing**: Orchestrators provide built-in load-balancing methods to distribute incoming traffic across multiple containers or pods, ensuring high availability and improved performance.

3. **Auto Scaling**: Orchestrators can automatically scale the number of containers or pods based on resource utilization or user-defined metrics, ensuring optimal resource allocation.

4. **Self-Healing**: Orchestrators detect and replace failed containers or pods, reducing downtime and minimizing manual intervention.

5. **Rolling Updates**: Orchestrators support rolling updates and canary deployments, allowing you to update applications with minimal disruption and the ability to roll back if issues arise.

6. **Service Discovery**: Orchestrators provide service discovery mechanisms that allow containers to discover and communicate with each other by name, making it easier to build distributed applications.

7. **Secrets Management**: Orchestrators offer secure ways to manage and distribute secrets and sensitive configuration data to containers, enhancing security and compliance.

8. **Resource Optimization**: Orchestrators optimize resource utilization by scheduling containers or pods on nodes with available resources, reducing operational costs.

9. **Multi-Cloud and Hybrid Deployments**: Orchestrators enable multi-cloud and hybrid cloud deployments, allowing you to run containers in various environments while maintaining consistent management and orchestration.

## 5. Acknowledgment

I would like to express my immense gratitude to the [UBC Cloud Innovation Centre](https://cic.ubc.ca/) for the valuable opportunities to learn more about AWS. This work would not have been possible without their guidance and support!

## 6. References

1. https://collabnix.com/how-docker-for-mac-works-under-the-hood/
2. https://developer.ibm.com/articles/true-benefits-of-moving-to-containers-1/
3. https://www.ibm.com/topics/container-orchestration
4. General ECS Guide: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html
5. General Docker Documentation: https://docs.docker.com/get-started/overview/
