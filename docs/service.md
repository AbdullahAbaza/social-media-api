# **Systemd Service File for FastAPI with Gunicorn**

This guide explains how to create and configure a systemd service file to run a FastAPI application using Gunicorn. The service ensures that your application starts automatically on system boot, restarts in case of failures, and runs in a controlled environment.

---

## **Table of Contents**
1. [What is a Systemd Service File?](#what-is-a-systemd-service-file)
2. [Service File Breakdown](#service-file-breakdown)
   - [Unit Section](#unit-section)
   - [Service Section](#service-section)
   - [Install Section](#install-section)
3. [Steps to Set Up the Service](#steps-to-set-up-the-service)
4. [Troubleshooting](#troubleshooting)
5. [Example `.env` File](#example-env-file)
6. [FAQs](#faqs)

---

## **What is a Systemd Service File?**
A systemd service file is a configuration file that defines how a service should be managed by the systemd init system. It specifies:
- How and when the service should start.
- What commands to run.
- What environment variables to use.
- How to handle failures and restarts.

Systemd is the default init system for most modern Linux distributions (e.g., Ubuntu, Debian, CentOS).

---

## **Service File Breakdown**

Below is a fully documented systemd service file for running a FastAPI app with Gunicorn. Each section and directive is explained in detail.

### **Service File: `/etc/systemd/system/fastapi.service`**
```ini
[Unit]
Description=Gunicorn instance to serve FastAPI application
After=network.target

[Service]
User=fastapi
Group=fastapi
WorkingDirectory=/home/fastapi/app/src/
Environment="PATH=/home/fastapi/app/src/.venv/bin"
EnvironmentFile=/home/fastapi/.env
ExecStart=/home/fastapi/app/src/.venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

---

### **Unit Section**
The `[Unit]` section defines metadata and dependencies for the service.

- **`Description`**: A brief description of the service. This is displayed when you check the service status.
  ```ini
  Description=Gunicorn instance to serve FastAPI application
  ```

- **`After`**: Ensures the service starts after the specified target. In this case, the service starts after the network is available.
  ```ini
  After=network.target
  ```

---

### **Service Section**
The `[Service]` section defines how the service should run.

- **`User` and `Group`**: The service runs under the specified user and group. Replace `fastapi` with the appropriate user and group.
  ```ini
  User=fastapi
  Group=fastapi
  ```

- **`WorkingDirectory`**: The directory where your application code is located.
  ```ini
  WorkingDirectory=/home/fastapi/app/src/
  ```

- **`Environment`**: Adds the virtual environment's `bin` directory to the `PATH`. This ensures that Gunicorn and other binaries can be found.
  ```ini
  Environment="PATH=/home/fastapi/app/src/.venv/bin"
  ```

- **`EnvironmentFile`**: Loads environment variables from a file (e.g., `/home/fastapi/.env`). This is useful for storing sensitive data like database credentials or API keys.
  ```ini
  EnvironmentFile=/home/fastapi/.env
  ```

- **`ExecStart`**: The command to start Gunicorn. Replace `/home/fastapi/app/src/.venv/bin/gunicorn` with the path to the `gunicorn` executable in your virtual environment. The `app.main:app` argument specifies the FastAPI app instance.
  ```ini
  ExecStart=/home/fastapi/app/src/.venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
  ```

- **`ExecReload`**: Gracefully reloads the service by sending a `HUP` signal.
  ```ini
  ExecReload=/bin/kill -s HUP $MAINPID
  ```

- **`Restart`**: Ensures the service automatically restarts if it stops or crashes.
  ```ini
  Restart=always
  ```

- **`KillMode`**: Uses a mix of signals to stop the service gracefully.
  ```ini
  KillMode=mixed
  ```

- **`TimeoutStopSec`**: Sets a 5-second timeout for stopping the service.
  ```ini
  TimeoutStopSec=5
  ```

- **`PrivateTmp`**: Provides the service with a private `/tmp` directory for isolation.
  ```ini
  PrivateTmp=true
  ```

---

### **Install Section**
The `[Install]` section defines how the service should be enabled.

- **`WantedBy`**: Specifies the target under which the service should be started. `multi-user.target` is a common target for server applications.
  ```ini
  WantedBy=multi-user.target
  ```

---

## **Steps to Set Up the Service**

1. **Create the Service File**:
   Save the configuration to `/etc/systemd/system/fastapi.service`:
   ```bash
   sudo nano /etc/systemd/system/fastapi.service
   ```

2. **Reload systemd**:
   Reload systemd to recognize the new service:
   ```bash
   sudo systemctl daemon-reload
   ```

3. **Start the Service**:
   Start the service:
   ```bash
   sudo systemctl start fastapi
   ```

4. **Enable the Service**:
   Enable the service to start automatically on boot:
   ```bash
   sudo systemctl enable fastapi
   ```

5. **Check the Status**:
   Verify the service is running:
   ```bash
   sudo systemctl status fastapi
   ```

---

## **Troubleshooting**

- **Service Fails to Start**:
  Check the logs for errors:
  ```bash
  sudo journalctl -u fastapi
  ```

- **Port Already in Use**:
  If port `8000` is already in use, change the port in the `ExecStart` line (e.g., `--bind 0.0.0.0:8001`).

- **Permissions Issues**:
  Ensure the `fastapi` user and group have the necessary permissions to access the app directory, virtual environment, and `.env` file.

---

## **Example `.env` File**

Ensure your `.env` file (located at `/home/fastapi/.env`) contains the necessary environment variables for your application. For example:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase
DEBUG=False
SECRET_KEY=your_secret_key
```


### **How do I reload the service after making changes?**
Use the following command:
```bash
sudo systemctl restart fastapi
```

### **How do I disable the service?**
To disable the service from starting on boot:
```bash
sudo systemctl disable fastapi
```



---

## **FAQs**

### **What is `WantedBy=multi-user.target`?**
It specifies that the service should start automatically when the system reaches the `multi-user.target` state (a common state for servers without a graphical interface).



The `WantedBy=multi-user.target` directive in a systemd service file specifies the **target** that the service should be started under. In systemd, a **target** is a grouping of services that define a system state or runlevel. Here's a detailed explanation of its purpose:

---

### **Purpose of `WantedBy=multi-user.target`**

1. **Defines When the Service Should Start**:
   - The `WantedBy` directive creates a symbolic link from the service to the specified target.
   - When the target (in this case, `multi-user.target`) is activated, the service will be started automatically.

2. **Multi-User Target**:
   - `multi-user.target` is a systemd target that represents a **multi-user system state without a graphical interface** (similar to runlevel 3 in traditional SysV init systems).
   - It is commonly used for servers or headless systems where a graphical interface is not required.

3. **Automatic Start on Boot**:
   - By setting `WantedBy=multi-user.target`, the service is enabled to start automatically when the system reaches the `multi-user.target` state during boot.
   - This ensures that your FastAPI application (or any other service) starts automatically when the system boots up.

4. **Dependency Management**:
   - The `multi-user.target` is a high-level target that depends on other essential targets (e.g., `network.target`, `basic.target`).
   - By associating your service with `multi-user.target`, you ensure that all necessary dependencies (e.g., networking) are available before your service starts.

---

### **How It Works**
- When you enable the service using `systemctl enable <service-name>`, systemd creates a symbolic link from the service file to the `multi-user.target.wants` directory.
- For example, if your service file is named `fastapi.service`, enabling it will create a symbolic link:
  ```bash
  /etc/systemd/system/multi-user.target.wants/fastapi.service -> /etc/systemd/system/fastapi.service
  ```
- During system boot, when `multi-user.target` is activated, systemd will start all services linked to it.

---

### **When to Use `WantedBy=multi-user.target`**
- Use this directive for services that should start automatically on boot and do not require a graphical interface.
- Examples include web servers (e.g., FastAPI, Flask), database servers, background workers, and other headless services.

---

### **Other Common Targets**
While `multi-user.target` is the most common for server applications, there are other targets you might use depending on your use case:
- **`graphical.target`**: Used for systems with a graphical interface (similar to runlevel 5).
- **`default.target`**: The default target for the system, which is often an alias for `multi-user.target` or `graphical.target`.
- **`network.target`**: Ensures the service starts after networking is available.
- **`basic.target`**: A minimal target that provides basic system functionality.

---

### **Example in Context**
Here’s how `WantedBy=multi-user.target` fits into a typical systemd service file for a FastAPI app:

```ini
[Unit]
Description=Gunicorn instance to serve FastAPI application
After=network.target

[Service]
User=fastapi
Group=fastapi
WorkingDirectory=/home/fastapi/app/src/
Environment="PATH=/home/fastapi/app/src/.venv/bin"
ExecStart=/home/fastapi/app/src/.venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

---

### **Steps to Enable the Service**
1. Save the service file to `/etc/systemd/system/fastapi.service`.
2. Enable the service:
   ```bash
   sudo systemctl enable fastapi
   ```
   This creates the symbolic link under `multi-user.target.wants`.
3. Start the service:
   ```bash
   sudo systemctl start fastapi
   ```
4. Verify the service is running:
   ```bash
   sudo systemctl status fastapi
   ```

---

### **Summary**
- `WantedBy=multi-user.target` ensures your service starts automatically when the system reaches the multi-user state during boot.
- It is ideal for server applications that do not require a graphical interface.
- This directive is a key part of making your service persistent across system reboots.
