# Safeconnekt

Safeconnekt is a mobile application leveraging QR technology to enhance emergency response and streamline personal identification. The application provides QR stickers for medical info, tagging personal items, pets, and individuals, enabling quick identification and recovery. It improves response times and achieves increase in successful recoveries through QR code scanning.

---

## Features

- **QR Technology**: Each user or item is assigned a unique QR code.
- **Emergency Response**: Rapid access to medical or personal information during emergencies.
- **Tagging**: Tag and manage personal items, pets, and individuals.
- **Enhanced Recovery**: Facilitates the recovery of lost items or individuals.
- **OTP-based Authentication**: Secure login using OTP sent to the registered mobile number.
- **Efficient Backend**: Built using Django and served with Gunicorn for robust performance.
- **Interactive Frontend**: Developed with React for a seamless user experience.

---

## Installation


### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/adavadkardhruv13/safeconnect.git
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


4. Run the development server:
   ```bash
   python manage.py runserver
   ```
---

## Technologies Used

### Backend
- FastAPI
- PostgrSQL
- Cloudnary
- AWS(RDS)

### Frontend
- Flutter


---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- QR Code Generator libraries
- FastAPI and Flutter communities
