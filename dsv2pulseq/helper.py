"""
Helper functions
"""

import numpy as np
from pypulseq.Sequence.sequence import Sequence
from pypulseq.make_delay import make_delay

def waveform_from_seqblock(seq_block, system):
    """
    extracts gradient waveform from Pypulseq sequence block.
    Generate a sequence of magnitudes sampled at every gradient raster time.
    
    """
    assert seq_block.channel in ['x', 'y', 'z'], 'No valid gradient waveform'
    dummy_seq = Sequence() # helper dummy sequence
    dummy_seq.add_block(make_delay(d=1e-3)) # dummy delay to allow gradients starting at a nonzero value
    dummy_seq.add_block(seq_block)
    grad = 'g'+seq_block.channel
    grad_amp = dummy_seq.waveforms_export()[grad]*1e3 # units in kHz
    t = dummy_seq.waveforms_export()['t_'+grad]
    t_sampled = np.arange(t[0], t[-1]+system.grad_raster_time, system.grad_raster_time)
    return np.interp(t_sampled, t, grad_amp)

def round_up_to_raster(number, decimals=0):
    """
    round number up to a specific number of decimal places.
    """
    multiplier = 10 ** decimals
    return np.ceil(number * multiplier) / multiplier