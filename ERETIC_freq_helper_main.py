#!/usr/bin/python3

'''
Eric Baetscher
OHSU AIRC
ERETIC project

20180716

utility to simplify picking ERETIC frequencies MRI 
'''

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

now_s_format = datetime.now().strftime('%Y%m%d_%H%M%S')

###--- SETUP ---###
freq_increase_to_fig_left = True
save_figures = True

use_common_Larmor = True
common_Larmor = 123258000

use_common_mm_offset = False
common_mm_offset = 40

#sequence specific parameters:
gre_3d_toggle = True
gre_3d_params = dict(fov_mm = 128,
					 read_offset_mm = 40,
					 hz_per_pix = 420,
					 base_res = 256,
					 MRI_Larmor = 123257000)

q_t2_toggle = True
q_t2_params = dict(fov_mm = 144,
				   read_offset_mm = 40,
				   hz_per_pix = 450,
				   base_res = 144,
				   MRI_Larmor = 123257000)


dixon_8pt_toggle = True
dixon_8pt_params = dict(fov_mm = 192,
						read_offset_mm = 40,
						hz_per_pix = 450,
						base_res = 384,
						MRI_Larmor = 123257000)

#~ spect_params


def gen_fov_bounding_freq(fov_mm, read_offset_mm, hz_per_pix, base_res, MRI_Larmor):
	'''
	function does basic arithmetic to output the minimum, maximum and 
	center frequencies of an MRI field-of-view given the FOV in mm,
	the bandwidth in Hz/pixel (proportional to gradient strength),
	the offset of the center of the FOV in mm, and the resolution in pixels
	'''
	
	freq_uncor_rng = (hz_per_pix * base_res)
	hz_per_mm =  (freq_uncor_rng / fov_mm)
	fov_centr_freq = (read_offset_mm * hz_per_mm)
	min_freq = ((fov_centr_freq + MRI_Larmor) - (0.5 * freq_uncor_rng))
	max_freq = ((fov_centr_freq + MRI_Larmor) + (0.5 * freq_uncor_rng))
	print("minimum frequency at edge of FOV:")
	print(min_freq)
	print(' ')
	print("maximum frequency at opposite edge of FOV:")
	print(max_freq)
	
	return(fov_centr_freq, freq_uncor_rng, min_freq, max_freq)

def plot_freq_schematic(fov_centr_freq,
						base_res,
						freq_uncor_rng,
						MRI_Larmor,
						min_freq,
						max_freq,
						title = 'unnamed'):
	fov_abs_cntr_freq = (fov_centr_freq + MRI_Larmor)
	
	fig_01 = plt.figure(str(title))
	
	ax = fig_01.add_subplot(111)
	ax2 = ax.twiny()
	
	fig_01.suptitle(title, fontsize=14, y = 0.72)
	
	x_pixels = np.linspace(0, base_res, (base_res - 1))
	n_pix_ones = np.ones(base_res)
	
	ax.plot(n_pix_ones)
	ax.set_xlim(0, base_res)
	ax.set_ylim(0, base_res)
	
	xdata, ydata = (base_res / 2), fov_abs_cntr_freq
	offset = 30
	
	bbox = dict(boxstyle="round", fc="0.8")
	props = {'ha': 'center', 'va': 'center', 'bbox': bbox}
	
	arrowprops = dict(
    arrowstyle = "->",
    connectionstyle = "angle,angleA=0,angleB=90,rad=10")
	ax.annotate('Center: \n pixel number, frequency offset \n (%.1f, %.1f Hz)'%(xdata, ydata),
				(xdata, 0), xytext=(-2*offset, offset), textcoords='offset points',
				bbox=bbox, arrowprops=arrowprops)
	
	ax.text((base_res / 2), (base_res * 0.8), ('MRI 1H 0-grad Larmor: ' +
												str(MRI_Larmor)), props, rotation=0)
	
	rec_eretic_freq = (max_freq - (freq_uncor_rng * 0.05))
	ax.text((base_res / 5), (base_res * 0.4), ('recommended \n ERETIC frequency: \n' +
											   str(rec_eretic_freq)), props, rotation=0, fontsize=15)
	
	ax2_tick_list = np.linspace(min_freq, max_freq, 11)
	
	ax2.set_xlim(min_freq, max_freq)
	ax2.set_xticks(ax2_tick_list)
	ax2.plot(n_pix_ones)
	ax2.autoscale_view()

	if freq_increase_to_fig_left == True:
		ax2.invert_xaxis()
	else:
		pass

	ax2.set_xlabel(r"frequency (Hz)")
	ax.set_xlabel(r"Pixel count")
	ax2.ticklabel_format(style = 'plain', useOffset = False)
	ax2.tick_params(labelsize = 12, direction = 'in')
	plt.xticks(rotation=60)
	
	rec_eretic_pos = (base_res * 0.05)
	ax.vlines(rec_eretic_pos, 0, base_res, colors=u'g', linestyles=u'dashed')
	
	#print(ax2_tick_list)
	plt.tight_layout(h_pad=2.2)
	plt.draw()
	
	if save_figures == True:
		fig_save_name = (str(title) + ".png")
		fig_01.savefig(title)
		return
	else:
		return
		

def unpack_params_and_run(scan_title, scan_toggle, scan_param_dict):
	if scan_toggle == False:
		print(str(scan_title) + " toggled off, ERETIC helper not run")
		return
	
	elif scan_toggle == True:
		
		fov_mm = scan_param_dict['fov_mm']
		read_offset_mm = scan_param_dict['read_offset_mm']
		hz_per_pix = scan_param_dict['hz_per_pix']
		base_res = scan_param_dict['base_res']
		MRI_Larmor = scan_param_dict['MRI_Larmor']
		
		if use_common_Larmor == True:
			MRI_Larmor = common_Larmor
		else:
			pass
			
		if use_common_mm_offset == True:
			read_offset_mm = common_mm_offset
		else:
			pass
		
		fov_centr_freq, freq_uncor_rng, min_freq, max_freq = gen_fov_bounding_freq(fov_mm, 
																				   read_offset_mm,
																				   hz_per_pix,
																				   base_res,
																				   MRI_Larmor)
		plot_freq_schematic(fov_centr_freq,
							base_res,
							freq_uncor_rng,
							MRI_Larmor,
							min_freq,
							max_freq,
							title = (str(scan_title) + "_" + str(now_s_format)))
	
																			   
																			   
	else:
		print("scan_toggle must be boolean, skipping " + str(scan_title))
		return

##--Main--##
if __name__ == "__main__":
	unpack_params_and_run('3D_GRE', gre_3d_toggle, gre_3d_params)
	unpack_params_and_run('MRI_SE_qT2', q_t2_toggle, q_t2_params)
	unpack_params_and_run('8-Point_Dixon', dixon_8pt_toggle, dixon_8pt_params)
	plt.show()
