# Deployment Guide: Streamlit Community Cloud & Firebase

To deploy your dashboard to the **Streamlit Community Cloud**, we must move from "local memory" to a "Cloud Database" (Firebase). Streamlit Cloud containers reset frequently, so local memory or files will be lost.

### Step 1: Set up Firebase (FREE)
1.  Go to the [Firebase Console](https://console.firebase.google.com/).
2.  Create a new project (e.g., "IoT-Dashboard").
3.  In the left menu, go to **Build > Realtime Database** and create a database.
4.  Set the **Rules** to `true` for testing (Note: Secure these later):
    ```json
    {
      "rules": {
        ".read": true,
        ".write": true
      }
    }
    ```
5.  Copy your **Database URL** (e.g., `https://your-db-name.firebaseio.com/`).

### Step 2: Update `streamlit_app.py`
We will replace the "In-memory/Flask" code with code that reads/writes directly to Firebase using the `requests` library.

### Step 3: Streamlit Community Cloud Deployment
1.  Push your code to a **GitHub Repository**.
    *   Include `streamlit_app.py`
    *   Include `requirements.txt`
2.  Login to [Streamlit Cloud](https://share.streamlit.io/).
3.  Click **"New app"**, select your Repo and Main file.
4.  **Important**: In the App Settings, add your Firebase URL as a "Secret" or hardcode it (if testing).

### Step 4: Update ESP32
Your ESP32 will now talk directly to the **Firebase URL** instead of your computer's IP. 
*   **New ESP32 URL**: `https://your-db-name.firebaseio.com/iot_data.json`

---
**Would you like me to update your `streamlit_app.py` now with the Firebase cloud logic so it's ready for deployment?**
