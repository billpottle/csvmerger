from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
from nicknameparser import *

root = Tk()
root.geometry("1000x800")

nicknames = NameDenormalizer()

def new_merge():

	# Restore Data State
	df1 = []
	df2 = []
	cols = []
	cols2 = []
	original_cols = []
	original_cols2 = []
	final_cols = []
	merged_cols = []
	matched_cols = []
	final_cols_mapping = []

	# Restore UI state
	load_first_button.grid(row=2, column = 0)
	load_second_button.grid(row=2, column = 1)

	col1_sel.grid_forget()
	col2_sel.grid_forget()

	done_cols_button.grid_forget()
	filter_cols_button.grid_forget()
	first_file_label.grid_forget()
	second_file_label.grid_forget()
	add_or_button.grid_forget()

# Initialize Menu
my_menu = Menu(root)
root.config(menu=my_menu)
file_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New Merge', command=new_merge)
file_menu.add_command(label='Exit', command=root.quit)
help_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='About', command=new_merge)
help_menu.add_command(label='Instructions', command=root.quit)

# Initialize Data structures
df1 = []
df2 = []
cols = []
cols2 = []
original_cols = []
original_cols2 = []
final_cols = []
merged_cols = []
matched_cols = []
#0 means take value from first file, 1 means take from 2nd, 2 means merged
final_cols_mapping = []

def updateCols1():
	col1_sel['values'] = cols 

def updateCols2():
	col2_sel['values'] = cols2 

def duplicate_col_warning():
	messagebox.showinfo("Warning", "This file contains more than one column with the same name. Please edit the original file and restart the merge")

col1_sel = ttk.Combobox(root, value=cols, postcommand= updateCols1)
col2_sel = ttk.Combobox(root, value=cols2, postcommand = updateCols2)

# Choose the columns to merge
def choose_merge(): 

	global merge_cols_button, filter_cols_button, matched_cols
	col1_sel.grid(row=10, column = 0, pady=10)
	col2_sel.grid(row=10, column = 1, pady=10)

	col1_sel.set('Column from File 1')
	col2_sel.set('Column from File 2')

	merge_cols_button = Button(root, text="Add Merge Columns", command=merge_cols)
	merge_cols_button.grid(row=11, column = 0, pady=10)
	done_merge_button.grid(row=11, column = 1, pady=10)

	if ((matched_cols[len(matched_cols) - 1]) == ('OR', 'OR')):
		matched_cols.pop()
		col1_label = Label(selected_match_cols_frame, text= '              ', bg='white')
		col1_label.grid(row=(len(matched_cols) +2) , column=0, pady = 5)

	done_cols_button.grid_forget()
	filter_cols_button.grid_forget()
	add_or_button.grid_forget()


def select_columns():
	global cols, cols2, cols_sel, col2_sel, done_cols_button, filter_cols_button
	
	col1_sel.grid(row=5, column = 0, pady=10)
	col2_sel.grid(row=5, column = 1, pady=10)

	col1_sel.set('Column from File 1')
	col2_sel.set('Column from File 2')

	add_or_button.grid(row=6,column=1, pady=10)
	done_cols_button.grid(row=6,column=2, pady=10)
	filter_cols_button.grid(row=6, column = 0, pady=10)
	

# Add file1_col to the final column list
# Remove file1_col and file2_col from dropdowns
def merge_cols(): 
	global merged_cols, cols, cols2, merge_frame

	# Make sure they have selected a column
	if (col1_sel.get() == 'Column from File 1') or (col2_sel.get() == 'Column from File 2'): 
		return

	merged_cols.append((col1_sel.get(), col2_sel.get()))
	
	col1_label = Label(selected_merge_cols_frame, text= col1_sel.get(), bg='white')
	col1_label.grid(row=(len(merged_cols) +1) , column=0, pady = 5)

	col2_label = Label(selected_merge_cols_frame, text= col2_sel.get(), bg='white')
	col2_label.grid(row=len(merged_cols) + 1 , column=1, pady = 5)
	
	cols.remove(col1_sel.get())
	cols2.remove(col2_sel.get())

	updateCols1()
	updateCols2()
	
	col1_sel.set('Column from File 1')
	col2_sel.set('Column from File 2')

# Choose cols that should be used to determine a duplicate record
def match_cols(): 
	global matched_cols, cols, cols2, selected_match_cols_frame

	if (col1_sel.get() == 'Column from File 1') or (col2_sel.get() == 'Column from File 2'): 
		return

	matched_cols.append((col1_sel.get(), col2_sel.get()))

	col1_label = Label(selected_match_cols_frame, text= col1_sel.get(), bg='white')
	col1_label.grid(row=(len(matched_cols) +1) , column=0, pady = 5)

	col2_label = Label(selected_match_cols_frame, text= col2_sel.get(), bg='white')
	col2_label.grid(row=len(matched_cols) + 1 , column=1, pady = 5)

	cols.remove(col1_sel.get())
	cols2.remove(col2_sel.get())

	updateCols1()
	updateCols2()

	col1_sel.set('Column from File 1')
	col2_sel.set('Column from File 2') 

def add_or_condition():
	global matched_cols

	if ((matched_cols[len(matched_cols) - 1]) == ('OR', 'OR')):
		return
	
	matched_cols.append(('OR', 'OR'))	
	col1_label = Label(selected_match_cols_frame, text= '---OR---', bg='white')
	col1_label.grid(row=(len(matched_cols) +1) , column=0, pady = 5)


# Determine if 2 items match
def items_match(a,b) : 
	global case_sensitive, include_nicknames
	print(a,b)
	# create a set including all nicknames
	if include_nicknames: 
		a_names = nicknames.get(a, {})
		b_names = nicknames.get(b, {})
		a_names_lower = {}
		if a_names: 
			a_names_lower = set(n.lower() for n in a_names)
		b_names_lower = {}
		if b_names: 
			b_names_lower = set(n.lower() for n in b_names)

	# Handle 4 potential cases
	if case_sensitive and not include_nicknames: 
		return a == b
	if case_sensitive and include_nicknames:
		return a == b or a in b_names or b in a_names
	if not case_sensitive and not include_nicknames:
		return a.lower() == b.lower()
	if not case_sensitive and include_nicknames: 
		return a==b or a.lower() in b_names_lower or b.lower in a_names_lower

# Merge two cells
def merge_cells(cell1, cell2):
	cell1 = str(cell1)
	cell2 = str(cell2)
	print('cell1, cell2', cell1, cell2)
	if not cell1 and cell2: 
		return cell2
	if not cell2 and cell1: 
		return cell1

	if items_match(cell1, cell2): 
		return cell1
	return str(cell1) + ', ' + str(cell2)

# how to merge a row....
	# Go through each column in file 1 and 2
	# If match/merge
		#If data in 1 and 2 are the same, use data in 1
		#If data in 1 and 2 are different (couldn't be in match) use 1,2
		#If data only in 1 or only 2, use data. 
	# Else 
		# Copy data from whichever file has it.

def merge_rows(row1, row2): 
	print('merging rows', row1, row2)
	result = []
	for i in range(len(final_cols_mapping)):
		# Copy from file 1
		if final_cols_mapping[i][0] == 0: 
			result.append(row1[final_cols_mapping[i][1]])
		# Copy from file 2
		if final_cols_mapping[i][0] == 1: 
			result.append(row2[final_cols_mapping[i][2]])
		# Merge the two cells
		if final_cols_mapping[i][0] == 2: 
			result.append(
				merge_cells(row1[final_cols_mapping[i][1]],
				 row2[final_cols_mapping[i][2]])
				 )
	
	return result


# Note: Each column name in each file should be unique within the file. 
# Exact column names between 2 files should be merged

# Returns the position of the column in the row
# for instance, get_col_pos('email', ['name', 'email', 'phone']) = 1
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


	# Create the final data frame and write to file
	final_df = pd.DataFrame(final_data, columns = final_cols)
	print('Final data frame', final_df)
	final_df.to_csv('output.csv')

	# Update UI
	merge_button.grid_forget()
	done_label = Label(root, text='Merge successfully written to output.csv', fg= 'green')
	done_label.grid(row = 16, column = 0, columnspan = 2)


# Check if two rows match according to match cols

def rows_match(row1, row2):

	global matched_cols, final_cols_mapping, original_cols2, original_cols
	if len(matched_cols) == 0: 
		return False 
	match = True

	# Extract out the or sets
	# 2 rows match if ALL conditions in ANY of the OR conditions matches. 
	or_conditions = []
	and_conditions = []
	for col in matched_cols:
		if col != ('OR', 'OR'): 
			and_conditions.append(col)
		else:
			or_conditions.append(and_conditions)
			and_conditions = []
	or_conditions.append(and_conditions)
	
	print('Or conditions are', or_conditions)
	
	for matched_col in matched_cols:
		first = get_col_pos(matched_col[0], original_cols)
		second = get_col_pos(matched_col[1], original_cols2)
		if not items_match(row1[first], row2[second]):
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
	first_file_label.config(text=root.filename + ' loaded')
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
	second_file_label.config(text=root.filename + ' loaded')
	second_file_label.grid(row=2, column = 1)


def check_show_begin():
	global df1, df2
	if len(df1) > 0 and len(df2) > 0:
		select_columns()

def start_finalize():
	global done_cols_button, filter_cols_button
	merge_button.grid(row = 16, column = 0, columnspan = 2)
	done_merge_button.grid_forget()
	merge_cols_button.grid_forget()
	col1_sel.grid_forget()
	col2_sel.grid_forget()



# Main UI Code
intro = Label(root, text='Welcome to CSV Merger. Follow the steps below or choose help in the menu for details')
intro.grid(row=0, column= 0, pady=10, columnspan=2)

step_1 = Label(root, text="Step 1 - Choose 2 files to merge:", font=('Helvetica', 18))
step_1.grid(row=1, column = 0, pady=10, columnspan=2)

case_sensitive = StringVar()
case_sensitive_box = Checkbutton(root, text='Case Sensitive', variable = case_sensitive)
case_sensitive_box.deselect()
case_sensitive_box.grid(row=15, column=0)

include_nicknames = StringVar()
include_nicknames_box = Checkbutton(root, text='Include Nicknames', variable = include_nicknames)
include_nicknames_box.deselect()
include_nicknames_box.grid(row=15, column=1)

load_first_button = Button(root, text="Load First File", bg = '#FFFFFF', command=open_file_1)
load_first_button.grid(row=2, column = 0)
first_file_label = Label(root, text='', fg= 'blue' )
	
load_second_button = Button(root, text="Load Second File",bg = '#FFFFFF', command=open_file_2)
load_second_button.grid(row=2, column = 1)
second_file_label = Label(root, text='', fg= 'red' )

step_2 = Label(root, text="Step 2 - Choose Match Columns:", font=('Helvetica', 18))
step_2.grid(row = 3, column = 0, pady=10, columnspan=2)
step2_ins = Label(root, text="Match columns are columns where you want to check if both files have an equal value.")
step2_ins.grid(row = 4, columnspan = 2)

done_cols_button = Button(root, text="Match Columns Complete", command=choose_merge, fg = '#FFFFFF', bg = 'green')
add_or_button = Button(root, text="Add Or Condition", command=add_or_condition)
filter_cols_button = Button(root, text="Add Match Column", command=match_cols)

step_3 = Label(root, text="Step 3 - Choose Merge Columns:", font=('Helvetica', 18))
step_3.grid(row=8, column = 0, pady=10, columnspan=2)
step3_ins = Label(root, text='Merge columns are those that you want to merge together regardless')
step3_ins.grid(row=9, column = 0, columnspan = 2)


# row 1o is the selects
# row 11 is the button
done_merge_button = Button(root, text="Merge Columns Complete", command=start_finalize, fg = '#FFFFFF', bg = 'green')


step_3 = Label(root, text="Step 4 - Finalize merge to output.csv:", font=('Helvetica', 18))
step_3.grid(row=14, column = 0, pady=10, columnspan=2)

merge_button = Button(root, text="Complete Merge", fg = '#FFFFFF', bg = 'green' , command = merge)

# Match Columns Frame
selected_match_cols_frame = Frame(root, width=200, height=200, bg= 'white', bd = 1)
selected_match_cols_frame.grid(row=3, column=2, rowspan = 3, padx=20, pady=20)

frame_label = Label(selected_match_cols_frame, text="Match Columns", bg = 'white')
frame_label.grid(row = 0, column = 0, columnspan = 2)

frame_file1 = Label(selected_match_cols_frame, text="File 1", fg='Red', bg='white')
frame_file1.grid(row=1, column=0)

frame_file1 = Label(selected_match_cols_frame, text="File 2", fg='blue', bg='white')
frame_file1.grid(row=1, column=1)

frame_label = Label(selected_match_cols_frame, text="					", bg='white')
frame_label.grid(row = 2, column = 0, columnspan = 2)


# Merge Columns Frame
selected_merge_cols_frame = Frame(root, width=200, height=200, bg= 'white', bd = 1)
selected_merge_cols_frame.grid(row=8, column=2, rowspan = 3, padx=20)

frame_label = Label(selected_merge_cols_frame, text="Merge Columns", bg = 'white')
frame_label.grid(row = 0, column = 0, columnspan = 2)

frame_file1 = Label(selected_merge_cols_frame, text="File 1", fg='Red', bg='white')
frame_file1.grid(row=1, column=0)

frame_file1 = Label(selected_merge_cols_frame, text="File 2", fg='blue', bg='white')
frame_file1.grid(row=1, column=1)

frame_label = Label(selected_merge_cols_frame, text="					", bg='white')
frame_label.grid(row = 2, column = 0, columnspan = 2)

merge_frame = Frame(selected_merge_cols_frame, bg='white', bd=1)
merge_frame.grid(row=3, column=0)



mainloop()
