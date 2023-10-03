# TCGPlayer Quick Printer

This script processes TCGPlayer CSV sales lists, generating a PDF with printable address labels. Below is a step-by-step guide to set up and run the script on your device.

## 1. Installing Python Through the Windows Store
a. Open the Microsoft Store on your Windows device.
b. Search for "Python".
c. Download and install the latest version of Python offered.
d. After installation, verify it by pressing `Windows + X`, selecting `Windows PowerShell` or `Terminal`, typing `python`, and pressing Enter. This should open the Python interactive shell.


## 2. Installing Required Libraries
a. **Opening the Command Prompt**:
   - Press the `Windows` key on your keyboard.
   - Type "Command Prompt" or "cmd" into the search bar.
   - Click on the `Command Prompt` application from the search results.

b. **Installing the Libraries**:
   - In the Command Prompt window, type the following command and then press `Enter`:

     ```
     pip install pandas reportlab
     ```

   - Wait for the process to complete. Once it's done, the libraries are successfully installed.


## 3. Making the Script Double-Clickable
a. **Rename the Script**: 
   - Locate your Python script in Windows Explorer.
   - Rename the file to have a `.pyw` extension instead of `.py`. This ensures that when you run the script, it won't bring up a terminal window.
   
b. **Setting the Default Program**:
   - Right-click the `.pyw` file.
   - Choose `Open with` > `Choose another app`.
   - From the list, select "Python". If it's not listed:
     - Scroll down and click on `More apps`.
     - Look for Python in the expanded list or use the `Look for another app on this PC` option to locate the Python executable (`python.exe`).
   - Ensure you check the box that says "Always use this app to open .pyw files" before clicking `OK`.

c. **Running the Script**: 
   - Simply double-click the `.pyw` file whenever you want to run the script.



### macOS:
## 1. Installing Python
a. Open Terminal.
b. Check if Python is already installed by typing `python3` and pressing Enter. If it's not installed, macOS will prompt you to install it.
c. If the above step doesn't prompt an install, download Python from the official [Python Downloads](https://www.python.org/downloads/mac-osx/) page and follow their instructions.


## 2. Installing Required Libraries
a. **Opening the Terminal**:
   - Open Finder.
   - Navigate to `Applications` > `Utilities`.
   - Double-click on the `Terminal` application.


b. **Installing the Libraries**:
   - In the Terminal window, type the following command and then press `Enter`:

     ```
     pip install pandas reportlab
     ```

   - Wait for the installation process to complete. The libraries are now installed.


## 3. Making the Script Double-Clickable
a. **Adding a Shebang**:
   - A shebang is a line at the very top of your script that tells the system how to execute the script. Open your script in any text editor.
   - Ensure the first line of your script is `#!/usr/bin/env python3`. If not, add it.
   
b. **Making the Script Executable**:
   - Open the Terminal application (You can find it in Applications > Utilities > Terminal).
   - Navigate to the directory containing your script using the `cd` command. For example, if your script is in the Downloads folder, you'd type `cd Downloads`.
   - Make the script executable with the following command:

     ```
     chmod +x your_script_name.py
     ```

c. **Running the Script**: 
   - Now, whenever you want to run your script, you can simply double-click it in Finder.
   - The first time you run it, macOS might ask for confirmation since you downloaded the file from the internet. Confirm that you want to run it, and subsequent launches will be immediate.




### Linux:
## 1. Installing Python
Most Linux distributions come with Python pre-installed. To verify:
a. Open Terminal.
b. Type `python3` and press Enter.

If Python isn't installed, install it using your distribution's package manager. For Ubuntu:
Use a bash sell

sudo apt update
sudo apt install python3


## 2. Installing Required Libraries
a. **Opening the Terminal**:
   - This might vary based on the Linux distribution and desktop environment you're using. Typically, you can either:
     - Press `Ctrl` + `Alt` + `T` together.
     - Or, search for "Terminal" in your application menu and open it.

b. **Installing the Libraries**:
   - In the Terminal window, type the following command and then press `Enter`:

     ```
     pip3 install pandas reportlab
     ```

   - The system will process the request, and once it's done, the libraries will be install


## 3. Making the Script Double-Clickable
a. **Editing the Script**: Open your script in a text editor of choice (e.g., nano, gedit) and ensure the first line is `#!/usr/bin/env python3`.

b. **Granting Execute Permissions**: Using the Terminal, navigate to the directory of your script and grant execute permissions:

cd /path_to_your_script/
chmod +x your_script_name.py

c. **Associating with Python**: In your file manager, right-click on the Python script, choose 'Properties' or 'Open With', and select 'Python 3'.

d. **Running the Script**: Double-click the Python script in your file manager. If prompted, choose 'Run'. (Replace /path_to_your_script/ and your_script_name.py with the appropriate details.)


