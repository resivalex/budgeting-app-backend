# Welcome to the Budgeting App Backend! 🚀

This backend application, built with FastAPI, handles your personal budgeting and expense data.

- [Getting Started](#getting-started-)
- [Google Drive Integration & Backup](#google-drive-integration---backup-)
- [API Endpoints](#api-endpoints-)
- [Code Structure](#code-structure-)
- [Development](#development-)
- [Acknowledgments](#acknowledgments-)
- [Contribution](#contribution-)
- [License](#license-)
- [Contact](#contact-)

## Getting Started 🚀

1.  Clone the repository: `git clone https://github.com/resivalex/budgeting-app-backend.git`
2.  Navigate into the directory: `cd budgeting-app-backend`
3.  Install dependencies: `poetry install`
4.  Set up environment variables (copy `.env.example` to `.env` if available, then edit).
5.  Set up Google Drive credentials (see [Google Drive Integration & Backup](#google-drive-integration---backup-)).
6.  Run database migrations: `poetry run alembic upgrade head`
7.  Start the server: `poetry run uvicorn main:app --reload`
8.  Access the backend at `http://localhost:8000`.

## Google Drive Integration & Backup 🔄🕒

This app uses Google Drive for daily automated backups of transaction data as CSV files.

**Setup:**

1.  Create a Google Cloud Project at [console.cloud.google.com](https://console.cloud.google.com/).
2.  Enable the Google Drive API.
3.  Create a Service Account:
    *   Go to "IAM & Admin" > "Service Accounts".
    *   Click "Create Service Account" (e.g., "budgeting-app-service").
    *   Grant it the "Drive API > Drive File Creator" role.
4.  Create and download the JSON key for this service account.
5.  Save the key to `credentials/google-drive-credentials.json`.
6.  Create a Google Drive folder for backups.
7.  Share this folder with the service account email (`service-account-name@project-id.iam.gserviceaccount.com`).
8.  Note the folder ID from the URL (the string after `/folders/`).
9.  Add these variables to your `.env` file:
    ```dotenv
    GOOGLE_DRIVE_CREDENTIALS_PATH=credentials/google-drive-credentials.json
    GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id

    # Optional: Configure daily backup time (24-hour format, UTC)
    DAILY_DUMP_HOUR=3
    DAILY_DUMP_MINUTE=0
    ```

Backups run daily at the configured time (default: 3:00 AM UTC), named with a timestamp.

## API Endpoints 🌐

Explore the available API endpoints (viewable at `/docs` when the server is running):

-   **System**: Check system health.
-   **Configuration**: Retrieve backend configuration.
-   **State**: Manage app settings, transactions (import/export).
-   **Admin**: Administrative functions, including manually triggering a data dump to Google Drive via `/trigger-dump`.

## Code Structure 🏗️

-   `src/budgeting_app_backend/`: Core application logic.
-   `main.py`: FastAPI app entry point and configuration.
-   `alembic/`: Database migration scripts (using Alembic).
-   `pyproject.toml`: Project metadata and dependencies (managed by Poetry).
-   `README.md`: This file.

## Development 💻

1.  Clone the repo and install dependencies (`poetry install`).
2.  Make code changes.
3.  Run the server (`poetry run uvicorn main:app --reload`) for live testing.
4.  Use an API client or the `/docs` UI to test endpoints.

## Acknowledgments 👏

Built with the help of these great open-source libraries:

-   [FastAPI](https://fastapi.tiangolo.com/)
-   [SQLAlchemy](https://www.sqlalchemy.org/) (with Alembic for migrations)
-   [pandas](https://pandas.pydata.org/)
-   [pydantic](https://pydantic-docs.helpmanual.io/)
-   [Google API Python Client](https://github.com/googleapis/google-api-python-client)
-   [APScheduler](https://apscheduler.readthedocs.io/)
-   [tabulate](https://pypi.org/project/tabulate/)

## Contribution 🤝

Contributions are welcome! Follow the "Development" steps and submit a pull request.

## License 📝

[MIT License](LICENSE).

## Contact 📞

Questions or issues? Open an issue on the GitHub repository.

---

Happy budgeting! 🎉
