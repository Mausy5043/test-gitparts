#!/usr/bin/python
import matplotlib
matplotlib.use("Agg")

from matplotlib.dates import strpdate2num
import numpy as np
import pylab as pl

import serial, commands, sys, time

port = serial.Serial('/dev/ttyACM0', 9600, timeout=10)

def gettelegram(cmd):
  # flag used to exit the while-loop
  abort = 0
  # countdown counter used to prevent infinite loops
  loops2go = 10
  #
  telegram = "NaN";

  while abort == 0:
    try:
      port.write(cmd)
      line = port.readline()
    except:
      # read error, terminate prematurely
      abort = 2

    if line != "":
      line = line.strip().split()
      if line[0] == cmd:
        if line[-1] == "!":
          telegram = ""
          for item in range(1,len(line)-1):
            telegram = telegram + ' {0}'.format(line[item])
          abort = 1

    loops2go = loops2go - 1
    if loops2go < 0:
      abort = 3

  # Return codes:
  # abort == 1 indicates a successful read
  # abort == 2 means that a serial port read/write error occurred
  # abort == 3 no valid data after several attempts

  return (telegram, abort)

def graphs():
  C=np.loadtxt('/tmp/testser.txt',delimiter=',',converters={0:strpdate2num("%Y-%m-%d %H:%M:%S")})
  # 1 = TMP36
  # 2 = DS18B20
  # 3 = DHT22
  # 4 = RelHum
  # 5 = DP1
  # 6 = DP2
  # 7 = HeatIndex
  # 8 = Voltage

  A1 = C[:,1]
  A1_extrema = [min(A1),max(A1)]
  A2 = C[:,2]
  A2_extrema = [min(A2),max(A2)]
  A3 = C[:,3]
  A3_extrema = [min(A3),max(A3)]
  A4 = C[:,4]
  A5 = C[:,5]
  A5_extrema = [min(A5),max(A5)]
  A6 = C[:,6]
  A7 = C[:,7]
  A8 = C[:,8]

  pl.close()
  ab = np.polyfit(A1,A2,1)
  fit = np.poly1d(ab)
  r2 = np.corrcoef(A1,A2)[0,1]
  pl.plot(A1,A2,'b.', label='TMP36 vs. DS18B20', alpha=0.7)
  pl.plot(A1_extrema,fit(A1_extrema),'y-')
  pl.annotate('{0}'.format(r2) , xy=(min(A1)+0.5,fit(min(A1))), size=6, color='b' )

  ab = np.polyfit(A1,A3,1)
  fit = np.poly1d(ab)
  r2 = np.corrcoef(A1,A3)[0,1]
  pl.plot(A1,A3,'r.', label='TMP36 vs. DHT22', alpha=0.7)
  pl.plot(A1_extrema,fit(A1_extrema),'c-')
  pl.annotate('{0}'.format(r2) , xy=(min(A1)+0.5,fit(min(A1))), size=6, color='r' )

  ab = np.polyfit(A3,A2,1)
  fit = np.poly1d(ab)
  r2 = np.corrcoef(A3,A2)[0,1]
  pl.plot(A3,A2,'g.', label='DHT22 vs. DS18B20', alpha=0.7)
  pl.plot(A3_extrema,fit(A3_extrema),'m-')
  pl.annotate('{0}'.format(r2) , xy=(min(A3)+0.5,fit(min(A3))), size=6, color='g' )

  pl.title('Sensor correlations')
  pl.xlabel("x")
  pl.ylabel("y")
  pl.grid(True)
  pl.legend(loc='upper left', prop={'size':8})
  pl.savefig('/tmp/C123.png')


  ab = np.polyfit(A5,A6,1)
  fit = np.poly1d(ab)
  r2 = np.corrcoef(A5,A6)[0,1]
  pl.close()
  pl.plot(A5,A6,'b.')
  pl.plot(A5_extrema,fit(A5_extrema),'b:')
  pl.title('DewPoint vs. DewPoint2')
  pl.xlabel("Dewpoint(1)")
  pl.ylabel("Dewpoint(2)")
  pl.annotate('{0}'.format(r2) , xy=(min(A5)+0.5,fit(min(A6))), size=6 )
  pl.grid(True)
  pl.savefig('/tmp/C56.png')


  D = matplotlib.dates.num2date(C[:,0])

  pl.close()
  pl.plot(D,A1, '.r', label='TMP36')
  pl.plot(D,A2, '.g', label='DS18*')
  pl.plot(D,A3, '.b', label='DHT22')
  pl.title('Temperature trends')
  pl.ylabel('T [degC]')
  pl.grid(True)
  pl.legend(loc='upper left', prop={'size':8})
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/D1.png')

  pl.close()
  pl.plot(D,A4,'.b')
  pl.title('Relative humidity trend')
  pl.ylabel('RH [%]')
  pl.grid(True)
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/D2.png')

  pl.close()
  pl.plot(D,A5,'.r', label='DP1')
  pl.plot(D,A6,'.b', label='DP2')
  pl.title('Dewpoint trends')
  pl.ylabel('T [degC]')
  pl.grid(True)
  pl.legend(loc='upper left', prop={'size':8})
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/D3.png')

  pl.close()
  pl.plot(D,A7,'.b')
  pl.title('Heat Index trend')
  pl.ylabel('T [degC]')
  pl.grid(True)
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/D4.png')

  pl.close()
  pl.plot(D,A8,'.b')
  pl.title('Solar charge trend')
  pl.ylabel('Charge [V]')
  pl.grid(True)
  pl.gcf().autofmt_xdate()
  pl.savefig('/tmp/D5.png')

  return

if __name__ == "__main__":
  time.sleep(7)
  telegram, status = gettelegram("S")
  time.sleep(2)
  telegram, status = gettelegram("A")
  dt = commands.getoutput("date '+%F %H:%M:%S'")
  if status == 1:
    f = file('/tmp/testser.txt', 'a')
    f.write('{0},{1}\n'.format(dt, telegram))
    f.close()

  graphs()
