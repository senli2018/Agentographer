# FastAPI Application Production Deployment Guide

This document provides detailed instructions for deploying a FastAPI application in a production environment using nohup.

## Deployment Scripts Overview

This project includes the following deployment scripts:

1. `deploy.sh` - Starts the application in the background using nohup
2. `stop.sh` - Stops the running application
3. `restart.sh` - Restarts the application
4. `status.sh` - Checks the application's running status
5. `logs.sh` - Views application logs

## Prerequisites

1. Ensure Python and required dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure scripts have execution permissions:
   ```bash
   chmod +x *.sh
   ```

3. Ensure the .env file is properly configured (production environment settings)

## Deploying the Application

### Starting the Application

Use the following command to start the application:

```bash
./deploy.sh
```

The application will run in the background, with logs written to the `logs/app.log` file.

### Checking Application Status

Use the following command to check the application's running status:

```bash
./status.sh
```

This will display whether the application is running, its PID, memory usage, runtime, and recent logs.

### Viewing Application Logs

Use the following commands to view application logs:

```bash
./logs.sh        # View application logs (last 50 lines)
./logs.sh -e     # View error logs
./logs.sh -f     # Continuously view log updates
./logs.sh -n 100 # View the last 100 lines of logs
```

More options can be viewed through `./logs.sh --help`.

### Stopping the Application

Use the following command to stop the application:

```bash
./stop.sh
```

### Restarting the Application

Use the following command to restart the application:

```bash
./restart.sh
```

## Auto-start (Optional)

To automatically start the application at system boot, add the following command to crontab:

```bash
@reboot cd /path/to/your/app && ./deploy.sh
```

Use the following command to edit crontab:

```bash
crontab -e
```

## Troubleshooting

1. If the application fails to start, check the error logs:
   ```bash
   ./logs.sh -e
   ```

2. If the PID file exists but the application is not running:
   ```bash
   ./status.sh  # This will automatically clean up expired PID files
   ```

3. If you need to force stop the application:
   ```bash
   ./stop.sh    # The script will attempt to forcefully terminate after normal stop fails
   ```

## Notes

1. These scripts are designed for Linux/Unix environments and may need adjustments for Windows
2. Ensure the server firewall allows the port used by the application (default is 8000)
3. For production environments, it's recommended to configure a reverse proxy (like Nginx) and SSL certificates 