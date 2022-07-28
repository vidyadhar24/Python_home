# import tkinter as tk
# import tkinter.filedialog as tkfd
# import tkinter.messagebox as tkms

# root = tk.Tk()
# root.geometry("400x400")


# def save_as_file():
#     open_dialog = tkfd.asksaveasfile(mode='w', defaultextension='.txt')
#     print(open_dialog.name)


# btn = tk.Button(root, text='someting', command=save_as_file)
# btn.pack()


# root.mainloop()
import re
match = "This is my personal notepad this \n 123 is new This is a smart one"

pattern = re.compile(r'\w*.')
result = pattern.findall(match)
print(result.count)
