from tkinter import *
from tkinter import ttk
import pandas as pd
from tkinter import filedialog
from functools import partial

root = Tk()
root.geometry("400x400")
df1 = []
df2 = []
cols = []
cols2 = []
final_cols = []
merged_cols = []


def updateCols1():
	col1_sel['values'] = cols 

def updateCols2():
	col2_sel['values'] = cols2 

col1_sel = ttk.Combobox(root, value=cols, postcommand= updateCols1)
col2_sel = ttk.Combobox(root, value=cols2, postcommand = updateCols2)


def select_columns():
	global cols, cols2, cols_sel, col2_sel
	label = Label(root, text="Select columns from file 1 to merge with file 2")
	label.pack()
	
	col1_sel.pack(pady=10)
	col2_sel.pack(pady=10)

	merge_cols_button = Button(root, text="Merge Columns", command=merge_cols)
	merge_cols_button.pack()
	

# Add file1_col to the final column list
# Remove file1_col and file2_col from dropdowns
def merge_cols(): 
	global final_cols, cols, cols2
	print(cols, col1_sel.get())
	merged_cols.append((col1_sel.get(), col2_sel.get()))
	cols.remove(col1_sel.get())
	cols2.remove(col2_sel.get())
	print(merged_cols)


# Do the actual merging
def merge(): 
	
	# Find the columns we are keeping
	final_cols = cols + cols2
	
	# go through each row

	# Need a list of lists for the final data
	final_data = dict()
	for ind in df1.index: 
		record = []
		for col in cols:
			#print(df1[col][ind]) 
			record.append(df1[col][ind])
		final_data[ind] = record
		
	print('Final Data', final_data)
	# Maybe a good idea here to use a list of lists. New field will be id. 
	final_df = pd.DataFrame(final_data, columns = final_cols)
	print('Final data frame', final_df)
	final_df.to_csv('output.csv')
# Create open dialog box function


def open_file_1():
	# Open File Dialog Box
	global df1, cols
	root.filename = filedialog.askopenfilename(
	    initialdir='/guis', title="Open CSV File", filetypes = (("CSV Files","*.csv"),))
	df1 = pd.read_csv(root.filename)
	cols = list(df1.columns)
	cols.insert(0, 'Column from File 1')
	load_first_button.pack_forget()
	check_show_begin()

def open_file_2():
	# Open File Dialog Box
	global df2, cols2
	root.filename = filedialog.askopenfilename(
	    initialdir='/guis', title="Open CSV File", filetypes = (("CSV Files","*.csv"),))
	df2 = pd.read_csv(root.filename)
	cols2 = list(df2.columns)
	cols2.insert(0, 'Column from File 2')
	load_second_button.pack_forget()
	check_show_begin()


def show_select(options):
	my_combo = ttk.Combobox(root, value=options)
	my_combo.current(0)
	my_combo.pack(pady=10)


def check_show_begin():
	global df1, df2
	if len(df1) > 0 and len(df2) > 0:
		start_button = Button(root, text="Select Columns", command=select_columns)
		start_button.pack()




global load_first_button
load_first_button = Button(root, text="Load First File", command=open_file_1)
load_first_button.pack()
load_second_button = Button(root, text="Load Second File", command=open_file_2)
load_second_button.pack()


# POPUP###############################
from tkinter import messagebox
def pop():
	messagebox.showinfo("Title", "Hello World!")

pop_button = Button(root, text="Popup", command=pop).pack()

mainloop()
