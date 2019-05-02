
import numpy as np
import math
import matplotlib.pyplot as plt
import json


def main():
	with open('sandpile_stats.txt', 'r') as f:
		data = json.load(f)
	# separate lists
	grain_vals = np.asarray([int(k) for k in data.keys()])
	diam_vals = np.asarray([v['diameter'] for k, v in data.items()])
	time_vals = np.asarray([round(v['time'], 4) for k, v in data.items()])
	
	log_grain_vals = np.log(grain_vals)
	log_diam_vals = np.log(diam_vals)
	log_time_vals = np.log(time_vals)
	
	# calculate linear regression
	fit_diam = np.polyfit(log_grain_vals, log_diam_vals, 1)
	fit_time = np.polyfit(log_grain_vals, log_time_vals, 1)
	# create functions that predict values
	diam_fn = np.poly1d(fit_diam)
	time_fn = np.poly1d(fit_time)
	
	
	plt.figure(1)
	
	plt.subplot(221)
	plt.plot(grain_vals, diam_vals, 'b.')
	plt.xlabel('Grains')
	plt.ylabel('Diameter')
	plt.grid(True)
	
	plt.subplot(222)
	plt.plot(grain_vals, time_vals, 'r.')
	plt.xlabel('Grains')
	plt.ylabel('Time (sec)')
	plt.grid(True)
	
	plt.subplot(223)
	plt.plot(log_grain_vals, log_diam_vals, 'b.', log_grain_vals, diam_fn(log_grain_vals), 'k-')
	plt.xlabel('Log(Grains)')
	plt.ylabel('Log(Diameter)')
	plt.grid(True)
	
	plt.subplot(224)
	plt.plot(log_grain_vals, log_time_vals, 'r.', log_grain_vals, time_fn(log_grain_vals), 'k-')
	plt.xlabel('Log(Grains)')
	plt.ylabel('Log(Time) (sec)')
	plt.grid(True)
		
	plt.show()
	

if __name__ == '__main__': main()
