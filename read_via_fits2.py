import pandas as pd
from astropy.table import Table

def read_fits_as_dataframe(filename, index_columns=None):
    # This is the way to read the FITS data into a numpy structured array
    # (using astropy.io.fits.getdata didn't work out of the box
    # because it gives a FITSRec)
    table = Table.read(filename)
    # Fix byte order.
    # See https://github.com/astropy/astropy/issues/1156
    data  = {}
    for key in table.keys():
        if np.ndim(table.as_array()[key]) == 2:
            for k in range(table.as_array()[key].shape[1]):
                data[key + '_' + str(k)] = table.as_array()[key][:,k].byteswap().newbyteorder()
        else:
            data[key] = table.as_array()[key].byteswap().newbyteorder()
    
    df    = pd.DataFrame.from_records(data)
    if index_columns is not None:
        # Strip whitespace for string columns that will become indices
        for index_column in index_columns:
            df[index_column]  = df[index_column].map(str.strip)
        df  = df.set_index(index_columns)
    return df

df = read_fits_as_dataframe('table.fits', ['ROI', 'Solution'])
print(df.head())
print(df.xs('HESS_J1023m575'))
print(df[['nfev', 'statname']])
