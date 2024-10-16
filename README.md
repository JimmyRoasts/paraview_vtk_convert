ParaView Time Series Visualization Project
Overview

This project aims to enhance the visualization of time series data in ParaView, focusing on mining stages and their corresponding dates. It provides a clear representation of mining progress over time, utilizing a Python script to create a .pvd file that links stages to dates.
Features

    Timeline Display: Unevenly spaced dates are displayed effectively on a timeline.
    Current Stage Indicator: The year is included in the time field, and the mining stage is displayed in the 'Step' field.
    Python Annotation: A Python annotation shows the current mining step in the visualization.
    Customizable Input: Users can prepare their input data in an Excel file, which is processed by a Python script.

Requirements

    ParaView: Ensure you have ParaView installed. This project has been tested with version X.X (replace with your version).
    Python: Python 3.x with the following packages:
        pandas
        numpy
        vtk

You can install the required packages using pip:

bash

pip install pandas numpy vtk

Setup Instructions
1. Prepare the Excel File

Create an Excel file with the following:

    A list of dates formatted as dd/mm/yyyy.
    Corresponding mining stages.
    Ensure the file has headings and includes Step 0 (the initial state).

Example:
Start	Step	Date_string
31/12/1999	0	Initial
01/01/2000	1	Jan 2000

2. Run the Python Script

Place the CSV file in the same directory as the Python script. Open the script in Python and run it. A dialog will prompt you to select your CSV file.
3. Import to ParaView

Open the generated .pvd file in ParaView. This file allows you to visualize the time series effectively.
4. Add Python Annotation

Use the Python annotation filter in ParaView to display the current mining step:

python

"Current mining step: " + str(t_index)

5. Use the Time Manager

Utilize the Time Manager in ParaView to adjust the slider and change the mining stage.
Project Structure

bash

/paraview-time-series-visualization

License

This project is licensed under the MIT License. See the LICENSE file for more information.
Acknowledgments

    Special thanks to the ParaView community for their resources and support.

Contact

For questions or suggestions, please reach out to jdavison@cavroc.com