# The Patient Manager

The Patient Manager is a Python application designed to manage doctors, patients, and appointments in a clinic setting. This application provides a user-friendly graphical interface to interact with the underlying database, allowing for efficient management of medical records.

## Project Structure

```
thePatientManager
├── database.py          # Contains database initialization and management classes
├── gui                  # GUI package for the application
│   ├── __init__.py     # Initialization file for the GUI package
│   ├── main_window.py   # Main application window and navigation
│   ├── doctors_view.py  # User interface for managing doctors
│   ├── patients_view.py # User interface for managing patients
│   └── appointments_view.py # User interface for managing appointments
├── requirements.txt     # Lists project dependencies
└── README.md            # Project documentation
```

## Features

- **Manage Doctors**: Add, update, delete, and view doctor records.
- **Manage Patients**: Add, update, delete, and view patient records.
- **Manage Appointments**: Schedule, update, delete, and view appointments.

## Requirements

To run this project, you need to install the following dependencies:

- Python 3.x
- SQLite3
- A GUI library (e.g., Tkinter or PyQt)

You can install the required libraries by running:

```
pip install -r requirements.txt
```

## Usage

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the application by executing the main window script:

```
python gui/main_window.py
```

4. Use the interface to manage doctors, patients, and appointments.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.