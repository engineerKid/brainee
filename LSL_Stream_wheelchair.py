from pylsl import StreamInlet, resolve_stream
import time  
import serial # to send data to the serial port 

"""Configure the lsl device.
		Helpful code snippets:
			https://snyk.io/advisor/python/pylsl/functions/pylsl.resolve_stream
			https://github.com/OpenBCI/OpenBCI_GUI/blob/master/Networking-Test-Kit/LSL/lslStreamTest_3Streams.py
        """

CHAIR_LEFT = b'L'
CHAIR_RIGHT = b'R'
CHAIR_FORWARD = b'F'
CHAIR_BACKWARD = b'B'
CHAIR_STOP = b'S'

isChairStarted = False

# Serial port config - We will write/command on this port - Arduino will read from here						
# Set Serial port config
SERIAL_PORT = '/dev/cu.usbmodem14201' # update this to where your arudunio USB is connected
BAUD_RATE = 9600 # ensure your aruduino is using the same baud rate
ser = serial.Serial(SERIAL_PORT, BAUD_RATE) # SerialPort, baudRate and timeOut parameters

# LSL Stream - Resolve and Open LSL streams for 'Focus' 
stream_eeg_focus = resolve_stream('type', 'Focus')
print('EEG Focus - Opening stream')
inlet_eeg_focus = StreamInlet(stream_eeg_focus[0])  # create a new inlet to read from the stream

# LSL Stream - Resolve and Open LSL streams for 'EMG' data.
stream_emg = resolve_stream('type', 'EMG')
print('EMG - Opening stream')
inlet_emg = StreamInlet(stream_emg[0])

# Setting thresholds and other values
FAST_TIME_THRES_LOWER = 800 # = .8 sec
FAST_TIME_THRES_UPPER = 1500 # = 1.5 sec
TIME_THRES = 3000 # milliseconds
DATA_THRES = 1.0 # update as needed - strength of the signal 0.0-1.0
prev_time = 0
serial_port_new_msg = ''
prev_row_active_channel = -1 # random number to initialize

print('Start Read data.....')

data_stream_count = 0

# Start reading data from the stream	
# Writes to the serial port based on EMG data from a specific channel
while(True):
	# data_stream_count +=1
	# print('WHILE - data_stream_count = ', data_stream_count)

	# Start the chair - chair has not started so start is with EEG Focus data
	if(isChairStarted == False):
		# Keep reading from 'Focus' data stream until you can start the chair
		data_eeg_focus, timestamp = inlet_eeg_focus.pull_sample() # get focus data sample and its timestamp
		if (data_eeg_focus[0] > 0):
			prev_time = int(round(time.time() * 1000)) # update time 
			serial_port_new_msg = CHAIR_FORWARD
			print ('Received Focus - STARTING THE CHAIR.')
			ser.write(serial_port_new_msg)
			isChairStarted = True


	# Move the Chair - Chair has already started so move it with EMG data
	else:
		data_emg, timestamp = inlet_emg.pull_sample() # get EMG data sample and its timestamp
		curr_time = int(round(time.time() * 1000)) # get current time in milliseconds
		time_elapsed = curr_time - prev_time
		serial_port_new_msg = ''
		fast_activity = False
		data_for_print = False
			
		# Loop the channels until an activity is found, then return the mapped character
		# for x in range(0,3): # as we want only first 4 channels	
		for x in range(0,3,2):	# just want to read 0 and 2 channels (FP1 and T3)
			
			if((data_emg[x] >=  DATA_THRES) & (time_elapsed > FAST_TIME_THRES_LOWER)):

				# Capture fast-activity if detected in less than half second, i.e. may indicate fast blink or clench
				if (time_elapsed < FAST_TIME_THRES_UPPER): # Fast action detected
					if(prev_row_active_channel == x): 
						print ('*********Fast Motion detected in channel - %i, data %f > %f' % (x, data_emg[x], DATA_THRES))
						# print('curr_time %i - prev_time %i = %i < %i' % (curr_time, prev_time, (curr_time - prev_time), FAST_TIME_THRES_UPPER))
						prev_time = int(round(time.time() * 1000)) # update time 
						fast_activity = True
						data_for_print = True
				
				# Capture regular-activity after specified time threshold, TIME_THRES
				# if activity from an electrode is detected and enough time has gone by since the last activity
				elif(curr_time - TIME_THRES > prev_time): # Regular action detected
					# print("got %s "  % (data_emg))
					print ('********Regular Motion detected in channel - %i, data %f > %f' % (x, data_emg[x], DATA_THRES))
					# print('curr_time %i - TIME_THRES %i = %i > %i' % (curr_time, TIME_THRES,(curr_time - TIME_THRES) , prev_time))
					prev_time = int(round(time.time() * 1000)) # update time 
					fast_activity = False
					data_for_print = True
				else: data_for_print = False # meaning we ignore the data stream as it's not within time threshold
				

				# Mapping message - when channel is active and we must send message to the serial port
				if(fast_activity):
					if(prev_row_active_channel < 2): # channel 0-1, i.e. FP1, FP2
						serial_port_new_msg = CHAIR_FORWARD # fast blink
					elif(prev_row_active_channel < 4): # channel 2-3, i.e. T3, T4
						serial_port_new_msg = CHAIR_STOP # fast clench
						isChairStarted = False 
						# prev_row_active_channel = -1 # reset
				elif(data_for_print & prev_row_active_channel > -1): # so no fast blink/clench, hence print previous stream's data and make current stream previous
					if(prev_row_active_channel < 2): 
						serial_port_new_msg = CHAIR_LEFT # single blink
						prev_row_active_channel = x
					elif(prev_row_active_channel < 4):
						serial_port_new_msg = CHAIR_BACKWARD # single clench
						prev_row_active_channel = x
				else: 
					prev_row_active_channel = -1

				if (data_for_print): # Write to the Serial Port - Arduino connected on this serial port will read the message
					print ('sending data to the serial port' , serial_port_new_msg)
					ser.write(serial_port_new_msg)
					break # break out of the 'for loop' as activity already detected - read next stream of data
