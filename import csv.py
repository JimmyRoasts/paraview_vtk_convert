import os
import pandas as pd
import numpy as np
from pyevtk.hl import pointsToVTK
from tkinter import Tk, filedialog

def convert_date_to_decimal_year(date):
    if pd.isna(date):
        return np.nan  # Handle missing dates
    year = date.year
    month_fraction = (date.month - 1) / 12
    return year + month_fraction

def generate_vtk_from_csv(csv_file=None, has_headers=True):
    if csv_file is None:
        # If no file is passed, open a file dialog to select CSV file
        root = Tk()
        root.withdraw()  # Hide the root window
        csv_file = filedialog.askopenfilename(initialdir=os.path.dirname(__file__), title="Select CSV file", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
    
    # Load the CSV file
    data = pd.read_csv(csv_file, header=0 if has_headers else None)
    
    # Detect and convert date columns to Decimal Year format
    if 'Start' in data.columns:
        data['Start'] = pd.to_datetime(data['Start'], dayfirst=True, errors='coerce')  # Assume dd/mm/yyyy format
        print(f"Converted 'Start' dates to decimal year format.")
        # Check for invalid dates
        invalid_dates = data['Start'][data['Start'].isna()]
        if len(invalid_dates) > 0:
            print(f"Warning: Found {len(invalid_dates)} invalid dates. These will be skipped.")
        data['DecimalYear'] = data['Start'].apply(convert_date_to_decimal_year)
    else:
        raise ValueError("The 'Start' column is missing in the CSV file.")
    
    # Ensure Step is numeric
    if 'Step' in data.columns:
        data['Step'] = pd.to_numeric(data['Step'], errors='coerce').fillna(0).astype(int)
        print("Converted 'Step' to numeric format.")
    else:
        raise ValueError("The 'Step' column is missing in the CSV file.")
    
    # Set up output file paths
    output_dir = os.path.dirname(csv_file)
    base_filename = os.path.splitext(os.path.basename(csv_file))[0]
    
    # Prepare dummy coordinates
    x = np.zeros(len(data))
    y = np.zeros(len(data))
    z = np.zeros(len(data))
    
    # Prepare VTK files (one for each row, associated with each timestep)
    vtk_files = []
    for i, row in data.iterrows():
        if pd.isna(row['DecimalYear']):
            continue  # Skip rows with invalid dates
        vtk_output_path = os.path.join(output_dir, f"{base_filename}_{i}")
        pointsToVTK(vtk_output_path, x, y, z, data={col: np.array([row[col]]) for col in data.columns if np.issubdtype(data[col].dtype, np.number)})
        vtk_files.append(f"{base_filename}_{i}.vtu")
        print(f"VTK file saved as {vtk_output_path}.vtu")
    
    # Create a PVD file to define timesteps
    pvd_file_path = os.path.join(output_dir, base_filename + '.pvd')
    
    # Use 'DecimalYear' as the time step
    timesteps = data['DecimalYear'].dropna().values  # Ensure no NaN values are used
    
    with open(pvd_file_path, 'w') as pvd_file:
        pvd_file.write('<VTKFile type="Collection" version="0.1" byte_order="LittleEndian">\n')
        pvd_file.write('    <Collection>\n')
        
        # Use the actual decimal year for the timestep
        for timestep, vtk_file in zip(timesteps, vtk_files):
            # Ensure that timestep is written as a float with enough precision
            pvd_file.write(f'        <DataSet timestep="{timestep:.6f}" file="{vtk_file}"/>\n')
        
        pvd_file.write('    </Collection>\n')
        pvd_file.write('</VTKFile>\n')

    
    print(f"PVD file saved as {pvd_file_path}")

# Example usage
generate_vtk_from_csv()  # You can specify csv_file="path/to/csv" if you want to call with a specific file
