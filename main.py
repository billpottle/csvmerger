# WARN ON DUPLICATE COL NAMES WITHIN 1 file

from tkinter import *
from tkinter import ttk
import pandas as pd
from tkinter import filedialog
from functools import partial

root = Tk()
root.geometry("800x600")
df1 = []
df2 = []
cols = []
cols2 = []
original_cols = []
original_cols2 = []
final_cols = []
merged_cols = []
matched_cols = []


def new_merge():
	pass


my_menu = Menu(root)
root.config(menu=my_menu)
file_menu = Menu(my_menu, tearoff=0 )
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New Merge', command=new_merge)
file_menu.add_command(label='Exit', command=root.quit)
help_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='About', command=new_merge)
help_menu.add_command(label='Instructions', command=root.quit)



#0 means take from first file, 1 means take from 2nd, 2 means merged
final_cols_mapping = []

def updateCols1():
	col1_sel['values'] = cols 

def updateCols2():
	col2_sel['values'] = cols2 

col1_sel = ttk.Combobox(root, value=cols, postcommand= updateCols1)
col2_sel = ttk.Combobox(root, value=cols2, postcommand = updateCols2)


def choose_merge(): 

	col1_sel.grid(row=10, column = 0, pady=10)
	col2_sel.grid(row=10, column = 1, pady=10)

	merge_cols_button = Button(root, text="Add Merge Columns", command=merge_cols)
	merge_cols_button.grid(row=11, column = 0, pady=10)

	done_cols_button.grid_forget()
	filter_cols_button.grid_forget()


def select_columns():
	global cols, cols2, cols_sel, col2_sel, done_cols_button, filter_cols_button
	
	col1_sel.grid(row=5, column = 0, pady=10)
	col2_sel.grid(row=5, column = 1, pady=10)

	#col1_sel.grid(row=10, column = 0, pady=10)
	#col2_sel.grid(row=10, column = 1, pady=10)

	#merge_cols_button = Button(root, text="Add Merge Columns", command=merge_cols)
	#merge_cols_button.grid(row=5, column = 0, pady=10)


	done_cols_button.grid(row=6,column=0, pady=10)

	
	filter_cols_button.grid(row=6, column = 1, pady=10)
	

# Add file1_col to the final column list
# Remove file1_col and file2_col from dropdowns
def merge_cols(): 
	global merged_cols, cols, cols2
	merged_cols.append((col1_sel.get(), col2_sel.get()))
	cols.remove(col1_sel.get())
	cols2.remove(col2_sel.get())
	merge_fields_label.config(text = merged_cols)


def match_cols(): 
	global matched_cols, cols, cols2
	matched_cols.append((col1_sel.get(), col2_sel.get()))
	cols.remove(col1_sel.get())
	cols2.remove(col2_sel.get())
	match_fields_label.config(text = matched_cols)


	# how to merge a row....
		# Go through each column in file 1 and 2
		# If match/merge
			#If data in 1 and 2 are the same, use data in 1
			#If data in 1 and 2 are different (couldn't be in match) use 1,2
			#If data only in 1 or only 2, use data. 
		# Else 
			# Copy data from whichever file has it. 


def merge_cells(cell1, cell2):
	cell1 = str(cell1)
	cell2 = str(cell2)
	print('cell1, cell2', cell1, cell2)
	if not cell1 and cell2: 
		return cell2
	if not cell2 and cell1: 
		return cell1
	if cell1 == cell2: 
		return cell1
	return str(cell1) + ', ' + str(cell2)

def merge_rows(row1, row2): 
	print('merging rows', row1, row2)
	result = []
	for i in range(len(final_cols_mapping)):
		if final_cols_mapping[i][0] == 0: 
			result.append(row1[final_cols_mapping[i][1]])
		if final_cols_mapping[i][0] == 1: 
			result.append(row2[final_cols_mapping[i][2]])
		if final_cols_mapping[i][0] == 2: 
			print('r12', row1, row2)
			result.append(
				merge_cells(row1[final_cols_mapping[i][1]],
				 row2[final_cols_mapping[i][2]])
				 )
	
	return result


# Note: Each column name in each file should be unique within the file. 
# Exact column names within 2 files should be merged

# Returns the position of the column in the row
# get_col_pos('email', ['name', 'email', 'phone']) = 1
def get_col_pos(name, row): 
	for i in range(len(row)): 
		if row[i] == name:
			return i
	return -1


# Do the actual merging
def merge(): 
	global matched_cols, merged_cols, df1, df2, original_cols, original_cols2
	# Find the columns we are keeping
	# Final columns will be the first column in each of match and merge, plus cols 1 + cols 2
	final_cols = []
	final_data = []
	for i in range(len(matched_cols)): 
		(first, second) = matched_cols[i]
		final_cols.append(first)
		final_cols_mapping.append([0, get_col_pos(first, original_cols), -1])		

	for i in range(len(merged_cols)): 
		(first, second) = merged_cols[i]
		final_cols.append(first)
		final_cols_mapping.append([2, get_col_pos(first, original_cols), get_col_pos(second, original_cols2)])

	for i in range(len(cols)): 
		if i != 0:
			final_cols.append(cols[i])
			final_cols_mapping.append([0, get_col_pos(cols[i], original_cols), -1])

	for i in range(len(matched_cols)): 
		(first, second) = matched_cols[i]
		final_cols.append(second)
		final_cols_mapping.append([1, -1, get_col_pos(second, original_cols2)])
	
	for i in range(len(cols2)): 
		if i != 0: 
			final_cols.append(cols2[i])
			final_cols_mapping.append([1, -1, get_col_pos(cols2[i], original_cols2)])

	print('Final cols are', final_cols)
	print('Final cols mapping', final_cols_mapping)
	


	test_data = []
	test_data.append(df1.iloc[1].values)

	to_drop = []
	# For merge cols, copy all data to df1 and delete cols from df2 before beginning

	# For each row in file 1
	for rownum in range(len(df1)): 
		row1 = df1.iloc[rownum].values
		match = False
	# Go through each row in file 2
		for rownum2 in range(len(df2)):
			row2 = df2.iloc[rownum2].values  
			# if there is a match
			# copy the row to final data with data from file 2
			# remove row from file 2
			if rows_match(row1, row2):
				final_data.append(merge_rows(row1, row2))
				match = True
				to_drop.append(rownum2)
		# copy the row to final data
		if match == False:
			final_data.append(row1)

	# Any remaining rows in df2 are not present in df1 
	print('to drop', to_drop)
	df2 = df2.drop(to_drop)
	print(df2)
	for rownum2 in range(len(df2)):
		# go through final columns mapping and only put them in the correct columns..
		final_row = []
		row = df2.iloc[rownum2].values
		for colnum2 in range(len(final_cols_mapping)):
			if (final_cols_mapping[colnum2][0] == 0):
				final_row.append('')
			else: 
				final_row.append(row[final_cols_mapping[colnum2][2]])
				
		final_data.append(final_row)
		# should be able to go through final_cols_mapping and if it's 1 or 2, copy from the value


	# Maybe a good idea here to use a list of lists. New field will be id. 
	final_df = pd.DataFrame(final_data, columns = final_cols)
	print('Final data frame', final_df)
	final_df.to_csv('output.csv')


# Check if two rows match according to all match columns

def rows_match(row1, row2):

	global matched_cols, final_cols_mapping, original_cols2, original_cols
	if len(matched_cols) == 0: 
		return False 
	match = True
	for matched_col in matched_cols:
		first = get_col_pos(matched_col[0], original_cols)
		second = get_col_pos(matched_col[1], original_cols2)
		if row1[first] != row2[second]:
			match = False
	return match

# Create open dialog box function
def open_file_1():
	# Open File Dialog Box
	global df1, cols, original_cols, load_first_button
	root.filename = filedialog.askopenfilename(
	    initialdir='/guis', title="Open CSV File", filetypes = (("CSV Files","*.csv"),))
	df1 = pd.read_csv(root.filename)
	cols = list(df1.columns)
	original_cols = list(df1.columns)
	cols.insert(0, 'Column from File 1')
	check_show_begin()
	load_first_button.grid_forget()
	first_file_label = Label(root, text=root.filename + ' loaded', fg= 'blue' )
	first_file_label.grid(row=2, column = 0)


def open_file_2():
	# Open File Dialog Box
	global df2, cols2, original_cols2, load_second_button
	root.filename = filedialog.askopenfilename(
	    initialdir='/guis', title="Open CSV File", filetypes = (("CSV Files","*.csv"),))
	df2 = pd.read_csv(root.filename)
	cols2 = list(df2.columns)
	original_cols2 = list(df2.columns)
	cols2.insert(0, 'Column from File 2')
	check_show_begin()
	load_second_button.grid_forget()
	second_file_label = Label(root, text=root.filename + ' loaded', fg= 'red' )
	second_file_label.grid(row=2, column = 1)


def check_show_begin():
	global df1, df2
	if len(df1) > 0 and len(df2) > 0:
		select_columns()



intro = Label(root, text='Welcome to CSV Merger. Follow the steps below or choose help in the menu for details')
intro.grid(row=0, column= 0, pady=10, columnspan=2)

step_1 = Label(root, text="Step 1 - Choose 2 files to merge:", font=('Helvetica', 24))
step_1.grid(row=1, column = 0, pady=10, columnspan=2)


global load_first_button
load_first_button = Button(root, text="Load First File", bg = '#FFFFFF', command=open_file_1)
load_first_button.grid(row=2, column = 0)
load_second_button = Button(root, text="Load Second File",bg = '#FFFFFF', command=open_file_2)
load_second_button.grid(row=2, column = 1)

step_2 = Label(root, text="Step 2 - Choose Match Columns:", font=('Helvetica', 24))
step_2.grid(row = 3, column = 0, pady=10, columnspan=2)
step2_ins = Label(root, text="Match columns are columns where you want to check if both files have an equal value.")
step2_ins.grid(row = 4, columnspan = 2)

done_cols_button = Button(root, text="Match Columns Complete", command=choose_merge, fg = '#FFFFFF', bg = 'green')
filter_cols_button = Button(root, text="Add Match Column", command=match_cols)

match_fields_label = Label(root, text='Match columns = ')
match_fields_label.grid(row = 7, column = 0, columnspan = 2)


step_3 = Label(root, text="Step 3 - Choose Merge Columns:", font=('Helvetica', 24))
step_3.grid(row=8, column = 0, pady=10, columnspan=2)
step3_ins = Label(root, text='Merge columns are those that you want to merge together regardless')
step3_ins.grid(row=9, column = 0, pady=10)

# row 1o is the selects
# row 11 is the button

merge_label = Label(root, text="Columns To be merged regardless")
merge_label.grid(row = 12, column = 0)
merge_fields_label = Label(root, text='Merge columns = ')
merge_fields_label.grid(row = 13, column = 0)

step_3 = Label(root, text="Step 4 - Finalize merge to output.csv:", font=('Helvetica', 24))
step_3.grid(row=14, column = 0, pady=10, columnspan=2)

merge_button = Button(root, text="Complete Merge", fg = '#FFFFFF', bg = 'green' , command = merge)
merge_button.grid(row = 15, column = 0, columnspan = 2)

# POPUP###############################
from tkinter import messagebox
def pop():
	messagebox.showinfo("Title", "Hello World!")


mainloop()
