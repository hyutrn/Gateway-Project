# Gateway for IoT Garden Project

This project create a gateway can control multi node device,...

## Features


## Directory Structure


### File Structure
- `README.md`: Description and usage information for the server.

## Getting Started

### Prerequisites

- Windows OS (for Winsock API).
- Code editor (e.g., VSCode).
- C++ compiler (e.g., MSVC, MinGW).
- CMake (for building the project).

### Installation

1. Clone the repository:
    ```bash
        git clone https://github.com/hyutrn/Gateway-Project
    ```
2. Install the required packages from the requirements.txt file. Run the following command:
    ```bash
        pip install -r requirements.txt
    ```
3. Run Server:
    + Terminal 1:
    ```bash
        python3 main.py
    ```
    + Terminal 2:
    ```bash
        python3 mqttclientGET.py
4. Open a web browser and navigate to the following address:

    ```[link]
        http://127.0.0.1:3001
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
