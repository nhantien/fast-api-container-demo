<h1 style="text-align: center;">Containers, Docker and Amazon ECS</h1>

<h2>Table of Content</h2>

- [1. Introduction](#1-introduction)
- [2. What even are containers and why do we use them?](#2-what-even-are-containers-and-why-do-we-use-them)
  - [Notes on OS Kernel isolation](#notes-on-os-kernel-isolation)
  - [Containers vs Container Images](#containers-vs-container-images)
    - [Side notes](#side-notes)
  - [Benefits of using container](#benefits-of-using-container)
- [3. Docker tutorial](#3-docker-tutorial)
- [4. Amazon ECS tutorial](#4-amazon-ecs-tutorial)
- [5. References](#5-references)

## 1. Introduction

<p align="center">
    <img src="https://cdn.sanity.io/images/v6v65cpt/production/b0160daf2ecb6b5ee3a91d0aa5f8df7e151c34b7-960x614.png" width=700>
</p>

[*Figure 1: DevOps tech stack*](https://cdn.sanity.io/images/v6v65cpt/production/b0160daf2ecb6b5ee3a91d0aa5f8df7e151c34b7-960x614.png)

As a software developer, we are expected to be able to quickly learn various softwares and tools besides programming languages to support our work. If you're someone like me who has some point has heard of a technology called "containers" and either did not know where to start, or found it too intimidating to even start using it, I hope this short article will help you get your feet wet.

## 2. What even are containers and why do we use them?

<p align="center">
    <img src="https://img.freepik.com/free-photo/shipping-industry-delivering-cargo-large-container-ship-generative-ai_188544-9112.jpg?w=2000" width=700>
</p>

[*Image source*](https://img.freepik.com/free-photo/shipping-industry-delivering-cargo-large-container-ship-generative-ai_188544-9112.jpg?w=2000)

If you do a quick Google search on "What are containers in software development?", it defines containers as "A container is a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another" ([*1*](https://www.docker.com/resources/what-container/)). Now, I must admit that the definition is as concise as it gets, but to beginners it is still a bit vague to imagine how the technology works and what the use cases for it. I believe it is easier to understand these concepts by going through a scenario.

Imagine you are a Python data scientist and you're working on a project. Your working machine has Python 3.10, with th packages (dependencies) `numpy==1.0.` and `pandas=1.7`. You derived all your results and hand the work them over to your supervisor to verify. The person clone your codes and attempt to run it on their machine, and an error pops up not even 2 seconds of running.

"No way!" - you exclaimed, "It worked on my machine! I tested it 10 times!"

Well, it turns out that your supervisor's machine (which is differ from your own) is running Python 3.7 and certain features are deprecated and thus certain your codes are no longer compatible.

"Easy, we're just going to upgrade to Python 3.10" - you said, and your supervisor reluctantly agreed.

Your supervisor rerun the codes after the upgrade, surely it has to work now. To your anticipation, the codes work, but your supervisor told you that the results he had is different from yours. It turns out your supervisor's machine has the package `numpy==1.5` where a certain underlying algorithm has changed thus making your results no longer reproducible. 

All of this could have been avoided if you had used a virtual environment and package manager ([Conda](https://docs.conda.io/en/latest/) for example). This would create a virtual Python environment separate from your base Python environment and let you install the specific packages version. Thus, any machine that has the Conda software can replicate the exact Python environment you have and install the exact packages your specified, which would ensure **reproducibility** of the software you built.

Now why did I mention this example? It is because the concept of a *container* or *containerized application* is very similar to a virtual environment, but with a **deeper level of virtualized isolation**:

- If a Python virtualenv just isolate different Python runtime and there dependencies (`numpy`,etc), a container virtualized **the filesystem** and any **softwares** you want to include in order for your application to work, including but not limited to: the programming language (node, Python, Java, etc), the packages that can be install with the package manager (npm, pip, etc), tools that can be downloaded via the Command Line Interface (wget, curl, etc).
- A container can contains all the source codes of your application (and it will be the case 99% of the time)
- Containers are isolated on a deeper level (OS Kernel level). An OS kernel is the most important program of any Operating System. It's a bridge between the software and hardwares and handle the most vital low-level processes of the machine.

To really nail down the fundamentals of a container, let's go through an analogy

Let's say you want to cook a hard boil egg in your home's kitchen. Now you could just use all the kitchen tools in that kitchen, any eggs in the fridge and cook your dish on the burner stovetop. But in order to cook the exact version of the dish (to the atomic scale), you decide to order a box that contains a specific type of egg (from a specific type of chicken, from a specific farm, you get the idea) instead of just any egg. The box also contain a specific type of pot that you want instead of any regular pot. After you have assembled everything provided to you inside that box, **you cook your stuff on your kitchen's stovetop**. The final dish will still be boiled egg, but if you were to use the resources in your kitchen instead from the box, you would not arrive at that specific "version" of the disk.

From the analogy, the box that contains the specific resources represent the container with their specified resources. The stovetop represent the OS kernel, since although you used particular resources to cook, you still cook it on your own kitchen's stovetop, instead of from a "containerized" stovetop. Your kitchen represents the entire OS.

### Notes on OS Kernel isolation

When they say containers isolate the compute environment on the OS kernel level, they mean if you run a container intended for the Windows machine on a Mac machine, it wouldn't work because those 2 OSs have different Kernels (Windows kernel for Windows vs XNU for MacOS).

You can relate back to the analogy, if someone was to use a kitchen with an oven instead of stovetop, the dish cannot be cooked.

### Containers vs Container Images

Up to this point, I have been using the term Containers interchangeably with Container Image because they're very similar, but with a few subtle differences. A Container Image is the **snapshot** of all the dependencies and filesystem of the containerized application. They are immutable, which means once they are created, they cannot be modified (hence, Image!). You can, however, create version of a container image where in each version you modify some components of it. A Container Image can be thought of as an "executable".

When you obtain a Container Image and execute it, a Container is started. The Container is the actual virtualized compute environment where the containerized app is run.

It is also interesting to note that a container that is made for Linux kernel **might* be able to run on XNU (MacOS). This is due to the fact that Docker for Mac spin up an internal Linux Virtual Machine managed by the docker app [1](#references).

#### Side notes

A virtual machine is similar to a container but now it isolate the OS entirely, which means on 1 physical computer you can run multiple different OS with isolated filesystem on top of your primary OS.

![](https://www.backblaze.com/blog/wp-content/uploads/2018/06/bb-bh-VMs-vs.-Containers-3.jpg)
[*Image source*](https://www.backblaze.com/blog/wp-content/uploads/2018/06/bb-bh-VMs-vs.-Containers-3.jpg)

### Benefits of using container

There are many benefits of using containers:

1. **Isolation**: Containers provide a high level of process and file system isolation. Each container runs in its own environment with its own file system, libraries, and dependencies. This isolation ensures that applications and services within containers do not interfere with each other.

2. **Portability**: Containers (or to be more specific, Container Image)encapsulate applications and their dependencies, making them highly portable across different environments. Developers can create a containerized application on their local machine and be confident that it will run consistently in other environments, such as development, testing, and production.

3. **Consistency**: Containers ensure consistency in the runtime environment. Since all dependencies are packaged within the container, you eliminate the "it works on my machine" problem. This consistency simplifies debugging and troubleshooting.

4. **Scalability**: Containers are lightweight and can be quickly started and stopped. This makes it easy to scale applications up or down in response to changing workloads. Container orchestration tools like Kubernetes help automate scaling and load balancing.

5. **Registry and Version Control**: Container Images can be store on a image registry (Dockerhub, Amazon ECR), which you can share your images with others and they can pull and deploy your images on their computer.

## 3. Docker tutorial

Theory behind, now we're going to do the hands-on interesting part. In this section, we will be using Docker to run a container locally on our machine. The container will be running a simple Python FastAPI which display the Iris Dataset when you hit the endpoint.

First of all, what is Docker?

Docker/Docker Desktop is the software that allow you to create, manage and run containers. There are other container softwares available for free, but Docker is the most well-supported.

If you want to follow hands-on this tutorial, make sure you have [Docker Desktop](https://docs.docker.com/engine/install/) installed. Docker Desktop will install the Docker engine (the brain behind this operation) and a nice desktop GUI. Make sure you have [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed while you're at it if you haven't already.

You can clone the demo repository here `nhantien/fast-api-container-demo`.

Directory structure:



## 4. Amazon ECS tutorial

## 5. References

1. https://collabnix.com/how-docker-for-mac-works-under-the-hood/