import os
import pandas as pd
import numpy as np
from pyevtk.hl import pointsToVTK

# Automatically get the folder of the current script
current_folder = os.path.dirname(os.path.realpath(__file__))

# File paths
csv_file = os.path.join(current_folder, 'Mungari_Sequence_with_NumericTime.csv')

# Load the CSV file
data = pd.read_csv(csv_file)

# Ensure NumericTime is treated as float
data['NumericTime'] = data['NumericTime'].astype(float)

# Prepare the data (using dummy x, y, z coordinates for VTK)
x = np.zeros(len(data))  # Ensure x, y, z have the same length as the number of rows in the CSV
y = np.zeros(len(data))
z = np.zeros(len(data))
step_values = data['Step'].values  # Ensure this has the correct length
numeric_time_values = data['NumericTime'].values  # Ensure this has the correct length

# Check if lengths of arrays match
assert len(x) == len(step_values) == len(numeric_time_values), "Mismatch in array lengths."

# Create the VTK file path
for i in range(len(step_values)):
    vtk_output_path = os.path.join(current_folder, f"Mungari_Sequence_with_NumericTime_{i}")

    # Create the VTK file with NumericTime and Step under the `data` parameter
    pointsToVTK(vtk_output_path, x, y, z, 
                data={"Step": np.array([step_values[i]]), 
                      "NumericTime": np.array([numeric_time_values[i]])})

    print(f"VTK file saved as {vtk_output_path}.vtk")
