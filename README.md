# s23-final-project-pacman

This project is the first programming project I have ever done at CMU. I will release another version of it anytime soon.

To run, navigate to TP3v2.py. Make sure to install tk (instructed below)

### 1. **MacOS/Linux:**
   On macOS or Linux, you'll likely need to install `tk` through your package manager.

   - For **macOS** (with Homebrew):
     ```bash
     brew install tcl-tk
     ```

     Then, you may need to set the environment variable so that Python can locate the correct `Tk` installation:

     ```bash
     export PATH="/opt/homebrew/opt/tcl-tk/bin:$PATH"
     export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"
     export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"
     ```

     After this, you can try reinstalling Python and ensure it's linked with `tk`:
     ```bash
     brew reinstall python-tk
     ```

   - For **Linux** (Debian/Ubuntu-based distros):
     ```bash
     sudo apt-get install python3-tk
     ```

### 2. **Windows:**
   If you're on Windows, the Python installer typically includes `Tkinter`. If `Tkinter` is missing, try reinstalling Python with the option to include `tcl/tk` and `IDLE` (which is the part that brings in `Tkinter`).

After installing, try running your script again and importing `tkinter`:
```python
import tkinter
```

Let me know how it goes!
