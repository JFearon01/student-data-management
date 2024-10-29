import tkinter
from tkinter import ttk
from tkinter import messagebox
import csv

  
def add_student():
    try:
        student_id = student_id_entry.get()
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        subject = subject_combobox.get()
        grade = grade_spinbox.get()

        if not (student_id and firstname and lastname and subject and grade):
            tkinter.messagebox.showerror("Error", "All fields must be filled!")
            return

        grade = int(grade)

        if not (0 <= grade <= 100):
            tkinter.messagebox.showerror("Error", "Grade must be a number between 0 and 100!")
            return

        if student_id in students:
            students[student_id]["Subjects"].append(subject)
            students[student_id]["Grades"].append(grade)
        else:
            students[student_id] = {"First Name": firstname, "Last Name": lastname,
                                    "Subjects": [subject], "Grades": [grade]}

        calculate_average(student_id)
        update_display()
    except ValueError:
        tkinter.messagebox.showerror("Error", "Grade must be a valid number!")


def calculate_average(student_id):
    grades = students[student_id]["Grades"]
    average_grade = sum(grades) / len(grades)
    students[student_id]["Average Grade"] = average_grade


def save_data():
    try:
        with open("student_data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Student ID", "First Name", "Last Name", "Subject", "Grade"])
            for student_id, info in students.items():
                for i in range(len(info["Subjects"])):
                    writer.writerow([student_id, info["First Name"], info["Last Name"],
                                     info["Subjects"][i], info["Grades"][i]])
    except IOError:
        tkinter.messagebox.showerror("Error", "Failed to save data to file!")


def load_data():
    try:
        students.clear()
        with open("student_data.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                student_id, firstname, lastname, subject, grade = row
                if student_id in students:
                    students[student_id]["Subjects"].append(subject)
                    students[student_id]["Grades"].append(int(grade))
                else:
                    students[student_id] = {"First Name": firstname, "Last Name": lastname,
                                            "Subjects": [subject], "Grades": [int(grade)]}
        for student_id in students.keys():
            calculate_average(student_id)
        update_display()
    except IOError:
        tkinter.messagebox.showerror("Error", "Failed to load data from file!")


def update_display():
    output_text.delete(1.0, tkinter.END)
    for student_id, info in students.items():
        output_text.insert(tkinter.END, f"Student ID: {student_id}\n")
        output_text.insert(tkinter.END, f"Name: {info['First Name']} {info['Last Name']}\n")
        output_text.insert(tkinter.END, "Subjects and Grades:\n")
        for i in range(len(info["Subjects"])):
            output_text.insert(tkinter.END, f"{info['Subjects'][i]}: {info['Grades'][i]}\n")
        if "Average Grade" in info:
            output_text.insert(tkinter.END, f"Average Grade: {info['Average Grade']}\n")
        else:
            output_text.insert(tkinter.END, "\n")

    # Calculate and display highest and lowest grades
    all_grades = [grade for info in students.values() for grade in info['Grades']]
    if all_grades:
        highest_grade = max(all_grades)
        lowest_grade = min(all_grades)
        output_text.insert(tkinter.END, f"\nHighest Grade: {highest_grade}\n")
        output_text.insert(tkinter.END, f"Lowest Grade: {lowest_grade}\n")

def edit_student():
    try:
        student_id = student_id_entry.get()
        if student_id not in students:
            tkinter.messagebox.showerror("Error", "Student ID not found!")
            return

        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        subject = subject_combobox.get()
        grade = grade_spinbox.get()

        if not (firstname and lastname and subject and grade):
            tkinter.messagebox.showerror("Error", "All fields must be filled!")
            return

        grade = int(grade)

        if not (0 <= grade <= 100):
            tkinter.messagebox.showerror("Error", "Grade must be a number between 0 and 100!")
            return

        students[student_id] = {"First Name": firstname, "Last Name": lastname,
                                "Subjects": [subject], "Grades": [grade]}
        calculate_average(student_id)
        update_display()
    except ValueError:
        tkinter.messagebox.showerror("Error", "Grade must be a valid number!")


def delete_student():
    student_id = student_id_entry.get()
    if student_id not in students:
        tkinter.messagebox.showerror("Error", "Student ID not found!")
        return

    del students[student_id]
    update_display()

def calculate_average_grade():
    student_id = student_id_entry.get()
    if student_id not in students:
        tkinter.messagebox.showerror("Error", "Student ID not found!")
        return

    grades = students[student_id]["Grades"]
    if not grades:
        tkinter.messagebox.showerror("Error", "No grades available for this student!")
        return

    average_grade = sum(grades) / len(grades)
    tkinter.messagebox.showinfo("Average Grade", f"The average grade for this student is: {average_grade}")

# Modify the buttons




window = tkinter.Tk()
window.title("Student Data Management")

frame = tkinter.Frame(window)
frame.pack()

# Saving User Info
user_info_frame = tkinter.LabelFrame(frame, text="Student Information")
user_info_frame.grid(row=0, column=0, padx=10, pady=10)

student_id_label = tkinter.Label(user_info_frame, text="ID")
student_id_label.grid(row=0, column=0)
student_id_entry = tkinter.Entry(user_info_frame)
student_id_entry.grid(row=0, column=1)

first_name_label = tkinter.Label(user_info_frame, text="First Name")
first_name_label.grid(row=1, column=0)
last_name_label = tkinter.Label(user_info_frame, text="Last Name")
last_name_label.grid(row=2, column=0)

first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=1)
last_name_entry.grid(row=2, column=1)

subject_label = tkinter.Label(user_info_frame, text="Subject")
subject_label.grid(row=3, column=0)
subject_combobox = ttk.Combobox(user_info_frame, values=["Python", "C++", "Java"])
subject_combobox.grid(row=3, column=1)

grade_label = tkinter.Label(user_info_frame, text="Grade")
grade_label.grid(row=4, column=0)
grade_spinbox = tkinter.Spinbox(user_info_frame, from_=0, to=100)
grade_spinbox.grid(row=4, column=1)

# Buttons
button_add = tkinter.Button(frame, text="Add Student", command=add_student)
button_add.grid(row=1, column=0, padx=10, pady=5)

button_save = tkinter.Button(frame, text="Save Data", command=save_data)
button_save.grid(row=2, column=0, padx=10, pady=5)

button_load = tkinter.Button(frame, text="Load Data", command=load_data)
button_load.grid(row=3, column=0, padx=10, pady=5)

button_edit = tkinter.Button(frame, text="Edit Student", command=edit_student)
button_edit.grid(row=1, column=1, padx=10, pady=5)

button_delete = tkinter.Button(frame, text="Delete Student", command=delete_student)
button_delete.grid(row=2, column=1, padx=10, pady=5)

button_calculate_avg = tkinter.Button(frame, text="Calculate Average Grade", command=calculate_average_grade)
button_calculate_avg.grid(row=3, column=1, padx=10, pady=5)

# Output text
output_text = tkinter.Text(window, height=20, width=50)
output_text.pack(pady=10)

students = {}

window.mainloop()
