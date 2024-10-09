#!/usr/bin/env python
# ecef_to_eci.py
#
# Converts ECEF components to ECI
#
# Usage: python3 ecef_to_eci.py year month day hour minute second
#                               ecef_x_km ecef_y_km ecef_z_km
#
# Written by Blake Batchelor, batchelorbh@vt.edu
# Other contributors: none
#
# Parameters:
#    year                input year
#    month               input month
#    day                 input day
#    hour                input hour
#    minute              input minute
#    second              input second
#    ecef_x_km           ECEF x component
#    ecef_y_km           ECEF y component
#    ecef_z_km           ECEF z component
#
# Output:
#    Prints ECI components to the screen
#
# Revision history:
#    09/29/2024          Script created
#
###############################################################################

#Import relevant modules
import sys
from math import pi, fmod, cos, sin

#Define constants
R_E_KM = 6378.137
E_E = 0.081819221456
W = 7.292115e-5

#Calculate denominator for SE and CE equations
def calc_denom(ecc, lat_rad):
   return sqrt(1 - ecc**2 * sin(lat_rad)**2)

#Pre-initialize input parameters
year = float('nan') #Input year
month = float('nan') #Input month
day = float('nan') #Input day
hour = float('nan') #Input hour
minute = float('nan') #Input minute
second = float('nan') #Input second
ecef_x_km = float('nan') #ECEF x component in km
ecef_y_km = float('nan') #ECEf y component in km
ecef_z_km = float('nan') #ECEF z component in km

#Arguments are strings by default
if len(sys.argv) == 10:
   year = float(sys.argv[1])
   month = float(sys.argv[2])
   day = float(sys.argv[3])
   hour = float(sys.argv[4])
   minute = float(sys.argv[5])
   second = float(sys.argv[6])
   ecef_x_km = float(sys.argv[7])
   ecef_y_km = float(sys.argv[8])
   ecef_z_km = float(sys.argv[9])
else:
   print(('Usage: python3 ecef_to_eci.py year month day hour minute second '
                         'ecef_x_km ecef_y_km ecef_z_km'))
   sys.exit()

#Main body of script

#Calculate fractional Julian date
jd = day - 32075.0 \
     + int(1461.0 * (year + 4800.0 + int((month - 14.0) / 12.0)) / 4.0) \
     + int(367.0 * (month - 2.0 - int((month - 14.0) / 12.0) * 12.0) /12.0) \
     - int(3.0 * (int((year + 4900.0 + int((month - 14.0) / 12.0)) / 100.0)) / 4.0)

jd_mid = jd - 0.5
d_frac = (second + 60 * (minute + 60 * hour)) / 86400
jd_frac = jd_mid + d_frac

#Calculate GMST angle
TUT1 = (jd_frac - 2451545.0) / 36525

GMST = 67310.54841 + (876600 * 60 * 60 + 8640184.812866) * TUT1 \
       + 0.093104 * TUT1**2 + -6.2e-6 * TUT1**3

GMST_rad = fmod(fmod(GMST, 86400) * W + 2 * pi, 2 * pi)

#Calculate ECI components
eci_x_km = ecef_x_km * cos(-GMST_rad) + ecef_y_km * sin(-GMST_rad)
eci_y_km = -ecef_x_km * sin(-GMST_rad) + ecef_y_km * cos(-GMST_rad)
eci_z_km = ecef_z_km

#Print ECI components
print(eci_x_km)
print(eci_y_km)
print(eci_z_km)
