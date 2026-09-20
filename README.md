# Plumbing Order Management App

A Python desktop application developed to help a refurbishment company organise and manage plumbing material orders and deliveries.

The application allows users to create orders for different job sites, select plumbing materials, add quantities, and generate a unique order ID for each order. Once materials are delivered, users can check each item and mark it as Have, Missing, or Not Checked.

The application also includes an email generation feature that creates ready-to-use messages for placing material orders and reporting missing items. Orders and their delivery statuses are saved locally using JSON, allowing information to remain available when the application is closed and reopened.

The project was created as a practical example of how a simple Python application can be used to digitalise and improve an everyday business process, reducing manual order preparation and making it easier to identify missing materials.

## Features

- Create plumbing material orders
- Add items and quantities
- Generate unique order IDs
- Check delivered and missing items
- Generate order emails
- Generate missing-item emails
- Save orders locally using JSON

## Screenshots

### Create Order
![Create Order](screenshots/create-order.png)

### Check Delivery
![Check Delivery](screenshots/check-delivery.png)

### Messages
![Messages](screenshots/messages.png)

## Technologies

- Python
- Tkinter
- JSON
- PyInstaller

## Download

Windows users can download the `.exe` version and run the application
without installing Python.
