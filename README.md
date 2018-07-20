# ERETIC freq helper
MRI frequency charting given FOV-mm, Larmor-Hz, FOV-offset, Hz/px, resolution.

One dimension of a 2D MRI slice (or 3D MRI volume) is typically the "readout" or "frequency-encoding" direction. If the readout direction in the image is left-to-right (or right-to-left) then each column in the image corresponds to a unique range of frequencies (assuming no aliasing for out of the FOV).

ERETIC (Electronic REference To access In-vivo Concentrations) is a technique that employs an additional synthetic radio frequency signal, inductively coupled to the MRI reciever coil to allow calibration of recieved magnetic resonance signals and subsequent absolute quantification of tissue composition.

Among the simplest implemetations of the ERETIC methods is to transmit a pure tone without regard to phase syncronization between the MRI system and the ERETIC frequency synthesis system. This corresponds to a column in the image, and some spin-echo sequences may have pseudo phase-sync between ERETIC and MRI system.

By default, the ERETIC freq helper script calculates and reports the frequency from a column 5% of the FOV from the left side of the frame, assuming frequency is increasing to the left. There is a toggle if the frequency is increasing in the opposite direction. 
