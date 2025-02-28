# YourDynamicShoppingList

## 📽️ Video Demo
[Watch on YouTube](https://www.youtube.com/watch?v=Sfb1ZYIigcU)

---

## 📌 Overview
YourDynamicShoppingList is a **web application** that allows users to dynamically create shopping lists, add, delete, and modify items, and share lists with others for collaborative shopping. Additionally, it can notify users if an item on their list is on discount using an **API from a government-provided website** for grocery discounts in Hungary.

---

## ✨ Features

### 📝 Dynamic Shopping Lists
- Create **new shopping lists** and add/remove/modify items.
- Mark items as completed **or delete them entirely**.
- Share shopping lists with other users for collaborative shopping.

### 🔔 Discount Notifications *(Planned Feature)*
- Uses a **government-provided API** to check for grocery discounts.
- Notifies users if any unchecked item is available at a discount in nearby stores.

### 👥 List Sharing & Collaboration *(Planned Update)*
- Allow users to **pair lists** so others can modify them.
- Future expansion to **multi-user shared lists** for families/households.
- Considerations for **verification & security** to ensure users approve shared lists.

### ⚡ Live Updates with AJAX
- Instead of **refreshing the entire page**, only relevant sections update dynamically.
- Improves **user experience and performance**.

### 🔐 Secure User Authentication
- **Password encryption & salting** for safe storage.
- Future plan to implement a **"Forgot Password" feature** using email verification.

### 🎨 Responsive & Structured Design
- **Bootstrap styling** for alerts and feedback messages.
- **Modular template structure**:
  - `layout.html` serves as the **base template**.
  - `homepage.html` dynamically displays all shopping lists for the logged-in user.
  - `shoppinglist.html` dynamically shows items for a selected shopping list.

---

## 🏗️ Project Structure

### 📂 **Frontend**
- **Templates (`/templates`)**: Contains all HTML files.
- **Static Files (`/static`)**: Contains images and CSS.
  - Plan to organize them further under a `design/` directory.

### 🗄️ **Backend**
- **Main Flask App (`my_flask_app.py`)**: Manages database, frontend, and backend logic.

### 🛢️ **Database (`YourShopMate.db`)**
Originally named after the project's first name, which has since changed. 

#### **Database Schema**
| Table Name     | Primary Key | Foreign Keys | Purpose |
|---------------|------------|--------------|---------|
| `users`       | `users_id` | N/A | Stores user data |
| `shoppinglists` | `shoppinglists_id` | `owner_id`, `coowner_id` → `users_id` | Stores shopping list details |
| `items`       | `items_id` | `list_id` → `shoppinglists_id`, `creator_id` → `users_id` | Stores individual shopping items |

---

## 🚀 Challenges & Design Considerations

### ✅ **Item Deletion vs. Marking as Completed**
- Should users only mark items as "completed," or **allow full deletion**?
- Decision: Added a **separate delete action** for flexibility.

### ✅ **Page Refresh vs. Live Updates**
- Initially, full-page refresh was required for list updates.
- Switched to **AJAX-based updates** for a smoother experience.
- Future refinement needed for better efficiency.

### ✅ **Database Query Optimization**
- Instead of returning arrays, **row.factory** should be used for key-value pairs.

### ✅ **User Feedback & Alerts**
- Implemented **Bootstrap alerts** for clear, concise feedback.

---

🔮 Future Plans
	•	📌 Optimize AJAX-based updates for smoother UI experience.
	•	📌 Implement “Forgot Password” feature with email verification.
	•	📌 Improve database query efficiency using key-value structures.
	•	📌 Enhance discount notification system for better store matching.
	•	📌 Expand list-sharing feature for multi-user collaboration.