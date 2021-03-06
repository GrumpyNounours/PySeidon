#!/usr/bin/python2.7
# encoding: utf-8
import pandas as pd
# Custom error
from pyseidon.utilities.pyseidon_error import PyseidonError

# ALTERNATE VERSION FOR ANDY

def valTable(struct, filename, vars, save_csv=False, debug=False, debug_plot=False):
    '''
    Takes validation data from the struct and saves it into a .csv file .

    Takes a single argument, a dictionary
    '''
    # initialize  lists
    kind, name, ovORun, RMSE, CF, SD, POF, NOF, MDPO, MDNO, skill, r2, phase = \
    [], [], [], [], [], [], [], [], [], [], [], [], []
    bias, pbias, NRMSE, NSE, corr, SI, gear = [], [], [], [], [], [], []

    # append to the lists the stats from each site for each variable
    for var in vars:
        (kind, name, ovORun, RMSE, CF, SD, POF, NOF, MDPO, MDNO, skill, r2, phase, bias, pbias, NRMSE, NSE, corr, SI, gear) \
            = siteStats(struct, var, kind, name, ovORun, RMSE, CF, SD, POF, NOF, MDPO, MDNO, skill, r2, phase,
                        bias, pbias, NRMSE, NSE, corr, SI, gear, debug=False, debug_plot=False)

    # put stats into dict and create dataframe
    val_dict = {'Type':kind, 'ovORun':ovORun, 'RMSE':RMSE, 'CF':CF, 'SD':SD, 'POF':POF,
                'NOF':NOF, 'MDPO':MDPO, 'MDNO':MDNO,  'skill':skill, 'r2':r2, 'phase':phase,
                'bias':bias, 'pbias':pbias,'NRMSE':NRMSE, 'NSE':NSE, 'corr':corr, 'SI':SI, 'gear':gear}

    table = pd.DataFrame(data=val_dict, index=name, columns=val_dict.keys())

    # export as .csv file
    if save_csv:
        out_file = '{}_val.csv'.format(filename)
        table.to_csv(out_file)
    return table

def siteStats(site, variable, type, name, ovORun, RMSE, CF, SD, POF, NOF, MDPO, MDNO, skill, r2, phase,
              bias, pbias, NRMSE, NSE, corr, SI, gear, debug=False, debug_plot=False):
    """
    Takes in the run (an array of dictionaries) and the type of the run (a
    string). Also takes in the list representing each statistic.
    """
    if debug: print "siteStats..."
    # check if it's a tidegauge site
    if ((site['type'] != 'TideGauge') and (variable != 'tg')):
        stats = site['{}_val'.format(variable)]
        type.append(variable)
        name.append(site['name'].split('/')[-1].split('.')[0])

    elif ((site['type'] == 'TideGauge') and (variable == 'tg')):
        stats = site['tg_val']
        type.append('elev')
        name.append(site['name'].split('/')[-1].split('.')[0])

    # do nothing if a tidegauge is encountered but variable isn't tg
    else:
        raise PyseidonError("---The variable tg is missing---")
   
    # add the statistics to the list, round to 2 decimal places
    ovORun.append(stats['ovORun'])
    RMSE.append(round(stats['RMSE'], 2))
    CF.append(round(stats['CF'], 2))
    SD.append(round(stats['SD'], 2))
    POF.append(round(stats['POF'], 2))
    NOF.append(round(stats['NOF'], 2))
    MDPO.append(stats['MDPO'])
    MDNO.append(stats['MDNO'])
    skill.append(round(stats['skill'], 2))
    r2.append(round(stats['r_squared'], 2))
    phase.append(stats['phase'])
    bias.append(round(stats['bias'], 2))
    pbias.append(round(stats['pbias'], 2))
    NRMSE.append(round(stats['NRMSE'], 2))
    NSE.append(round(stats['NSE'], 2))
    corr.append(round(stats['CORR'], 2))
    SI.append(round(stats['SI'], 2))
    gear.append(site['type'])
    if debug: print "...siteStats done."

    return (type, name, ovORun, RMSE, CF, SD, POF, NOF, MDPO, MDNO, skill, r2, phase, bias, pbias, NRMSE, NSE, corr, SI, gear)
