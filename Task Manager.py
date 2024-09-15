import hashlib
import pickle
from enum import Enum
import pandas as pd
from datetime import datetime, timedelta
import os
import logging

logging.basicConfig(filename='task_manager_logs.txt', level=logging.INFO)

# Define roles and permissions
class Role(Enum):
    ADMIN = 1
    USER = 2

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Permission:
    CREATE_TASKS = 1
    UPDATE_TASKS = 2
    DELETE_TASKS = 3
    MANAGE_USERS = 4

# Base User Class
class User:
    def __init__(self, username, password, role=Role.USER):
        self.username = username
        self.password = UserManager.hash_password(password)
        self.role = role
        self.permissions = self._get_permissions(role)

    def _get_permissions(self, role):
        if role == Role.ADMIN:
            return (
                Permission.CREATE_TASKS
                | Permission.UPDATE_TASKS
                | Permission.DELETE_TASKS
                | Permission.MANAGE_USERS
            )
        elif role == Role.USER:
            return Permission.CREATE_TASKS | Permission.UPDATE_TASKS

    def has_permission(self, permission):
        return bool(self.permissions & permission)

# Base Task Class
class Task:
    def __init__(
        self,
        title,
        description="",
        deadline=None,
        priority=Priority.MEDIUM,
        collaborators=[],
        creator=None,
    ):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.collaborators = collaborators
        self.completed = False
        self.checklist = []
        self.notes = []
        self.attachments = []
        self.creator = creator
    def mark_in_progress(self):
        if not self.completed:
            print(f"Task '{self.title}' marked as In Progress.")
            self.status = "In Progress"
        else:
            print("Cannot change status for a completed task.")
    def mark_idle(self):
        if self.completed:
            print(f"Task '{self.title}' marked as Idle.")
            self.status = "Idle"
        else:
            print("Cannot change status for an in-progress task.")

    def mark_completed(self):
        if not self.completed:
            print(f"Task '{self.title}' marked as Completed.")
            self.status = "Completed"
            self.completed = True
        else:
            print("Task is already completed.")

    def mark_dropped(self):
        if not self.completed:
            print(f"Task '{self.title}' marked as Dropped.")
            self.status = "Dropped"
            self.completed = True
        else:
            print("Cannot change status for a completed task.")  

    def add_checklist_item(self, item):
        self.checklist.append(item)

    def add_note(self, note):
        self.notes.append(note)

    def add_attachment(self, path):
        self.attachments.append(path)

    def __str__(self):
        creator_info = f"Created by: {self.creator}" if self.creator else "Created by: Anonymous"
        return (
            f"Title: {self.title}\nDescription: {self.description}\n"
            f"Deadline: {self.deadline}\nPriority: {self.priority.name}\n"
            f"Collaborators: {', '.join(self.collaborators)}\n"
            f"{creator_info}\n"
            f"Completed: {self.completed}\n"
            f"Checklist: {', '.join(self.checklist)}\n"
            f"Notes: {', '.join(self.notes)}\n"
            f"Attachments: {', '.join(self.attachments)}\n"
        )

# UserManager Class
class UserManager:
    @staticmethod
    def hash_password(password):
        logging.info(f'Hashing password for Admin/user')
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(stored_hashed_password, input_password):
        logging.info(f'Verifying password for Admin/user')
        return stored_hashed_password == hashlib.sha256(
            input_password.encode()
        ).hexdigest()

    def login(self, task_manager):
        logging.info(f'Admin/User login attempt')
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = self.verify_user(username, password)
        if user:
            logging.info(f"Login successful! Welcome, {user.username}!")
            print(f"Login successful! Welcome, {user.username}!")
            return user
        else:
            logging.warning("Invalid username or password.")
            print("Invalid username or password.")
            return None

    def verify_user(self, username, password):
        user = task_manager.users[task_manager.users["username"] == username]
        if user.empty or not self.verify_password(
            user.iloc[0]["password"], password
        ):
            return None
        return User(
            user.iloc[0]["username"],
            user.iloc[0]["password"],
            role=Role(user.iloc[0]["role"]),  # Fix: Convert the role value to Enum
        )

# Task Manager Class
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.users = pd.DataFrame(columns=["username", "password", "role"])
        self.load_data()

    def load_data(self):
        self.load_users()
        self.load_tasks()

    def create_user(self, logged_in_user):
        if not logged_in_user or logged_in_user.role != Role.ADMIN:
            logging.warning("Unauthorized attempt to create a new user.")
            print("You need to be logged in as an admin to create a new user.")
            return

        username = input("Enter new username: ")
        password = input("Enter new password: ")
        role_input = input("Enter new user role (1. ADMIN, 2. USER): ")

        try:
            role = Role(int(role_input))
        except ValueError:
            logging.warning("Invalid role input. Using default role (USER).")
            print("Invalid role input. Using default role (USER).")
            role = Role.USER

        self.add_user(username, password, role)
        logging.info(f"User '{username}' created successfully with role '{role.name}'.")
        print(f"User '{username}' created successfully with role '{role.name}'.")
    
    def save_users(self):
        try:
            with open("users.pkl", "wb") as file:
                pickle.dump(self.users, file)
                print("Users saved successfully.")
        except Exception as e:
            print(f"Error saving users: {e}")

    def load_users(self):
        try:
            if os.path.exists("users.pkl") and os.path.getsize("users.pkl") > 0:
                self.users = pd.read_pickle("users.pkl")
                print("Users loaded successfully.")
            else:
                print("No users found or the file is empty.")
        except Exception as e:
            print(f"Error loading users: {e}")
    def login(self):
        return user_manager.login(self)
    def mark_task_status(self, logged_in_user):
      try:
        task_index = int(input("Enter the number of the task to mark status: ")) - 1
        if 0 <= task_index < len(self.tasks):
            task_to_mark = self.tasks[task_index]

            if logged_in_user.username == task_to_mark.creator or logged_in_user.has_permission(Permission.MANAGE_USERS):
                status_choice = input("Enter the status (1. In Progress,2.Idle, 3. Completed, 4. Dropped): ")
                if status_choice == "1":
                    task_to_mark.mark_in_progress()
                elif status_choice == "2":
                    task_to_mark.mark_idle()
                elif status_choice == "3":
                    task_to_mark.mark_completed()
                elif status_choice == "4":
                    task_to_mark.mark_dropped()
                else:
                    print("Invalid status choice.")
            else:
                print("You don't have permission to mark the status for this task.")
        else:
            print("Invalid task number.")
      except ValueError:
        print("Invalid input. Please enter a valid task number.")
       
    def create_task(self, logged_in_user):
        if not logged_in_user:
            print("You need to log in to create a task.")
            return

        title = input("Enter task title: ")
        description = input("Enter task description (optional): ")
        deadline = input("Enter task deadline (YYYY-MM-DD) (optional): ")
        priority_input = input(
            "Enter task priority (LOW, MEDIUM, HIGH) (optional): "
        )

        try:
            priority = Priority[priority_input]
        except KeyError:
            print("Invalid priority. Using default priority (MEDIUM).")
            priority = Priority.MEDIUM

        collaborators = input(
            "Enter collaborators separated by commas (optional): "
        ).split(",")

        # Use the username of the logged-in user
        username = logged_in_user.username

        self.add_task(username, title, description, deadline, priority, collaborators)
        print("Task created successfully!")
    def exit_program(self):
        try:
            self.save_users()
            self.save_tasks()
            print("Exiting program. Data saved successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")
    def list_tasks(self, username):
        tasks = self.tasks
        if tasks:
            for task in tasks:
                # Check if the user is logged in
                if username:
                    # Check if the user has USER permission
                    if (
                        self.users.loc[
                            self.users[self.users["username"] == username].index,
                            "role",
                        ].__contains__(Permission.CREATE_TASKS)
                        or task.creator == username
                    ):
                        # Display all information for the tasks the user has created
                        print(task)
                    else:
                        # Display limited information for logged-in users with USER permission
                        print(f"Title: {task.title}, Created by: {task.creator}")
                else:
                    # Display limited information for logged-out users
                    print(f"Title: {task.title}, Created by: {task.creator}")
        else:
            print("No tasks found.")
        return tasks



    def load_tasks(self):
        try:
            if os.path.exists("tasks.pkl") and os.path.getsize("tasks.pkl") > 0:
                self.tasks = pickle.load(open("tasks.pkl", "rb"))
                print("Tasks loaded successfully.")
            else:
                print("No tasks found or the file is empty.")
        except (FileNotFoundError, EOFError, pickle.UnpicklingError) as e:
            print(f"Error loading tasks: {e}")

    def delete_task(self, logged_in_user):
      if not logged_in_user:
          print("You need to log in to delete a task.")
          return

      # Show a list of tasks to choose from
      print("List of Tasks:")
      for i, task in enumerate(self.tasks, start=1):
          print(f"{i}. {task.title} (Created by: {task.creator})")

      try:
          task_index = int(input("Enter the number of the task to delete: ")) - 1
          if 0 <= task_index < len(self.tasks):
              task_to_delete = self.tasks[task_index]

              if (
                  logged_in_user.username == task_to_delete.creator
                  or logged_in_user.has_permission(Permission.MANAGE_USERS)
              ):
                  self.tasks.remove(task_to_delete)
                  print("Task deleted successfully!")
              else:
                  print("You don't have permission to delete this task.")
          else:
              print("Invalid task number.")
      except ValueError:
          print("Invalid input. Please enter a valid task number.")
    def save_tasks(self):
        try:
            with open("tasks.pkl", "wb") as file:
                pickle.dump(self.tasks, file)
                print("Tasks saved successfully.")
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def add_user(self, username, password, role=Role.USER):
        new_user = User(username, password, role)
        self.users = self.users._append(
            {
                "username": new_user.username,
                "password": new_user.password,
                "role": new_user.role.value,  # Use role.value to store the Enum value
            },
            ignore_index=True,
        )
    def set_task_due_date(self, logged_in_user):
      if not logged_in_user:
        print("You need to log in to set a task due date.")
        return
      print("List of Tasks:")
      for i, task in enumerate(self.tasks, start=1):
          print(f"{i}. {task.title} (Created by: {task.creator})")
      try:
        task_index = int(input("Enter the number of the task to set the due date: ")) - 1
        if 0 <= task_index < len(self.tasks):
            task_to_set_due_date = self.tasks[task_index]

            if (
                logged_in_user.username == task_to_set_due_date.creator
                or logged_in_user.has_permission(Permission.MANAGE_USERS)
            ):
                due_date = input("Enter the due date (YYYY-MM-DD): ")
                task_to_set_due_date.deadline = datetime.strptime(due_date, "%Y-%m-%d")
                print(f"Due date set for task '{task_to_set_due_date.title}': {task_to_set_due_date.deadline}")
            else:
                print("You don't have permission to set the due date for this task.")
        else:
            print("Invalid task number.")
      except ValueError:
        print("Invalid input. Please enter a valid task number.")

    def show_due_date_reminders(self):
        current_date = datetime.now()
        upcoming_tasks = [task for task in self.tasks if task.deadline and task.deadline > current_date]

        if upcoming_tasks:
            print("\nUpcoming Task Due Date Reminders:")
            for task in upcoming_tasks:
                print(f"{task.title}: {task.deadline}")
        else:
            print("No upcoming task due date reminders.")
    def add_task(
        self,
        username,
        title,
        description="",
        deadline=None,
        priority=Priority.MEDIUM,
        collaborators=[],
    ):
        if deadline:
            try:
                deadline = datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD. Using no deadline.")
                deadline = None

        new_task = Task(
            title, description, deadline, priority, collaborators, creator=username
        )
        self.tasks.append(new_task)
        self.save_tasks()

if __name__ == "__main__":
    user_manager = UserManager()
    task_manager = TaskManager()

# Add initial users
task_manager.add_user("Satya", "satya.eth", Role.ADMIN)
task_manager.add_user("Hrugved", "hrug_077", Role.ADMIN)
task_manager.add_user("Samarth", "samarth_25.09.06", Role.ADMIN)
task_manager.add_user("User", "1234")  # Assigns default USER role

print("\nFinal user data:")
print(task_manager.users)

logged_in_user = None  # Initialize logged_in_user variable
try:
  while True:
    print("\nTask Manager Menu:")
    if not logged_in_user:
        print("1. Login")
        print("2. Create Task")
        print("3. List Tasks")
        print("4. Manage Task Status")
        print("5. Delete Task")
        print("6. Set Task Due Date")
        print("7. Show Due Date Reminders")
        print("(Please Login to Create Tasks, Manage Tasks, and Delete Tasks,etc)")
        print("10. Exit")
    else:
        print(f"1. Logout ({logged_in_user.username})")
        print("2. Create Task")
        print("3. List Tasks")
        print("4. Manage Task Status")
        print("5. Delete Task")
        print("6. Set Task Due Date")
        print("7. Show Due Date Reminders")
        if logged_in_user.role == Role.ADMIN:
          print("8. Delete All Tasks")
          print("9. Create User")
        print("10. Exit")

    choice = input("Enter your choice: ")

    if choice == "1" and not logged_in_user:
        logging.info("User attempting to log in.")
        logged_in_user = task_manager.login()
        if logged_in_user:
            # Allow further actions for logged-in user
            pass
    elif choice == "1" and logged_in_user:
        logging.info("User logging out.")
        logged_in_user = None
        print("Logout successful!")
    elif choice == "8" and logged_in_user and logged_in_user.role == Role.ADMIN:
        logging.info("Admin attempting to delete all tasks.")
        confirmation1 = input("Are you sure you want to delete all tasks? (yes/no): ")
        if confirmation1.lower() == "yes":
            confirmation2 = input("This action is irreversible. Double-confirm by typing 'DELETE ALL': ")
            if confirmation2 == "DELETE ALL":
                task_manager.tasks = []  # Delete all tasks
                print("All tasks deleted successfully!")
            else:
                print("Operation canceled.")
        else:
            print("Operation canceled.")
    elif choice == "4" and logged_in_user:
        logging.info("User attempting to manage task status.")
        task_manager.mark_task_status(logged_in_user)
    
    elif choice == "2":
        task_manager.create_task(logged_in_user)
    elif choice == "3":
        task_manager.list_tasks(logged_in_user.username if logged_in_user else "")
    elif choice == "5":
        task_manager.delete_task(logged_in_user)
    elif choice == "6":
        task_manager.set_task_due_date(logged_in_user)
    elif choice == "7":
        task_manager.show_due_date_reminders()
    elif choice == "9" and logged_in_user and logged_in_user.role == Role.ADMIN:
        task_manager.create_user(logged_in_user)
    elif choice == "10":
        task_manager.save_tasks()  # Call save_tasks method before exiting
        break
    else:
        print("Invalid choice.")
except KeyboardInterrupt:
    task_manager.exit_program()