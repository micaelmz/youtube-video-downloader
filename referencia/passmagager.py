from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

    done_label.config(text='The password has been copied to the clipboard')

# ---------------------------- SAVE PASSWORD ------------------------------- #
# IDEA, SALVAR ENCRIPTADO EM UM .DAT E DPS CONSEGUIR CARREGAR AS INFOS USANDO ESSE APP
# CASO TENHA A SENHA MESTRA PRA DESENCRIPTAR


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title='Oops', message='Please, don\'t leave any fields empty!')
        done_label.config(text='')
    else:
        is_ok = messagebox.askokcancel(title=website, message=f'These are the details entered:\nEmail: {email}\nPassword: {password}\nIs it ok to save?')

        if is_ok:
            try:
                with open('data.json', 'r', encoding='utf-8') as data_file:
                    # Reading old file
                    data = json.load(data_file)
            except FileNotFoundError:
                with open('data.json', 'w', encoding='utf-8') as data_file:
                    # Creating a new file
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating an old file with new data (append)
                data.update(new_data)
                # Saving a new data into an old file
                with open('data.json', 'w', encoding='utf-8') as data_file:
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                done_label.config(text='Your data has been successfully saved!')

        else:
            done_label.config(text='')


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_password():
    website = website_entry.get()
    try:
        with open('data.json', 'r', encoding='utf-8') as data_file:
            # Reading old file
            data = json.load(data_file)
            email = data[website]['email']
            password = data[website]['password']
    except FileNotFoundError:
        messagebox.showerror(title='Error', message='No Data File Found')
    except KeyError:
        messagebox.showerror(title='Error', message=f'No Data Found For The Website: {website}')
    else:
        messagebox.showinfo(title=website, message=f'Email: {email}\nPassword: {password}')
    finally:
        pass

# ---------------------------- UI SETUP ------------------------------- #


# Screen settings
root = Tk()
icon = PhotoImage(file='logo.png')
root.iconphoto(False, icon)
root.title('Password Manager')
root.config(padx=50, pady=50)

# Main Canvas
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo)
canvas.grid(row=1, column=2)

# Labels
website_label = Label(text='Website:')
website_label.grid(row=2, column=1)
email_label = Label(text='Email/Username:')
email_label.grid(row=3, column=1)
password_label = Label(text='Password:')
password_label.grid(row=4, column=1)
done_label = Label(text='', width=47, fg='green')
done_label.grid(row=6, column=2, columnspan=2)

# Entry's
website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(row=2, column=2)
email_entry = Entry(width=55)
email_entry.insert(0, 'micaelmuniz6@gmail.com')
email_entry.grid(row=3, column=2, columnspan=2)
password_entry = Entry(width=35)
password_entry.grid(row=4, column=2)

# Buttons
generate_password_button = Button(text='Generate Password', width=15, command=generate_password)
generate_password_button.grid(row=4, column=3)
add_button = Button(text='Add', width=47, command=save)
add_button.grid(row=5, column=2, columnspan=2)
search_button = Button(text='Search', width=15, command=search_password)
search_button.grid(row=2, column=3)

root.mainloop()
