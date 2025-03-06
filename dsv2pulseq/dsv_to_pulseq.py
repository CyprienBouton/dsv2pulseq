#!/usr/bin/env python

import argparse
import os
from dsv2pulseq.read_dsv import read_dsv

defaults = {'out_file': 'external.seq',
            'ref_volt': 223.529007,
            'lead_time': 100,
            'hold_time': 30,
            'indep_Tx': False,
            'elliptical_Tx': True}

def main(args):

    # check input
    sfx = ['_INF', '_GRX', '_GRY', '_GRZ', '_RFD', '_RFP']
    for suffix in sfx:
        if not os.path.isfile(args.in_file_prefix + suffix + '.dsv') or not os.path.isfile(args.in_file_prefix + suffix + '.DSV'):
            raise OSError(f"DSV file {args.in_file_prefix + suffix + '.dsv'} does not exist.")

    seq = read_dsv(args.in_file_prefix, args.ref_volt, plot=False)
    seq.set_lead_hold(args.lead_time, args.hold_time)
    seq.write_pulseq(args.out_file)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create Pulseq sequence file from dsv file.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('in_file_prefix', type=str, help="Input dsv file prefix. E.g. 'gre'")
    parser.add_argument('-o', '--out_file', type=str, help='Output Pulseq file.')
    parser.add_argument('-r', '--ref_volt', help='Reference voltage of simulation [V].', type=float)
    parser.add_argument('-b', '--lead_time', help='RF lead time [us] (minimum time between start of event block and beginning of RF).', type=int)
    parser.add_argument('-a', '--hold_time', help='RF hold time [us] (minimum time from end of RF to end of event block).', type=int)
    parser.add_argument('--indep_Tx',  action=argparse.BooleanOptionalAction, help="If there is two independents RF transmitter")
    parser.add_argument('--elliptical_Tx',  action=argparse.BooleanOptionalAction, help="If the RF transmitter is elliptical")
    
    parser.set_defaults(**defaults)
    args = parser.parse_args()

    if args.indep_Tx:
        # 1/sqrt(2) if circular siemens values for RF elliptical Tx
        factor = 0.4457 if args.elliptical_Tx else 1/(2**0.5)
        args.ref_volt *= factor
    main(args)
