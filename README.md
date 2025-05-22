# Feast Rocks

This repository contains OCI Rock definitions for the [Feast](https://feast.dev/) feature store, packaged for secure, repeatable deployment. Rocks are minimal, container-like application images built using [Rockcraft](https://canonical.com/rocks), designed for simplicity and immutability.

Currently, this repository includes the `feast-ui` rock, which provides a web-based user interface for exploring and managing features in a Feast store.

## 🧱 Feast UI Rock

The `feast-ui` rock packages the Feast UI as a standalone service. It includes:

- Python 3.10 environment
- All required Python packages from `requirements.txt`
- A non-root `ubuntu` user for running the service securely

Service definition:

```yaml
services:
  feast-ui:
    summary: "Feast web UI service for managing feature store metadata"
    command: feast ui
    user: ubuntu
    working-dir: /home/ubuntu
