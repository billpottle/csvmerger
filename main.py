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
matched_cols = []


def updateCols1():
	col1_sel['values'] = cols 

def updateCols2():
	col2_sel['values'] = cols2 

col1_sel = ttk.Combobox(root, value=cols, postcommand= updateCols1)
col2_sel = ttk.Combobox(root, value=cols2, postcommand = updateCols2)



match_label = Label(root, text="Columns used to determine matched records")
match_label.pack()
match_fields_label = Label(root, text='Match columns = ')
match_fields_label.pack()

merge_label = Label(root, text="Select columns from file 1 to merge with file 2")
merge_label.pack()
merge_fields_label = Label(root, text='Merge columns = ')
merge_fields_label.pack()



def select_columns():
	global cols, cols2, cols_sel, col2_sel
	label = Label(root, text="Select columns from file 1 to merge with file 2")
	label.pack()
	
	col1_sel.pack(pady=10)
	col2_sel.pack(pady=10)

	merge_cols_button = Button(root, text="Add Merge Columns", command=merge_cols)
	merge_cols_button.pack()

	filter_cols_button = Button(root, text="Add Match Columns", command=match_cols)
	filter_cols_button.pack()
	

# Add file1_col to the final column list
# Remove file1_col and file2_col from dropdowns
def merge_cols(): 
	global merged_cols, cols, cols2
	print(cols, col1_sel.get())
	merged_cols.append((col1_sel.get(), col2_sel.get()))
	cols.remove(col1_sel.get())
	cols2.remove(col2_sel.get())
	merge_fields_label.config(text = merged_cols)


def match_cols(): 
	global matched_cols, cols, cols2
	print(cols, col1_sel.get())
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
	if cell1 == '' and cell2 != '': 
		return cell2
	if cell2 == '' and cell1 != '': 
		return cell1
	if cell1 == cell2: 
		return cell1
	return cell1 + ', ' + cell2				

def merge_rows(row1, row2): 
	result = []
	for col1 in row1: 
		for col2 in row2:
			result.append(merge_cells(col1, col2))
	
	return result


# Note: Each column name in each file should be unique within the file. 
# Exact column names within 2 files should be merged

# Do the actual merging
def merge(): 
	global matched_cols, merged_cols, df1, df2
	# Find the columns we are keeping
	# Final columns will be the first column in each of match and merge, plus cols 1 + cols 2
	final_cols = []
	for i in range(len(matched_cols)): 
		(first, second) = matched_cols[i]
		final_cols.append(first)

	for i in range(len(merged_cols)): 
		(first, second) = merged_cols[i]
		final_cols.append(first)

	for i in range(len(cols)): 
		if i != 0: 
			final_cols.append(cols[i])
	
	for i in range(len(cols2)): 
		if i != 0: 
			final_cols.append(cols2[i])

	print('Final cols are', final_cols)
	
	# For each row in file 1
	print('file 1', df1)
	for rownum in range(len(df1)): 
		print('row 1 in df1', df1.iloc[rownum])
	# Go through each row in file 2
		for row2 in df2: 
		# if there is a match
		# copy the row to final data with data from file 2
		# remove row from file 2
			if rows_match(row1, row2):
				final_data.append(merge_rows(row1, row2))
				df2.drop(row2)
		# copy the row to final data
			else:
				final_data.append(row1)

	# Any remaining rows in df2 are not present in df1 
	for row2 in df2:
		final_data.append(row2)


	# Need a list of lists for the final data
	final_data = dict()
	#for ind in df1.index: 
		#record = []
		#for col in cols:
			#print(df1[col][ind]) 
			#record.append(df1[col][ind])
		#final_data[ind] = record
		
	#print('Final Data', final_data)
	# Maybe a good idea here to use a list of lists. New field will be id. 
	#final_df = pd.DataFrame(final_data, columns = final_cols)
	#print('Final data frame', final_df)
	#final_df.to_csv('output.csv')


# Check if two rows match according to all match columns
def rows_match(row1, row2):
	global matched_cols
	print('matching row 1', row1)
	print(row2)
	match = True
	for match in matched_cols:
		print(match) 
		if row1[match] != row2[match]:
			match = False
	return match

# merge a list of columns....
def merge_row(row1, row2):
	print(row1)

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

merge_button = Button(root, text="Complete Merge", command = merge)
merge_button.pack()
# POPUP###############################
from tkinter import messagebox
def pop():
	messagebox.showinfo("Title", "Hello World!")

pop_button = Button(root, text="Popup", command=pop).pack()

mainloop()
