# Haproxy Manager UI

Welcome to the Haproxy Manager UI!

This document provides an overview of the Haproxy Manager UI and its API documentation, enabling you to effectively manage and manipulate HAProxy configurations through a user-friendly interface.

## Table of Contents

- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [HAProxy Class API Documentation](#haproxy-class-api-documentation)
- [Usage Examples](#usage-examples)
- [Acknowledgments](#acknowledgments)

## Quick Start

Getting started with the Haproxy Manager UI is easy! Follow these steps to quickly set up and use the provided `server.py` script for managing your HAProxy configurations through a user-friendly web interface.

### Prerequisites

Make sure you have the following prerequisites installed:

```shell
pip install -r requirements.txt
```

### Step 1: Download the Code

Download or clone the codes from the repository.

### Step 2: Configuration Setup

1. Open the terminal and navigate to the directory containing `server.py`.
2. Launch the Flask web application:

   ```bash
   python server.py
   ```

### Step 3: Access the Web Interface

1. Open your web browser.
2. Enter the following URL in the address bar:

   ```
   http://0.0.0.0:5000/
   ```

   This takes you to the Haproxy Manager UI web interface.

### Step 4: Managing HAProxy Configurations

- **Adding a New Service:**

  Use the "Add Service" section on the web interface to provide details for the new service. Click "Add" to include the service in the HAProxy configuration.

- **Updating an Existing Service:**

  In the "Update Service" section, modify the details of an existing service. Enter the current server name and domain, along with updated information, and click "Update" to apply changes.

- **Deleting a Service:**

  To remove a service, use the "Delete Service" section. Enter the server name and domain of the service to delete, and click "Delete" to remove it from the HAProxy configuration.

- **Restarting HAProxy:**

  If configuration changes require a HAProxy service restart, use the "Restart HAProxy" button to apply changes.

### Note

- Ensure you have necessary permissions to restart the HAProxy service (`service haproxy restart`). Depending on your environment, administrative privileges may be needed.

- Customize the `server.py` script to match your project's specific requirements and integrate it into your workflow.

The Haproxy Manager UI, along with the provided `server.py` script, makes managing HAProxy configurations a hassle-free experience. Enjoy the convenience of a user-friendly interface for configuring and managing your HAProxy setups!

## API Documentation

The Haproxy Manager UI offers a convenient interface for managing and manipulating HAProxy configurations through the `HAProxy` class API.

## HAProxy Class API Documentation

The `HAProxy` class provides an interface for managing and manipulating HAProxy configurations.

### Initialization:

```python
haproxy_config = HAProxy(config_path="/etc/haproxy/haproxy.cfg")
```

- **config_path** (str): Path to the HAProxy configuration file. Default is "/etc/haproxy/haproxy.cfg".

### Attributes:

- `config_path` (str): Path to the HAProxy configuration file.
- `config_str` (str): Content of the HAProxy configuration file.
- `sections` (dict): Parsed sections of the HAProxy configuration.

### Methods:

#### 1. update_backend(server_name, domain, local_port, local_host)

Update the HAProxy configuration by adding or modifying backend configurations.

- **server_name** (str): Name of the server.
- **domain** (str): Domain associated with the server.
- **local_port** (int): Local port on which the backend server runs.
- **local_host** (str): Local host of the backend server.

**Example:**

```python
haproxy_config.update_backend("my_server", "example.com", 8080, "127.0.0.1")
```

#### 2. save() -> str

Return the current HAProxy configuration as a string.

**Example:**

```python
config_str = haproxy_config.save()
print(config_str)
```

#### 3. save_to_file()

Save the current HAProxy configuration to a specified file.

**Example:**

```python
haproxy_config.save_to_file()
```

#### 4. delete_backend(server_name, domain)

Delete the backend configuration for the specified server and domain.

- **server_name** (str): Name of the server.
- **domain** (str): Domain associated with the server.

**Example:**

```python
haproxy_config.delete_backend("my_server", "example.com")
```

#### 5. list_services() -> List[Dict[str, Union[str, int]]]

List all backend services.

Returns a list where each element is a dictionary containing `server_name`, `domain`, `local_port`, and `local_host`.

**Example:**

```python
services = haproxy_config.list_services()
print(services)
```

## Usage Examples

Suppose you want to set up a new backend server named "app_server" for the domain "myapp.com". This server runs on "localhost" at port "3000".

```python
# Initialize the HAProxy object
haproxy_config = HAProxy()

# Update the backend configuration
haproxy_config.update_backend("app_server", "myapp.com", 3000, "127.0.0.1")

# Save the changes to the HAProxy configuration file
haproxy_config.save_to_file()

# If you decide to delete the backend configuration:
haproxy_config.delete_backend("app_server", "myapp.com")
haproxy_config.save_to_file()
```

This example demonstrates how to effortlessly manage your HAProxy configuration using the `HAProxy` class.

## Acknowledgments

- OpenAI
- MetaGPT
