from pylsl import StreamInlet, resolve_stream
import time  
import serial # to send data to the serial port 

"""Configure the lsl device.
		Helpful code snippets:
			https://snyk.io/advisor/python/pylsl/functions/pylsl.resolve_stream
			https://github.com/OpenBCI/OpenBCI_GUI/blob/master/Networking-Test-Kit/LSL/lslStreamTest_3Streams.py
        """

CAR_LEFT = b'L'
CAR_RIGHT = b'R'
CAR_FORWARD = b'F'
CAR_BACKWARD = b'B'
CAR_STOP = b'S'

# Set Serial port config
SERIAL_PORT = '/dev/cu.usbmodem14101' # update this to where your arudunio USB is connected
BAUD_RATE = 9600 # ensure your aruduino is using the same baud rate
# Serial port config - We will write/command on this port - Arduino will read from here						
ser = serial.Serial(SERIAL_PORT, BAUD_RATE) # SerialPort, baudRate and timeOut parameters

# Resolve and Open LSL streams for 'EMG' data.
stream_emg = resolve_stream('type', 'EMG')
print('EMG - Opening stream')

# create a new inlet to read from the stream
inlet_emg = StreamInlet(stream_emg[0])

# info - just to print details
info_inlet_emg = inlet_emg.info()
# print("EMG - The stream's XML meta-data is: ", info_inlet_emg.as_xml())

# Setting thresholds
TIME_THRES = 2000 #2000 milliseconds
DATA_THRES = 0.90 # We can keep threshold to confirm that particualar signal received - update as needed
serial_port_new_msg = ''
prev_time = 0

# Start reading data from the stream	
# Writes to serial port based on EMG data from a specific channel
#  interprets or prase EMG
print('Read data - write EMG code')
while(True):
	data_emg, timestamp = inlet_emg.pull_sample() # get EMG data sample and its timestamp
	# print("got %s at time %s" % (data_emg, timestamp))

	curr_time = int(round(time.time() * 1000)) # get current time in milliseconds

	# Loop the channels until an activity is found, then return the mapped character
	for x in range(0, 3): 		
		# if activity from an electrode is detected and enough time has gone by since the last activity
		if((data_emg[x] >=  DATA_THRES) & (curr_time - TIME_THRES > prev_time)): 
			prev_time = int(round(time.time() * 1000)) # update time 
			print("got %s "  % (data_emg))
			print ('Motion detected in channel - %i, data %f > %f' % (x, data_emg[x], DATA_THRES))
			
			# For EMG, we can follow below electrode to placement mapping to allow detecting what muscle moved
			if(x == 0): #channel 1
				serial_port_new_msg = CAR_LEFT
			elif(x == 1): #channel 2
				serial_port_new_msg = CAR_RIGHT
			elif(x == 2): #channel 3
				serial_port_new_msg = CAR_BACKWARD
			elif(x == 3): #channel 4
				serial_port_new_msg = CAR_FORWARD
			else : # # May not need signal for stop.. if no signal.. then car will stop automatically
				serial_port_new_msg = CAR_STOP

			# Write to the Serial Port - Arduino connected on this serial port will read the message
			print ('sending data to the serial port-' , serial_port_new_msg)
			ser.write(serial_port_new_msg)
