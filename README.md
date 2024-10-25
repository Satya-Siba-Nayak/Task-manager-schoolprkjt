# 🚀 Python Task Manager

A semi-complex task management system built in Python for my 12th standard school project. This application allows multiple users to create, manage, and track tasks with different permission levels and features.

## ✨ Features

- **User Authentication System**
  - Secure password hashing
  - Multiple user roles (Admin/User)
  - Role-based permissions

- **Task Management**
  - Create and delete tasks
  - Set task priorities (Low/Medium/High)
  - Add task descriptions and deadlines
  - Track task status (In Progress/Idle/Completed/Dropped)
  - Collaborate with other users
  - Add checklists, notes, and attachments to tasks

- **Admin Features**
  - Create new users
  - Manage user permissions
  - Delete all tasks
  - Override task permissions

- **Additional Features**
  - Due date reminders
  - Task filtering
  - Data persistence using pickle
  - Logging system for tracking activities

## 🛠️ Technical Stack

- Python 3.x
- pandas (for data management)
- hashlib (for password encryption)
- pickle (for data persistence)
- datetime (for deadline management)
- logging (for activity tracking)

## 📋 Prerequisites

- Python 3.x installed on your system
- Required Python packages:
  ```bash
  pip install pandas
  ```

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/task-manager.git
   cd task-manager
   ```

2. Run the program:
   ```bash
   python task_manager.py
   ```

3. Default login credentials:
   ```
   Admin Users:
   Username: Satya     Password: satya.eth
   Username: Hrugved   Password: hrug_077
   Username: Samarth   Password: samarth_25.09.06
   
   Regular User:
   Username: User      Password: 1234
   ```

## 💻 Usage

1. **Login/Logout**
   - Use the menu option 1 to login/logout
   - Different features are available based on user role

2. **Task Management**
   - Create new tasks with title, description, and deadline
   - Set task priorities and status
   - Add collaborators to tasks
   - Delete tasks (if permitted)

3. **Admin Functions**
   - Create new users
   - Manage user permissions
   - Delete all tasks (with confirmation)

## 📁 File Structure

```
task-manager/
├── task_manager.py      # Main program file
├── users.pkl           # Stored user data
├── tasks.pkl          # Stored task data
└── task_manager_logs.txt # Activity logs
```

## 🔐 Security Features

- Password hashing using SHA-256
- Role-based access control
- Permission verification for sensitive operations
- Activity logging for security tracking

## 🤝 Contributing

This was a school project, but feel free to fork and modify it for your own use! If you have suggestions for improvements, feel free to open an issue.

## 📝 License

This project is open source and available under the MIT License.

## 👥 Authors
- [**Satya siba Nayak**](https://github.com/Satya-Siba-Nayak)
- [**Hrugved Bhoite**](https://www.instagram.com/hrug_077/)
- [**Samarth More**](https://www.instagram.com/samarth_25.09.06/)

## 🙏 Acknowledgments

- Thanks to our school teachers for guidance and support
- Special thanks to Python and its amazing community
- Inspired by professional task management systems

---
*Note: This project was developed as an educational exercise and may not be suitable for production use without additional security enhancements.*