import scipy.io.wavfile as wavfile
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt

def sgram(filename,chan=0,start=0,end=-1,tf=8000,band='wb',save_name='',slice_time=-1,cmap='Greys'):
    # filename -- name of a wav file to plot
    # chan -- for dealing with stereo files, 0 (default) = left channel, 1 = right channel
    # start, end -- times (in seconds) of the waveform chunk to plot -- default plot whole file
    # tf -- the top frequency to show in the spectrogram -- default is 8000Hz
    # band -- 'wb' (default) wideband (300Hz effective filter bandwidth), 'nb' narrow band (45Hz filter)
    # save_name -- name of a file to save results with pyplot.savefig() -- default no name.
    # slice_time -- location of an optional spectral slice.  -- default = -1 (no slice)
    # cmap -- name of a matplotlib colormap for the spectrogram -- default = Greys
    
    sf = tf*2    # top frequency is the Nyquist frequency for the analysis
    nb = 0.04    # analysis window size for narrow band spectrogram (sec)
    wb = 0.008   # analysis window size for wide band spectrogram
    step = 0.001  # step size between spectral slices (sec)
    order = 13    # FFT size = 2 ^ order
    preemph = 0.94
    
    if band=='nb':
        w = nb
    else:
        w = wb
     
    # set up parameters for the spectrogram window
    figheight = 4.5
    max_figwidth = 12 # maximum figure width in inches
    inches_per_sec = 6.5 # desired width scaling of printed spectrogram
    slice_width = 1.5  # how much space to give to the spectral slice
    cmap = plt.get_cmap(cmap)

    # set up parameters for signal.spectrogram()
    noverlap = int((w-step)*sf) # skip forward by step between each frame
    nperseg = int(w*sf)         # number of samples per waveform window
    nfft = np.power(2,order)    # number of points in the fft
    scaling = 'spectrum'        # see signal.spectrogram documentation
    mode = 'magnitude'
    window = signal.blackmanharris(nperseg)
    
    # ----------- read and condition waveform -----------------------
    orig_sf, raw = wavfile.read(filename)
    
    if raw.ndim == 2:  # if this is a stereo file, use one of the channels
        print(f'Stereo file, using channel {chan}')
        raw = raw[:,chan]
    
    if (orig_sf == sf):  # resample to 'sf' samples per second
        x = raw
    else:
        print(f'Resampling from {orig_sf} to {sf}')
        resample_ratio = sf/orig_sf
        new_size = int(len(raw) * resample_ratio)  # how many samples in downsampled version?
        x = signal.resample(raw,new_size)  # now sampled at desired sampling freq
            
    i1 = int(start * sf)   # index of starting time: seconds to samples
    i2 = int(end * sf)     # index of ending time
    if i2<0 or i2>len(x):  # stop at the end of the waveform
        i2 = len(x)
    if i1>i2:              # don't let start follow end
        i1=0
    
    x2 = np.append(x[0], x[1:] - preemph * x[:-1])  # apply pre-emphasis
    x2 = np.rint(31000 * (x2[i1:i2]/max(x2[i1:i2]))).astype(np.int16)  # scale the signal chunk

    # ----------- compute the spectrogram ---------------------------------
    f,ts,Sxx = signal.spectrogram(x2,fs=sf,noverlap = noverlap, window=window, nperseg = nperseg, 
                              nfft = nfft, scaling=scaling, mode = mode, detrend = 'linear')
    Sxx = 20 * np.log10(Sxx+1)  # put spectrum on decibel scale
    
    # ------------ display in a matplotlib figure --------------------
    ts = np.add(ts,start)  # increment the spectrogram time by the start value
    dur = max(ts)-min(ts) + w   # scale figure size
    figwidth = np.min([(dur * inches_per_sec), max_figwidth])
  
    if slice_time>0: # if spectral slice is desired, add an axes for it
        fig = plt.figure(figsize=(figwidth+slice_width, figheight),dpi=72)
        gs = fig.add_gridspec(nrows=1, ncols=2, width_ratios=[figwidth/slice_width, 1])
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
    else:
        fig = plt.figure(figsize=(figwidth, figheight),dpi=72)
        ax1 = fig.add_subplot(111)

    extent = (min(ts),max(ts),min(f),max(f))  # get the time and frequency values for indices.

    im = ax1.imshow(Sxx, aspect='auto', interpolation='nearest', cmap=cmap, vmin = 25, 
                extent = extent, origin='lower')
    ax1.grid(which='major', axis='y', linestyle=':')  # add grid lines
    ax1.set(xlabel="Time (sec)", ylabel="Frequency (Hz)")
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
   
    if slice_time > 0:  # if spectral slice is desired, plot the spectrum
        i = np.argmin(np.abs(ts-slice_time))  # find the index of the spectral slice
        ax1.axvline(x=slice_time,color='black',linestyle="--")
        spectrum = Sxx.T[i]  
        ax2.plot(spectrum,f,color='black') 
        ax2.grid(which='major', axis='y', linestyle=':')  # add grid lines
        ax2.set_ymargin(0)    # put y-axis at bottom and top of axis (as in spectrogram)
        ax2.tick_params(labelleft=False)  # do not write the frequency axis labels
    
    
    if len(save_name)>0:
        print(f'Saving file: {save_name}')
        plt.savefig(save_name,dpi=300,bbox_inches='tight')
        
    return (f,ts,Sxx)

# ------- toy with finding first two peaks ---------------
# find the first peak in the spectrum starting at "startfreq"
# report the amplitude and the frequency of the peak
def Spectral_peak(x,startfreq,sf,npoints):
    df = sf/npoints     # step size on the frequency scale
    start = int(startfreq/df)
    for i in range(start,len(x)):
        if ((x[i-1]<x[i]) & (x[i+1]<x[i])):
            break  # stop after finding a peak
    return x[i],i*df
