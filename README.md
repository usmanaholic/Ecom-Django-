# TrickStoree - E-commerce Website

TrickStoree is an online shopping platform built using Django. It provides a user-friendly interface where customers can browse products, add them to the cart, and complete their purchases. The site...

## Features

- **Product Browsing**: Users can view a variety of products with details.
- **Search Functionality**: Users can search for products using a search bar.
- **User Authentication**: Sign up, log in, and manage user profiles.
- **Cart System**: Users can add items to their cart and proceed to checkout.
- **coupon System**: Admin can add coupon and user can avail it.
- **Order Management**: Users can view their order history and order details.
- **Payment Integration**: Users can pay for their orders online (if integrated).
- **Admin Panel**: Admin can manage products, categories, and user orders.

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (or MySQL/PostgreSQL if preferred)
- **Version Control**: Git
- **Hosting**: [Your Hosting Platform]

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/usmanaholic/trickstoree.git
    ```

2. Navigate into the project directory:
    ```bash
    cd trickstoree
    ```

3. Create a virtual environment:
    ```bash
    python3 -m venv env
    ```

4. Activate the virtual environment:
    - For Windows:
      ```bash
      .\env\Scripts\activate
      ```
    - For Mac/Linux:
      ```bash
      source env/bin/activate
      ```

5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Apply migrations:
    ```bash
    python manage.py migrate
    ```

7. Create a superuser (for accessing the admin panel):
    ```bash
    python manage.py createsuperuser
    ```

8. Run the development server:
    ```bash
    python manage.py runserver
    ```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to access the site.

## Features to Implement

- Payment Gateway Integration (e.g., Stripe, PayPal)
- User Review & Rating System
- Product Categories and Filters
- Advanced Admin Dashboard

## Contributing

If you'd like to contribute to the project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to modify any sections depending on your project specifics and features!

![Homepage](/homepage.PNG)
