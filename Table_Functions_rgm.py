import astropy.io.fits as fits
from astropy.table import Table, Column
import match_lists
import numpy as np
import stats
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import plotid

def coord_convert(t, ra_col, dec_col):
	t[ra_col] = np.rad2deg(t[ra_col])
	t[dec_col] = np.rad2deg(t[dec_col])

	return t


def merge(t, t1, suf1, col_ra, col_dec, col1_ra, col1_dec, radius = 0.0006, join = "inner"):

	old_cols = list(t1.columns)
	new_cols = []
	for col in old_cols:
		new_cols.append(col + "_" + suf1)
		t1.rename_column(col, col + "_" + suf1)

	dists, inds = match_lists.match_lists(t[col_ra], t[col_dec], t1[col1_ra+ "_" + suf1], t1[col1_dec + "_" + suf1], radius)
	ms = np.where( inds <> len(t1) )[0]
	
	if join == "inner":
		t = t[ms]
		t1 = t1[inds[ms]]
		for col in new_cols:
			t[col] = t1[col]
	elif join == "outer":
		ws = np.where( inds == len(t1) )[0]
		tm = t[ms]
		t1m = t1[inds[ms]]
		for col in new_cols:
			tm[col] = t1m[col]
		tw = t[ws]
		for col in t1m.columns:
			tw[col] = [-99.0]*len(tw)
		for row in tw:
			tm.add_row(row)
		n = 0
		ws1 = []
		while n < len(t1):
			if n not in inds[ms]:
				ws1.append(n)
			n += 1
		t1w = t1[ws1]
		for col in t.columns:
			ncol = Column([-99.0]*len(t1w), name = col)
			t1w.add_column(ncol, index = 0)
			#t1w[col] = [-99.0]*len(t1w)
		for row in t1w:
			tm.add_row(row)
		t = tm

	return t

def check_graph(t, RA, DEC, t1, RA1, DEC1, width, nbins=100,gtype = "all",
 suptitle=None):

	#Needs width in arcsecs
	n = 0
	#xs = []
	#ys = []
	xs = (t[RA] - t1[RA1])*np.cos((t[DEC]+t1[DEC])*np.pi/360.0)*3600.0
	ys = (t[DEC] - t1[DEC1])*3600.0
	#while n < len(t):
	#	x = (t[RA][n] - t1[RA1][n])*np.cos((t[DEC][n]+t1[DEC][n])*np.pi/360.0)*3600.0
	#	y = (t[DEC][n] - t1[DEC1][n])*3600.0

	#	if not np.isnan(x) and not np.isnan(y):
	#		xs.append(x)
	#		ys.append(y)
	#	n += 1

	print len(xs)
	n = 0
	xs_s = []
	ys_s = []
	if gtype == "square":
		w = width / np.sqrt(2.0)
		while n < len(xs):
			x = xs[n]
			y = ys[n]
			if x <= w and x >= -w and y <= w and y >= -w:
				xs_s.append(xs[n])
				ys_s.append(ys[n])
			n += 1

		xs = xs_s
		ys = ys_s

	xs1 = list(xs) + []
	ys1 = list(ys) + []

	RA_med = np.median(xs1)
	DEC_med = np.median(ys1)
	RA_MAD = stats.MAD(xs1, RA_med)
	DEC_MAD = stats.MAD(ys1, DEC_med)
	print "Number of points", len(xs)
	print "RA offset", RA_med, "DEC offset", DEC_med
	print "RA MAD", RA_MAD, "DEC MAD", DEC_MAD
	print "RA Sigma MAD", 1.486*RA_MAD, "DEC Sigma DEC", 1.486*DEC_MAD
	print "RA Median Error", 1.486*RA_MAD/np.sqrt(len(xs)), "DEC Median Error", 1.486*DEC_MAD/np.sqrt(len(ys))
	gs = gridspec.GridSpec(2,2, width_ratios = [2,1], height_ratios = [1,2])
	fig = plt.figure()
	ax1 = plt.subplot(gs[0])
	ax1.hist(xs, bins = 100, color = "r")
	ax1.set_xlim(-1*width, width)
	ax1.axes.get_xaxis().set_visible(False)
	ax1.set_ylabel("Number")
	
	ax2 = plt.subplot(gs[2])
	#ax2.plot(xs, ys, "k+")
	plt.hist2d(xs, ys, bins = 100, cmap = "binary")
	ax2.set_ylim(-width, width)
	ax2.set_xlim(-width, width)
	ax2.set_xlabel('Delta RA /"')
	ax2.set_ylabel('Delta Dec /"')
	labels1 = ax2.get_xticks()
	ax2.set_xticklabels(labels1, rotation = 270)

	fig.suptitle("Errors in matching")	
        if suptitle != None: 	fig.suptitle('Errors in matching: '+suptitle)

	ax3 = plt.subplot(gs[3]) 
	ax3.hist(ys, bins = 100, orientation = "horizontal", color = "r")
	ax3.set_ylim(-width, width)
	ax3.set_xlabel("Number")
	ax3.axes.get_yaxis().set_visible(False)
	labels2 = ax3.get_xticks()
	ax3.set_xticklabels(labels2, rotation = 270)

	ax4 = plt.subplot(gs[1])
	ax4.annotate("Number of points: " + str(len(xs)), xy = (0.01, 0.1), size = "small")
	ax4.annotate("RA offset: {0:.4f}".format(RA_med) + '"', xy = (0.01,0.90), size = "small")
	ax4.annotate("DEC offset: {0:.4f}".format(DEC_med) + '"', xy = (0.01, 0.8), size = "small")
	ax4.annotate("RA MAD: {0:.4f}".format(RA_MAD) + '"', xy = (0.01, 0.7), size = "small")
	ax4.annotate("DEC MAD: {0:.4f}".format(DEC_MAD) + '"', xy = (0.01, 0.6), size = "small")
	ax4.annotate("RA median error: {0:.4f}".format(1.486*RA_MAD/np.sqrt(len(xs))) + '"', xy = (0.01, 0.5), size = "small")
	ax4.annotate("DEC median error: {0:.4f}".format(1.486*DEC_MAD/np.sqrt(len(ys))) + '"', xy = (0.01, 0.4), size = "small")
	ax4.annotate("RA sigma MAD: {0:.4f}".format(RA_MAD*1.486) + '"', xy = (0.01, 0.3), size = "small")
	ax4.annotate("DEC sigma MAD: {0:.4f}".format(DEC_MAD*1.486) + '"', xy = (0.01, 0.2), size = "small")

	ax4.axes.get_xaxis().set_visible(False)
	ax4.axes.get_yaxis().set_visible(False)

	plt.show()

        label='check_des'
        plotdir='./'
        figname='Muzzin+2013_' + label + '.png'
        print('Saving: '+figname)
        plt.savefig(plotdir+figname)

	return RA_med, DEC_med

def mag_hist(t, col, SG_col = "CLASS_STAR", SG_val = 1):

	stars = np.where( (t[SG_col] == SG_val) )[0]
	ids = np.where( (t[SG_col] == SG_val) & (t[col] > 0.0) & (t[col] < 50))[0]
	print "Number in table:", len(t)
	print "Number not in graph:", len(t) - len(ids)
	print "Number that satisfy classifier:", len(stars)
	print "Number that are junk:", - len(ids) + len(stars)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	info = "Number in table: " + str(len(t)) + "\nNumber not in graph: " + str(len(t) - len(ids)) + "\nNumber that satisfy classifier: " + str(len(stars)) + "\nNumber that are junk: " + str(len(stars)-len(ids))
	plt.text(0.05, 0.80, info, transform = ax.transAxes, bbox = dict(facecolor = "white", alpha = 0.7))
	plt.hist(t[col][ids], bins = 100)
	plt.xlabel(col, fontsize = "x-large")
	plt.ylabel("Number", fontsize = "x-large")
	plotid.plotid()
	plt.show()

def col_mag(t1, col1, t2, col2):

	ids = np.where( (t1[col1] > 0.0) & (t1[col1] < 50.0) & (t2[col2] > 0.0) & (t2[col2] < 50.0) )[0]

	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.plot(t1[col1][ids]-t2[col2][ids], t1[col1][ids], "k.", ms = 2)
	plt.xlabel(col1 + "-" + col2, fontsize = "x-large")
	plt.ylabel(col1, fontsize = "x-large")
	plt.gca().invert_yaxis()
	plotid.plotid()
	info = "Number in table: " + str(len(t1)) + "\nNumber not in graph: " + str(len(t1) - len(ids))
	plt.text(0.05, 0.80, info, transform = ax.transAxes, bbox = dict(facecolor = "white", alpha = 0.7))
	plt.show()
