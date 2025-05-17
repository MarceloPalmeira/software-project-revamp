# 🎬 iCinema – Cinema Management System

Welcome to **iCinema**, a cinema management system developed to simplify ticket purchasing, movie reviews, and much more! This project simulates a real cinema experience, allowing users to choose movies, showtimes, seats, and payment methods, as well as review the movies they've watched.

---

## 📌 Requirements

- **Python 3.x** installed  
- To run the project, please execute:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

- A `users.json` file to store user data (it will be created automatically if it doesn't exist)  
- Create an account using **GMAIL ONLY** for proper email functionality  

---

## Features

### 1️⃣ Cinema and Movie Listings: Displaying listings of cinemas and movies ✅  
### 2️⃣ Seat Selection and Booking: Enabling users to select seats and book tickets ✅  
### 3️⃣ Payment Processing: Secure processing of ticket payments ✅  
### 4️⃣ User Account Management: Creating and managing user profiles ✅  
### 5️⃣ Booking History and Cancellations: Viewing past bookings and managing cancellations ✅  
### 6️⃣ Promotions and Discounts: Offering and managing discounts and special offers ✅  
### 7️⃣ Real-Time Seat Availability: Showing real-time availability of seats in cinemas ✅  
### 8️⃣ Mobile Ticketing: Generating mobile tickets for ease of access ✅ (tickets are generated and sent via email)  
### 9️⃣ Customer Reviews and Ratings: Feature for users to rate and review movies ✅  
### 🔟 Notifications and Alerts: Sending notifications for new releases and booking confirmations ✅ (only reservation confirmations via email)  

---

## Object-Oriented Programming Principles Applied

- ✅ **Encapsulation:** Use of private attributes and `@property` methods in classes like `Account`, `EmailManager`, etc.  
- ✅ **Inheritance:** For example, `IngressoManager` inherits from `EmailManager`.  
- ✅ **Polymorphism:** Classes like `CartaoPayment`, `PixPayment`, and `DinheiroPayment` override the method `processar_pagamento()`.  
- ✅ **Abstract Class:** The abstract base class `Payment` defines a common interface for all payment types.

---

## Design Patterns Used

### 1. Creational Pattern – **Builder**
**Where:** `AccountBuilder` for user account creation  
**File:** `models/user.py`

**Problem:** Creating complex objects with many parameters can make constructors messy and hard to maintain.  
**Solution:** The Builder Pattern allows step-by-step construction of `Account` objects with readable and scalable code.

**Why:** Besides improving readability, I chose the **Builder Pattern** because it is the **most scalable** creational pattern. As the `Account` class evolves (e.g., adding CPF, birthdate, etc.), the builder can grow safely without breaking the existing code.

**Example:**
```python
builder = AccountBuilder()
user = builder.set_name("João").set_email("joao@email.com").set_password("123").build()
```

---

### 2. Structural Pattern – **Facade**
**Where:** `SistemaFacade` centralizes the system’s operations  
**File:** `facade/sistema_facade.py`

**Problem:** Directly using multiple managers (`AuthManager`, `CinemaManager`, `ReviewManager`) in routes creates tight coupling and repetition.  
**Solution:** The Facade Pattern provides a **unified interface** to the subsystems, making the main code cleaner and more maintainable.

**Example:**
```python
sistema = SistemaFacade()
user = sistema.login(email, password)
sistema.reservar(user, cinema, filme, horario, assento, coupon, payment_method)
```

---

### 3. Behavioral Pattern – **Strategy**
**Where:** Payment system with `Payment`, `PixPayment`, `CartaoPayment`, etc.  
**Files:** `models/pagamento.py`, `payment_factory.py`

**Problem:** Each payment method has different logic. Using conditionals (`if/else`) for every case makes the code hard to extend.  
**Solution:** The Strategy Pattern allows each payment class to implement its own logic via a shared interface, enabling dynamic selection at runtime.

**Why:** It supports the **Open/Closed Principle** — new payment types can be added without modifying existing logic.

**Example:**
```python
payment = PaymentFactory.create("pix", total)
confirmation = payment.processar_pagamento()
```

---