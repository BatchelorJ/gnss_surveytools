import os
import sys
import csv
import geodepy.transform as gt


def dynaxyz2csv(dynaxyz_file, filetype):
    """
    Converts DynAdjust *.xyz file to csv with header info
    :param dynaxyz_file: DynAdjust v1.0 *.xyz
    :param filetype: type of file, string
    :return: None (writes new *.csv file with info from *.xyz file)
    """
    # Define output file name
    dynaxyz_fname, ext = os.path.splitext(dynaxyz_file)
    dynacsv_file = dynaxyz_fname + filetype

    # Open *.xyz file, remove spaces
    with open(dynaxyz_file) as file:
        lines = file.readlines()
        for num, line in enumerate(lines):

            # Remove any existing commas
            line_nocommas = line.replace(', ', '')

            # Remove spaces, replace with commas
            csv_line = ','.join(line_nocommas.split())
            lines[num] = csv_line + '\n'

        # Select only header and points info lines
        points_and_header = [lines[18]] + lines[20:]

    # Write csv data to new file
    with open(dynacsv_file, 'w+') as file:
        file.writelines(line for line in points_and_header)


def dynacsv_mga_transform(dynacsv_file, mga_transform_func):
    """
    Converts file with MGA coordinates to another MGA, using GeodePy function
    :param dynacsv_file: *.csv file (tested with output file from dynaxyz2csv
    :param mga_transform_func: geodepy.transform mga transformation function
    :return: None (writes new *.csv file with tranformed info from input file)
    """
    # Read *.csv Data into Function
    with open(dynacsv_file) as file:
        csv_data_gda2020 = list(csv.reader(file))
    header = csv_data_gda2020[0]

    # Read Position of Different Columns from Header
    try:
        stn_index = header.index('Station')
        nth_index = header.index('Northing')
        est_index = header.index('Easting')
        zn_index = header.index('Zone')
    except ValueError:
        raise ValueError('Station, Northing, Easting and/or '
                         'Zone not found in header')

    # Convert grid values from mga2020 to mga1994
    csv_data_mga1994 = []
    for stn in csv_data_gda2020[1:-1]:
        stn_name = stn[stn_index]
        stn_zn = float(stn[zn_index])
        stn_nth = float(stn[nth_index])
        stn_est = float(stn[est_index])
        (stn_zn94,
         stn_est94,
         stn_nth94,
         stn_ellht) = mga_transform_func(stn_zn,
                                         stn_est,
                                         stn_nth,)
        csv_data_mga1994.append([stn_name, stn_zn94, stn_est94, stn_nth94])

    # Define output file name
    dynacsv_fn, ext = os.path.splitext(dynacsv_file)
    dyna_mga94_file = dynacsv_fn + '_' + mga_transform_func.__name__ + ext

    # Write new csv file with converted mga1994 data
    with open(dyna_mga94_file, 'w+', newline='') as file:
        csv.writer(file).writerows(csv_data_mga1994)


if __name__ == "__main__":
    input_file = sys.argv[1]
    dynaxyz_fn, extention = os.path.splitext(input_file)
    csv_file = dynaxyz_fn + '.csv'
    dynaxyz2csv(input_file)
    dynacsv_mga_transform(csv_file, gt.mga2020_to_mga94)
