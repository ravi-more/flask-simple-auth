# Flask Simple Auth

This Flask project provides a simple authentication system with features like password reset using JWT and email notifications. No Flask authentication Python library is used. It utilizes MongoDB as the database and is built using HTML and CSS without relying on third-party UI libraries.

## Features

- Complete authentication system
- Password reset using JWT and email
- Route security with `login_required` decorator
- Scalable project structure

## Project Structure

The project is scaffolded in a way that allows easy scaling.

## Rendering Dynamic Pages

Jinja2 is used to render dynamic HTML pages.

## Setup

### Virtual Environment

- Isolation of project dependencies
- Easy replication of the development environment
- Create a virtual environment:

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:
    On Windows:

    ```bash
    .\venv\Scripts\activate
    ```

   On Unix or MacOS:

    ```bash
    source venv/bin/activate
    ```

### Install Dependencies

- Install the project dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

### Configuration

- Add project configuration file at `instance/config.py` with the following content:

  ```python
    SECRET_KEY = "your_secret_key"
    SECURITY_PASSWORD_SALT = "your_password_salt"
    MONGO_URI = "your_mongo_uri"
    MAIL_SERVER = "your_mail_server"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "your_mail_username"
    MAIL_PASSWORD = "your_mail_password"
  ```

- Replace the placeholders with your actual values.

### Run the Project

- Execute the following command to run the project:

  ```bash
  flask run
  ```

- Now your Flask Simple Auth project is up and running!
- Feel free to customize and expand upon this template to better fit the specifics of your project!

## Contributing

Welcome to the community! We encourage and appreciate contributions to enhance this project. Please review our [contribution guidelines](CONTRIBUTING.md) for details on how to contribute.

## Acknowledgments

A big thank you to the open-source community for their invaluable contributions and resources that have played a crucial role in making this project a reality.

## License

This project is licensed under the MIT License. For more information, refer to the [LICENSE](LICENSE) file.
