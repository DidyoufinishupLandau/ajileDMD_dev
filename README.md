# DMD---PSI

The code is built on python=3.8.x on Windows 10. 

## How to run
The code is based on two primary components:
- DMD_driver.py which provides DMD_driver class. This is used to control the DMD,
and is based on the ajiledriver
- adc_driver.py which provides adc_driver class. This is used to control an appropriately
coded RaspberryPi.

For example:

```python
import numpy as np
from DMD_main import control_DMD
import time
import generate_pattern

call_pattern = generate_pattern.DmdPattern('hadamard', 128, 128, gray_scale=255)
hadamard_pattern = call_pattern.execute()
# define a 3D array with form [[mask], [mask], [mask]...]
cd = control_DMD(hadamard_pattern, project_name = "my_project", main_sequence_itr=1, frame_time=50)
cd.execute()
```
## Higher level image handling

We also have data structure to handle the data transfer between the computer and the DMD.
This is provided in the DMD_structures.py file:

```python
from DMD_driver import DMD_driver
from DMD_structures import dmd_image

# Connect to the driver
dmd = DMD_driver()
# Create an image (can be a named pattern, numpy array, or none)
image_to_project = dmd_image(dmd_driver=dmd, image='random_50_50')
# We can directly project this
image_to_project.project()
```
