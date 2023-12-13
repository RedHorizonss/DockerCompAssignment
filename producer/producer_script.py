from infofile import infos, samples

def get_data_from_files():
    prefix_val_list = [] # define empty list to hold data
    for s in samples: # loop over samples
        for val in samples[s]['list']:
            if s == 'data':
                prefix = "Data/" # Data prefix
            else: # MC prefix
                prefix = "MC/mc_"+str(infos[val]["DSID"])+"."
            
            prefix_val_list.append(prefix+" "+str(val)) # append prefix and value to list
            
    return prefix_val_list # return dictionary of awkward arrays
