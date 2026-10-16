# Issues found and fixes made

The line numbers below refer to the original assigned file.
Bandit reported one medium finding and two low findings. It reported
no high findings. Pylint and Flake8 use message categories rather than
Bandit severity levels.

<table>
<tr>
<th>Issue</th>
<th>Type</th>
<th>Line(s)</th>
<th>Description</th>
<th>Fix Approach</th>
</tr>
<tr>
<td>Executable discount input</td>
<td>Security. Bandit B307, medium severity. Pylint W0123.</td>
<td>24 to 27 and 51 to 52</td>
<td>eval can run Python entered at the discount prompt.</td>
<td>Read only the documented multiplication and subtraction forms and calculate the result directly.</td>
</tr>
<tr>
<td>Stock errors are ignored</td>
<td>Bandit B110, low severity. Pylint W0718.</td>
<td>29 to 34</td>
<td>The broad exception handler hides errors without a message.</td>
<td>Catch KeyError and print the unknown product instead of ignoring the error.</td>
</tr>
<tr>
<td>Receipt number generator</td>
<td>Bandit B311, low severity.</td>
<td>21</td>
<td>The random module is not suitable when a value needs to be unpredictable. The practical risk is limited because these labels are not access credentials.</td>
<td>Use secrets.randbelow to generate the same four digit receipt labels. This does not guarantee unique numbers.</td>
</tr>
<tr>
<td>Shared default list</td>
<td>Bug. Pylint W0102.</td>
<td>10 and 19</td>
<td>The same default receipt list is reused across calls.</td>
<td>Use None as the default and create a fresh list inside the function.</td>
</tr>
<tr>
<td>Bare exception</td>
<td>Pylint W0702 and Flake8 E722.</td>
<td>13 to 17</td>
<td>The checkout handler catches every exception, including unexpected programming errors.</td>
<td>Catch only KeyError, TypeError and IndexError while retaining the original handling of invalid cart entries.</td>
</tr>
<tr>
<td>Receipt file handling</td>
<td>Pylint R1732 and W1514.</td>
<td>36 to 39</td>
<td>The receipt file is not explicitly closed and its encoding depends on the machine.</td>
<td>Use a with statement and specify UTF8 encoding.</td>
</tr>
<tr>
<td>Unused imports and variable</td>
<td>Pylint W0611 and W0612. Flake8 F401 and F841.</td>
<td>1, 3 and 26</td>
<td>json and logging are unused. The tools also cannot follow the total reference inside the evaluated string.</td>
<td>Remove the unused imports and refer directly to sales_total in the safe discount calculation.</td>
</tr>
<tr>
<td>Missing descriptions</td>
<td>Pylint C0114 and C0116.</td>
<td>1, 10, 24, 29, 36, 41 and 44</td>
<td>The module and functions have no descriptions.</td>
<td>Add short docstrings explaining their purpose.</td>
</tr>
<tr>
<td>Naming and string formatting</td>
<td>Pylint C0103 and C0209.</td>
<td>21 and 41</td>
<td>printSales does not follow normal Python naming, and the receipt uses older string formatting.</td>
<td>Rename the function to print_sales and use a formatted string for receipt text.</td>
</tr>
<tr>
<td>Spacing and long lines</td>
<td>Flake8 E302, E305 and E501.</td>
<td>10, 21, 24, 29, 36, 41, 44 and 56</td>
<td>Some definitions need more blank lines, and one expression exceeds the line limit.</td>
<td>Add the required blank lines and wrap long expressions.</td>
</tr>
</table>

After the changes, Pylint scores 9.62 out of 10, which is above
the required 9.5. Two messages remain for the original global sales
variable name and the global statement. Bandit reports no findings,
and Flake8 reports no messages.

The original reports are in `reports/before`. The final reports are
in the main folder. An empty Flake8 report means that no issues were
found. No warnings were suppressed and no line limits were changed.
