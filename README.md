# Overview
This repository contains the source code for DTApp, a Flask-based application that allows users to upload and process Terraform state files.

For security reasons, the state file is ignored and will not be committed.

To read on how to stress test it, please navigate to [section 7](#7-Stress-Tesing)

# Table of Contents
- [Project Structure](#1-Project-Structure)
- [Requirements](#2-Requirements)
- [Getting Started](#3-Getting-Started)
- [Endpoints](#4-Endpoints)
- [Rate Limiting](#5-Rate-Limiting)
- [How To Use](#6-HOW-TO-USE)
- [Stress Tesing](#7-Stress-Tesing)
- [License](#8-License)

## 1. Project Structure

```
.
├── app
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── nginx
│   ├── Dockerfile
│   └── nginx.conf
├── test
│   └── stress.js
├── README.md
├── your_terraform_state.json
└── docker-compose.yaml
```

`your_terraform_state.json` should be the actual Terraform state file.

## 2. Requirements

- Make sure you have `docker` installed
- ake sure you have `docker-compose` installed
- Make sure you have `k6` installed
- Ensure to modifiy the file name in `stress.js` file (line 5 & 43) in `test` directory to match the actual filename.
- Put the terraform state file at the root directory

## 3. Getting Started

1. **Clone the Repository**:

   ```bash
   git clone git@github.com:alioujalloh/DTApp.git
   cd DTApp
   ```

2. **Create a custom local domain**:

   You can open `etc/hosts` using:
   ```
   sudo vi /etc/hosts
   ```
   Then add the entry and save: 
   `127.0.0.1     dt-app.info`

3. **Build and Run with Docker Compose**:

   ```
   docker-compose up --build -d
   ```

   This will start the Flask app and the Nginx server. The Nginx server will handle rate limiting for `/upload` location and proxy requests to the Flask app.

4. **Access the Application**:

   After starting the services, you can access the app at:
   ```
   http://dt-app.info:8080"
   ```
 

## 4. Endpoints

- `/`: A welcome page with instructions.
  
- `/upload`: Endpoint to upload Terraform state files.

## 5. Rate Limiting

Requests to the `/upload` endpoint are rate-limited using Nginx. Please ensure not to send requests too frequently to avoid being rate-limited :).
You can test the rate limiting by following [section 7 guide](#7-Stress-Tesing). Currently, the limit is set to 10 requests per second plus 5 bursts.

## 6. HOW TO USE

For this app, we can filter by `attribute value` but we can also filter by both `attribute key` and `attribute value` to be more precise.
Below are few examples, ensure to replace `your_terraform_state.json` with the actual state filename:

1. **Get the welcome message and know what is the app for**:
   ```
   curl -X GET "http://dt-app.info:8080"
   ```
2. **Get all security groups within the provided Terraform state file**:
   ```
   curl -X POST -F "file=@your_terraform_stae.json" "http://dt-app.info:8080/upload"
   ```
3. **Get all security groups that have sg-12345678 in their attributes**:
   ```
   curl -X POST -F "file=@your_terraform_stae.json" "http://dt-app.info:8080/upload?attribute_filter=sg-12345678"
   ```
   Ensure to replace sg-12345678 with the actual value.

4. **Get all security groups with specific attribue key and attribute value**:
   ```
   curl -X POST -F "file=@your_terraform_state.json" "http://dt-app.info:8080/upload?attribute_key=type&attribute_value=ingress"
   ```

## 7. Stress Tesing

### 7.1. Setting up the Test

Navigate to `test` directory where the `stress.js` script is located.

### 7.2. Running the Test Scenarios

These are few examples for all 3 cases that we have:

1. **Get all Security Groups**:
    This scenario tests the ability to retrieve all the data.
    ```bash
    k6 run -e ENDPOINT=getall stress.js
    ```

2. **Filter by Attribute Value**:
    This scenario tests the filtering of data based on a specific attribute value. Ensure to change sg-12345678 with the actual attribute value.
    ```bash
    k6 run -e ENDPOINT=attribute_value_filter -e filterValue=sg-12345678 stress.js
    ```

3. **Filter by Attribute key and Value**:
    This scenario tests the filtering based on both attribute key and value.
    ```bash
    k6 run -e ENDPOINT=attribute_key_and_value_filter -e attribute_key=type -e attribute_value=ingress stress.js
    ```

### 7.3. Checking Results

After each test run, k6 will provide a summary of the results in the terminal. Look for important metrics like checks, request durations, number of failed requests, and more. 



## 8. License

This project is open-source and available under the [MIT License](https://github.com/alioujalloh/DTApp/blob/main/LICENSE).
