# sgram() -- pretty good looking speech spectrograms

Classic spectrograms in a python function call.

function sgram() is defined in sgram.py,
and is included in the jupyter notebook - using_sgram.ipynb

Using functions defined in the scipy.signal library and the matplotlib.pyplot library, sgram() produces a spectrogram plot from a wav audio file. It is optimized to produce speech spectrograms that closely resemble the 'classic' spectrograms produced by the Kay Elemetrics analog spectrograph. In particular, two analysis bandwidths are predefined, and the spectrogram is calibrated to use 6" per second for chunks under 1.7 seconds long. A spectral "slice" can also requested and printed after the spectrogram on the same frequency scale.

    filename -- name of a wav file to plot
    chan -- for dealing with stereo files, 0 (default) = left channel, 1 = right channel
    start, end -- times (in seconds) of the waveform chunk to plot -- default plot the whole file
    tf -- the top frequency to show in the spectrogram -- default is 8000Hz
    band -- 'wb' (default) wideband (300Hz effective filter bandwidth), 'nb' narrow band (45Hz filter)
    save_name -- name of a file to save figure with pyplot.savefig() -- default no name.
    slice_time -- location of an optional spectral slice. -- default = -1 (no slice)
    cmap -- name of a matplotlib colormap for the spectrogram -- default = Greys

The function returns the frequency scale (frequency of each point in the spectrum), the time scale (time values of each spectrum), and the spectral amplitudes at those times and frequencies.

    f -- a one dimensional array of frequency values (in Hz)
    ts -- a one dimensional array of time values (in seconds, should be one per millisecond)
    Sxx -- a two dimensional array of amplitude values (dB scaled)

<img src="https://user-images.githubusercontent.com/7074947/207211367-5e7713b2-594d-43e1-9719-6ae69248e878.png" width="364">

