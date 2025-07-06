# How to Start the Digital Goniometry Application

This guide provides simple steps to start and use the Digital Goniometry Application. You do not need to be a programmer to follow these instructions.

## What You Need

*   A computer with macOS (Apple Silicon preferred).
*   A built-in camera or an external webcam.
*   The application files (the folder you downloaded or received).

## Step-by-Step Instructions

### 1. Open the Terminal

*   On your Mac, open the **Terminal** application. You can find it by:
    *   Going to `Applications` > `Utilities` > `Terminal`.
    *   Using Spotlight Search (press `Command + Spacebar`, then type `Terminal` and press Enter).

### 2. Navigate to the Application Folder

*   In the Terminal window, you need to go to the folder where you have the `goniometry_app` application files.
*   Type the following command and press Enter:

    ```bash
    cd /Users/carolinejohnson/workspace/goniometry_app
    ```
    *(Note: If your application folder is in a different location, replace `/Users/carolinejohnson/workspace/goniometry_app` with the actual path to your `goniometry_app` folder.)*

### 3. Start the Application

*   Once you are in the correct folder in the Terminal, type the following command and press Enter:

    ```bash
    venv/bin/python app.py
    ```

*   You will see some messages appear in the Terminal. This is normal. **Do not close the Terminal window.** The application needs it to run.

### 4. Open the Application in Your Web Browser

*   Open your preferred web browser (like Chrome, Safari, or Firefox).
*   In the address bar at the top, type the following address and press Enter:

    ```
    http://127.0.0.1:5000/
    ```

*   The application should now open in your browser, and you should see a live video feed from your camera with pose detection and angle measurements.

### 5. Capture Measurements

*   To save a measurement, click the **"Capture Measurement"** button on the web page.
*   A message will appear on the screen confirming that the measurement was captured and saved.
*   The captured image will be saved in the `static/images` folder within your `goniometry_app` directory.
*   The angle data will be saved in a file named `measurements.csv` in the main `goniometry_app` directory.

### 6. Stop the Application

*   When you are finished using the application, go back to the **Terminal window**.
*   Press `Ctrl` and `C` keys on your keyboard at the same time (`Ctrl + C`).
*   You will see a message indicating the server has stopped. You can now close the Terminal window.

If you encounter any issues, please ensure your computer's camera permissions are granted for the Terminal application (System Settings > Privacy & Security > Camera).