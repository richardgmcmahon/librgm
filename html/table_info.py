from __future__ import division, print_function

import sys

import numpy as np

def table_info(table, col_list,
               type_v = "AB",
               modelcols_seperate = False,
               debug=False, verbose=False):
    """

    forked from Fernanda Ostrovski's version of table_info which is forked from
    Sophie Reed's version.

    work in progress by rgm

    Inputs:
        table: Astropy table
        col_list: column name list
        type_v: AB to convert Vega mag to AB; should deprecate
        modelcols_seperate:

    It formats the floats

    returns list of string lists.

    Returns:
        vals_list
        header_list
        column header names with some mangling.

    """
    t = table

    print('type(table):', type(table))
    print('type(col_list):', type(col_list))
    print('Number of rows:', len(t))
    print('Number of columns:', len(col_list))
    print('col_list')
    for icol, col in enumerate(col_list):
        print(icol, col)
    print()

    print('table.colnames')
    for icol, colname in enumerate(table.colnames):
        print(icol, colname, len(table[colname]), table[colname].dtype)
        try:
            print('Range:', np.min(table[colname]), np.max(table[colname]))
            print('Range:', np.nanmin(table[colname]),
                  np.nanmax(table[colname]))
            itest_nan = np.isnan(table[colname])
            itest_notnan = np.isfinite(table[colname])
            print('Number of NaNs:', len(table[colname][itest_nan]))
            print('Number of finite values:', len(table[colname][itest_notnan]))
            print()
        except:
            # deal with the string arrays
            # http://stackoverflow.com/questions/12654093/arrays-of-strings-into-numpy-amax
            print('Non-numeric column')
            print('Range:', np.min(np.array(table[colname], dtype=object)),
                  np.max(np.array(table[colname], dtype=object)))
            pass


        # print(table[icol].info)
        # print(table.info[icol])
    print()

    # iterate over columns
    # Using itercols() is similar to for col in t.columns.values() but
    # is syntactically preferred.
    for col in table.itercols():
        print('col.dtype:', col.dtype)
        print('len(col):', len(col))

    for icol, col in enumerate(col_list):
        p = col_list.index(col)
        print('colname column index:', p)
        if p < 0:
            print('Error: colname inconsistency: Exiting')
            sys.exit()

    key=raw_input("Enter any key to continue: ")

    vals_list = []

    debug = False
    for n, row in enumerate(t):
        if debug:
            print(n, row)

        val_list = []
        header_list = []
        spreads = ""
        diffs = ""

        for icol, col in enumerate(col_list):

            if debug:
                print(n, col, table.colnames[icol])
                print(table[col][n])

            p = col_list.index(col)

            if col in ["TILENAME", "COADD_OBJECTS_ID", "RADEC_STRING",
                       "RUN", "Jname", "Bname", "NED",
                       "SDSS_DR12", "PS1_DR1", "IRSA", "WISE"]:
                val_list.append(table[col][n])
                if col == "COADD_OBJECTS_ID":
                    col = "CO_ID"
                header_list.append(col)

            elif "LENSID" in col:
                val_list.append(table[col][n])
                header_list.append(col)

            elif "CO_ID" in col:
                val_list.append(table[col][n])
                header_list.append(col)
            elif "-" in col:
                if "MODEL" not in col:
                    colours = col.split("-")
                    ch = []
                    for cs in colours:
                        for c in cs.split(" "):
                            if len(c) > 0:
                                ch.append(c)
                    if "PSF" in ch[0]:
                        ch1 = "M" + ch[0][4:]
                    else:
                        ch1 = ch[0]
                    if "PSF" in ch[1]:
                        ch2 = "M" + ch[1][4:]
                    else:
                        ch2 = ch[1]

                    col = ch1 + "- " + ch2
                    header_list.append(col)
                    val1 = table[ch[0]][n]
                    val2 = table[ch[1]][n]
                    #if type_v == "AB":
                    #    if ch1 == "J":
                    #        val1 += 0.937
                    #    elif ch1 == "K":
                    #        val1 += 1.839
                    #    if ch2 == "J":
                    #        val2 += 0.937
                    #    elif ch2 == "K":
                    #        val2 += 1.839

                    if ch2 == "J":
                        print(val1-val2)
                    val_list.append("%0.2f" % (val1 - val2))

                elif "MODEL" in col:
                    colours = col.split("-")
                    ch = []
                    for cs in colours:
                        for c in cs.split(" "):
                            if len(c) > 0:
                                ch.append(c)
                    band = ch[0][-1]
                    if modelcols_seperate == False:
                        diffs += band + ": " + "%0.2f" % \
                            (table[ch[0]][n] - table[ch[1]][n]) + " "
                    else:
                        header_list.append(col)
                        val_list.append("%0.2f" % \
                             (table[ch[0]][n] - table[ch[1]][n]))

            elif "SPREAD" in col:
                band = col[-1]
                spreads += band + ": " + "%0.2f" % table[col][n] + " "

            elif "RA" in col or "DEC" in col or "ALPHA" in col or "DELTA" in col or 'Dec' in col:
                val_list.append("%0.5f" % table[col][n])
                if "ALPHA" in col or "DELTA" in col:
                    col = col[0] + col[8:]
                header_list.append(col)

            elif (("MAG" in col and "MODEL" not in col and "-" not in col) or ("W" in col and "-" not in col) or ("J" in col and "-" not in col and "OB" not in col) or ("H" in col and "-" not in col) or ("K" in col and "-" not in col) or ('U' in col and 'MAG' not in col and "NUV" not in col) or ('G' in col and 'MAG' not in col) or ('R' in col and 'MAG' not in col) or ('I' in col and 'MAG' not in col) or ('Z' in col and 'MAG' not in col)) and "ERR" not in col and "FLAG" not in col and "WIN" not in col and "IMAGE" not in col:

                if "PSF" in col:
                    band = col[-1]
                    if "MAGERR_PSF_" + band in col_list:
                        e = table["MAGERR_PSF_" + band][n]
                        val_list.append("%0.2f" % table[col][n] + " +/- " + "%0.4f" % e)
                    else:
                        val_list.append("%0.2f" % table[col][n])

                    col = "M" + col[4:]

                elif "AUTO" in col:
                    band = col[-1]
                    if "MAGERR_AUTO_" + band in col_list:
                        e = table["MAGERR_AUTO_" + band][n]
                        val_list.append("%0.2f" % table[col][n] + " +/- " + "%0.4f" % e)
                    else:
                        val_list.append("%0.2f" % table[col][n])
                    col = "M" + col[4:]

                elif ("W" in col or "J" in col or 'H' in col or "K" in col or "NUV" in col or "APERCOR5" in col) and 'ERR' not in col and "FLAG" not in col:
                    val = table[col][n]
                    #if type_v == "AB" and col == "J":
                    #    val += 0.937
                    #if type_v == "AB" and col == "K":
                    #    val += 1.839

                    if col + "_ERR" in col_list or col + "_MAGERR" in col_list:
                        e = table[col + "_ERR"][n]
                        val_list.append("%0.2f" % val + " +/- " + "%0.4f" % e)

                    #elif "ERR" not in col:
                    else:
                        val_list.append("%0.2f" % table[col][n])
                elif ("ELLIP" in col):
                    val_list.append("%0.2f" % table[col][n])

                else:
                    band = col[-1]
                    if "MAGERR_" + band in col_list:
                        e = table["MAGERR_" + band][n]
                        val_list.append("%0.2f" % tband[col][n] +
                                        " +/- " + "%0.4f" % e)
                    elif band + "_ERR" in col_list:
                            e = t[band + "_ERR"][n]
                            val_list.append("%0.2f" % t[col][n] + " +/- "
                                            + "%0.4f" % e)
                    else:
                        val_list.append("%0.2f" % t[col][n])
                #print col
                header_list.append(col)

            elif "MAG" in col and "MODEL" in col and "ERR" not in col:
                band = col[-1]
                if "MAGERR_MODEL_" + band in col_list:
                                        e = t["MAGERR_MODEL_" + band][n]
                                        val_list.append(("%0.2f" % t[col][n] + " +/- %0.4f" % e))
                else:
                                        val_list.append(("%0.2f" % t[col][n]))
                #print col
                header_list.append(col)

            elif "fiberMag" in col and "Err" not in col:
                band = col[-1]
                if "fiberMagErr_" + band in col_list:
                                        e = t["fiberMagErr_" + band][n]
                                        val_list.append(("%0.2f" % t[col][n] + " +/- %0.4f" % e))
                else:
                                        val_list.append(("%0.2f" % t[col][n]))
                #print col
                header_list.append(col)


            elif "FLAG" in col or "Cl" in col or 'source' in col or "class" in col and 'ERR' not in col:
                #print col
                                header_list.append(col)
                                val_list.append(str(table[col][n]))

            elif "ERR" not in col and "FLAG" not in col and "ID" not in col and "Cl" not in col:
                header_list.append(col)
                val_list.append("%0.2f" % table[col][n])

            elif "WIN" in col or "IMAGE" in col:
                val_list.append("%0.2f" % table[col][n])
                header_list.append(col)

        if spreads <> "":
            val_list.append(spreads)
            header_list.append("Spread Models")

        if diffs <> "":
            val_list.append(diffs)
            header_list.append("PSF - Models")

        vals_list.append(val_list)

    #print header_list
    return vals_list, header_list
