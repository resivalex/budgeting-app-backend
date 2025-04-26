Here's a more friendly and concise version of your `README.md` file for the project "Budgeting App Backend":

# Welcome to the Budgeting App Backend! 🚀

This is the powerhouse of the Budgeting App. It's a backend application built with FastAPI that handles all your personal budgeting and expense data.

## What's Inside? 📦
- [How to Get Started?](#getting-started-)
- [What Can I Do with it?](#api-endpoints-)
- [How is it Built?](#code-structure-)
- [How Do I Make it Mine?](#development-)
- [Who Helped Make This?](#acknowledgments-)
- [Can I Help Too?](#contribution-)
- [What about the Legal Stuff?](#license-)
- [Who Do I Talk to?](#contact-)

## Getting Started 🚀

1. Copy the repository: `git clone https://github.com/resivalex/budgeting-app-backend.git`
2. Install what's necessary: `poetry install`
3. Set up your environment variables. (Don't worry, we'll tell you where everything goes.)
4. Set up Google Drive credentials (see [Google Drive Integration](#google-drive-integration-))
5. Start the server: `poetry run uvicorn main:app --reload`
6. Voilà! You can now access the backend at `http://localhost:8000`.

## Google Drive Integration 🔄

The Budgeting App uses Google Drive exclusively for backing up transaction dumps. Here's how to set it up:

1. Create a Google Cloud Project at [console.cloud.google.com](https://console.cloud.google.com/)
2. Enable the Google Drive API for your project
3. Create a Service Account in the Google Cloud Console:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Give it a name like "budgeting-app-service"
   - Grant it the "Drive API > Drive File Creator" role
4. Create and download the JSON key for this service account
5. Save the JSON key to your `credentials` folder as `google-drive-credentials.json`
6. Create a folder in Google Drive where you want to store your transaction dumps
7. Share this folder with the service account email (it will look like `service-account-name@project-id.iam.gserviceaccount.com`)
8. Get the folder ID from the URL when you open the folder (it's the long string in the URL after `/folders/`)
9. Add these variables to your `.env` file:
   ```
   GOOGLE_DRIVE_CREDENTIALS_PATH=credentials/google-drive-credentials.json
   GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id
   
   # Optional: Configure the daily backup schedule (24-hour format, UTC timezone)
   DAILY_DUMP_HOUR=3
   DAILY_DUMP_MINUTE=0
   ```

Transaction data will be automatically backed up to Google Drive daily at the configured time (default: 3:00 AM UTC).

## Scheduled Data Backup 🕒

The application includes an automatic daily backup system that:

1. Exports all transaction data as CSV
2. Uploads it to your configured Google Drive folder
3. Names the file with a timestamp for easy identification
4. Runs daily at your configured time (default: 3:00 AM UTC)

You can configure the backup time by setting these environment variables:
- `DAILY_DUMP_HOUR`: Hour of the day in 24-hour format (0-23)
- `DAILY_DUMP_MINUTE`: Minute of the hour (0-59)

For manual backups, use the `/trigger-dump` endpoint.

## API Endpoints 🌐

The Budgeting App Backend offers you these API endpoints:

- `System`: Check the system health.
- `Configuration`: Retrieve the backend configuration.
- `State`: Get app settings, transactions, and import or export transactions.
- `Admin`: Administrative functions like manually triggering backups.

Each endpoint does something special. Feel free to explore them!

## Code Structure 🏗️

Here's a sneak peek into our project's blueprint:

- `budgeting_app_backend/` - The brain of our app.
- `main.py` - The entry point of our application and the FastAPI app configuration.
- `requirements.txt` - A list of Python dependencies required by the project.
- `README.md` - Hey, that's this file!

## Development 💻

Want to make the Budgeting App Backend your own? Here's how:

1. Clone the repository and install the dependencies.
2. Make your changes to the code.
3. Run the server for testing with live reloading. See your changes in real-time!
4. Test the endpoints using an API client of your choice.

## Acknowledgments 👏

A big shoutout to these wonderful open-source libraries and frameworks that make our app possible:

- [FastAPI](https://fastapi.tiangolo.com/)
- [PyCouchDB](https://github.com/andrewsmedina/pycouchdb)
- [pandas](https://pandas.pydata.org/)
- [pydantic](https://pydantic-docs.helpmanual.io/)
- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
- [APScheduler](https://apscheduler.readthedocs.io/)
- [tabulate](https://pypi.org/project/tabulate/)

## Contribution 🤝

Want to contribute to the Budgeting App Backend? Great! Follow the steps in the "Development" section and then send a pull request with your changes. We appreciate all the help we can get!

## License 📝

The Budgeting App Backend is free and open-source, under the [MIT License](LICENSE).

## Contact 📞

Got questions? Suggestions? Issues? Reach out to us or open an issue on our GitHub repository. We'd love to hear from you!

---

We hope this `README.md` gives you a clear overview of the Budgeting App Backend, its features, and how to get it up and running on your local machine. The code is quite user-friendly, but if you have any questions or need further help, don't hesitate to ask. We believe in making budgeting easier for everyone, and your feedback helps us do just that. Enjoy exploring and happy budgeting! 🎉
