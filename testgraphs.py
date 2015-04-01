#!/usr/bin/python
import matplotlib
matplotlib.use("Agg")

from matplotlib.dates import strpdate2num
import numpy as np
import pylab as pl

import os, time, headstails, commands

os.nice(10)

def taildata():
  f = headstails.FileExtremities('/tmp/testser.txt','r')
  # read last 600 datapoints
  F = f.tail(600)

  h = file('/tmp/taildata.txt','w')
  for c in F:
    h.write("%s" % (c) )
  h.close()

def corrs():
  C=np.loadtxt('/tmp/corr.txt',delimiter=',',converters={0:strpdate2num("%Y-%m-%d %H:%M:%S")})
  # 1 = ATMEGA vs DS18B20
  # 2 = DHT22 vs. DS18B20
  # 3 = TMP36 vs. DS18B20
  #
  # correlation coefficients a,b : f(x) =  a*x + b
  # r2 : R^2 of data to correlation coefs
  # 1,2,3 = a  (slope)
  # 4,5,6 = b  (offset)
  # 6,7,8 = r2 (R^2)

  A1 = C[:,1]
  A2 = C[:,2]
  A3 = C[:,3]
  B1 = C[:,4]
  B2 = C[:,5]
  B3 = C[:,6]
  R1 = C[:,7]
  R2 = C[:,8]
  R3 = C[:,9]

  D = matplotlib.dates.num2date(C[:,0])

  pl.close()
  print "corr.coef-a- trends"
  print ""
  pl.plot(D,A1, '.r', label='ATMEGA vs. DS18B20')
  pl.plot(D,A2, '.g', label='DHT22 vs. DS18B20')
  pl.plot(D,A3, '.b', label='TMP36 vs. DS18B20')
  pl.title('correlation trends slope (a)')
  pl.ylabel('a [-]')
  pl.grid(True)
  pl.legend(loc='upper left', prop={'size':8})
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/corr-a.png')

  pl.close()
  print "corr.coef-b- trends"
  print ""
  pl.plot(D,A4, '.r', label='ATMEGA vs. DS18B20')
  pl.plot(D,A5, '.g', label='DHT22 vs. DS18B20')
  pl.plot(D,A6, '.b', label='TMP36 vs. DS18B20')
  pl.title('correlation trends offset (b)')
  pl.ylabel('b [-]')
  pl.grid(True)
  pl.legend(loc='upper left', prop={'size':8})
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/corr-b.png')

  pl.close()
  print "corr.coef-R2- trends"
  print ""
  pl.plot(D,A1, '.r', label='ATMEGA vs. DS18B20')
  pl.plot(D,A2, '.g', label='DHT22 vs. DS18B20')
  pl.plot(D,A3, '.b', label='TMP36 vs. DS18B20')
  pl.title('correlation trends R^2 (r2)')
  pl.ylabel('r2 [-]')
  pl.grid(True)
  pl.legend(loc='upper left', prop={'size':8})
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/corr-r.png')

  return

def graphs():
  C=np.loadtxt('/tmp/taildata.txt',delimiter=',',converters={0:strpdate2num("%Y-%m-%d %H:%M:%S")})
  # 1 = ATMEGA chip
  # 2 = DS18B20
  # 3 = DHT22
  # 4 = RelHum
  # 5 = DP1
  # 6 = DP2
  # 7 = HeatIndex
  # 8 = Voltage
  # 9 = TMP36

  A1 = C[:,1]
  A1_extrema = [min(A1),max(A1)]
  A2 = C[:,2]
  A2_extrema = [min(A2),max(A2)]
  A3 = C[:,3]
  A3_extrema = [min(A3),max(A3)]
  A4 = C[:,4]
  A4_extrema = [min(A4),max(A4)]
  A5 = C[:,5]
  A5_extrema = [min(A5),max(A5)]
  A6 = C[:,6]
  A7 = C[:,7]
  A8 = C[:,8]
  A9 = C[:,9]
  A9_extrema = [min(A9),max(A9)]

  pl.close()
  ab = np.polyfit(A1,A2,1)
  fit = np.poly1d(ab)
  r2 = np.corrcoef(A1,A2)[0,1]
  print "ATMEGA vs. DS18B20"
  a1 = ab[0]
  b1 = ab[1]
  r21 = r2
  print a1, b1, r21
  print ""
  pl.plot(A1,A2,'r.', label='ATMEGA vs. DS18B20', alpha=0.7)
  pl.plot(A1_extrema,fit(A1_extrema),'c-')
  pl.annotate('{0}'.format(r2) , xy=(min(A1)+0.5,fit(min(A1))), size=6, color='c' )

  ab = np.polyfit(A3,A2,1)
  fit = np.poly1d(ab)
  r2 = np.corrcoef(A3,A2)[0,1]
  print "DHT22 vs. DS18B20"
  a2 = ab[0]
  b2 = ab[1]
  r22 = r2
  print a2, b2, r22
  print ""
  pl.plot(A3,A2,'g.', label='DHT22  vs. DB18B20', alpha=0.7)
  pl.plot(A3_extrema,fit(A3_extrema),'m-')
  pl.annotate('{0}'.format(r2) , xy=(min(A3)+0.5,fit(min(A3))), size=6, color='m' )

  ab = np.polyfit(A9,A2,1)
  fit = np.poly1d(ab)
  r2 = np.corrcoef(A9,A2)[0,1]
  print "TMP36 vs. DS18B20"
  a3 = ab[0]
  b3 = ab[1]
  r23 = r2
  print a3, b3, r23
  print ""
  pl.plot(A9,A2,'b.', label='TMP36  vs. DS18B20', alpha=0.7)
  pl.plot(A9_extrema,fit(A9_extrema),'y-')
  pl.annotate('{0}'.format(r2) , xy=(min(A9)+0.5,fit(min(A9))), size=6, color='y' )

  print "Sensor correlations graph"
  print ""
  pl.title('Sensor correlations')
  pl.xlabel("T(x) [degC]")
  pl.ylabel("T(y),DS18B20 [degC]")
  pl.grid(True)
  pl.legend(loc='upper left', prop={'size':8})
  pl.savefig('/tmp/C123.png')


  ab = np.polyfit(A5,A6,1)
  fit = np.poly1d(ab)
  r2 = np.corrcoef(A5,A6)[0,1]
  print "Dewpoint1 vs. Dewpoint2"
  print ab
  print r2
  print ""
  pl.close()
  pl.plot(A5,A6,'b.')
  pl.plot(A5_extrema,fit(A5_extrema),'b-')
  pl.title('DewPoint vs. DewPoint2')
  pl.xlabel("Dewpoint(1) [degC]")
  pl.ylabel("Dewpoint(2) [degC]")
  pl.annotate('{0}'.format(r2) , xy=(min(A5)+0.5,fit(min(A6))), size=6 )
  pl.grid(True)
  pl.savefig('/tmp/C56.png')


  D = matplotlib.dates.num2date(C[:,0])

  pl.close()
  print "Temperature trends"
  print ""
  pl.plot(D,A1, '.r', label='ATMEGA')
  pl.plot(D,A2, '.y', label='DS18B20')
  pl.plot(D,A3, '.g', label='DHT22')
  pl.plot(D,A9, '.b', label='TMP36')
  pl.title('Temperature trends')
  pl.ylabel('T [degC]')
  pl.grid(True)
  pl.legend(loc='upper left', prop={'size':8})
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/D123.png')

  pl.close()
  print "Relative humidity trend"
  print ""
  pl.plot(D,A4,'.b')
  pl.title('Relative humidity trend')
  pl.ylabel('RH [%]')
  pl.grid(True)
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/D4.png')

  pl.close()
  print "Dewpoint trends"
  print""
  pl.plot(D,A5,'.r', label='DP1')
  pl.plot(D,A6,'.b', label='DP2')
  pl.title('Dewpoint trends')
  pl.ylabel('T [degC]')
  pl.grid(True)
  pl.legend(loc='upper left', prop={'size':8})
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/D56.png')

  pl.close()
  print "Heat Index trends"
  print ""
  pl.plot(D,A7,'.b')
  pl.title('Heat Index trend')
  pl.ylabel('T [degC]')
  pl.grid(True)
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/D7.png')

  pl.close()
  print "Solar charger trend"
  print""
  pl.plot(D,A8,'.b')
  pl.title('Solar charge trend')
  pl.ylabel('Charge [V]')
  pl.grid(True)
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/D8.png')

  f = file('/tmp/corr.txt', 'a')
  od = commands.getoutput("date '+%F %H:%M:%S'")
  f.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}\n'.format(od, a1, a2, a3, b1, b2, b3, r21, r22, r23))
  f.close()

  return

if __name__ == "__main__":
  time.sleep(20)
  taildata()
  graphs()