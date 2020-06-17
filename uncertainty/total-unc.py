from ROOT import *
import numpy as np


doreweight = 0   #decide if we want to do the reweighting process

var = "ntrk"  #change the var name according to the inputvar you want to read
mc = "sherpa_SF"   #by setting it as "SF" or "MC", it will automatically making scale factor plots or MC closure plots
inputvar = "ntrk"  #by setting it as bdt (or ntrk,width,c1..), it will read the corresponding histogram, but remember to change the TLine range according to X-axis of different variable, one can check it by browsing the histograms in root file.

def myText(x,y,text, color = 1):
	l = TLatex()
	l.SetTextSize(0.025)
	l.SetNDC()
	l.SetTextColor(color)
	l.DrawLatex(x,y,text)
	pass

bin = [0, 50, 100, 150, 200, 300, 400, 500, 600, 800, 1000, 1200, 1500, 2000]

ntrackall = TFile("../root-files/dijet_sherpa_py.root")
ntrackall3 = TFile("../root-files/dijet_data_py.root")
ntrackall4 = TFile("../root-files/dijet-pythia-py.root")
ntrackall5 = TFile("../root-files/dijet-sherpa-pdf-54.root")
ntrackall6 = TFile("../root-files/dijet-sherpa-pdf-100.root")

for i in range(7,13):   #for only dijet event, start from jet pT>500 GeV
#for i in range(13):	#for gamma+jet combined with dijet event, start from jet pT>0 GeV
        if(bin[i] != 800):
		min = bin[i]
		max = bin[i+1]

		higher_quark = ntrackall.Get(str(min)+"_LeadingJet_Forward_Quark_"+inputvar)
		higher_quark2 = ntrackall.Get(str(min)+"_SubJet_Forward_Quark_"+inputvar)
		higher_gluon = ntrackall.Get(str(min)+"_LeadingJet_Forward_Gluon_"+inputvar)
		higher_gluon2 = ntrackall.Get(str(min)+"_SubJet_Forward_Gluon_"+inputvar)
		lower_quark = ntrackall.Get(str(min)+"_LeadingJet_Central_Quark_"+inputvar)
		lower_quark2 = ntrackall.Get(str(min)+"_SubJet_Central_Quark_"+inputvar)
		lower_gluon = ntrackall.Get(str(min)+"_LeadingJet_Central_Gluon_"+inputvar)
		lower_gluon2 = ntrackall.Get(str(min)+"_SubJet_Central_Gluon_"+inputvar)

		higher_data = ntrackall3.Get(str(min)+"_LeadingJet_Forward_Data_"+inputvar)
		higher_data2 = ntrackall3.Get(str(min)+"_SubJet_Forward_Data_"+inputvar)
		lower_data = ntrackall3.Get(str(min)+"_LeadingJet_Central_Data_"+inputvar)
		lower_data2 = ntrackall3.Get(str(min)+"_SubJet_Central_Data_"+inputvar)

		higher_quark_pythia = -1*ntrackall4.Get(str(min)+"_LeadingJet_Forward_Quark_"+inputvar)
		higher_quark2_pythia = -1*ntrackall4.Get(str(min)+"_SubJet_Forward_Quark_"+inputvar)
		higher_gluon_pythia = -1*ntrackall4.Get(str(min)+"_LeadingJet_Forward_Gluon_"+inputvar)
		higher_gluon2_pythia = -1*ntrackall4.Get(str(min)+"_SubJet_Forward_Gluon_"+inputvar)
		lower_quark_pythia = -1*ntrackall4.Get(str(min)+"_LeadingJet_Central_Quark_"+inputvar)
		lower_quark2_pythia = -1*ntrackall4.Get(str(min)+"_SubJet_Central_Quark_"+inputvar)
		lower_gluon_pythia = -1*ntrackall4.Get(str(min)+"_LeadingJet_Central_Gluon_"+inputvar)
		lower_gluon2_pythia = -1*ntrackall4.Get(str(min)+"_SubJet_Central_Gluon_"+inputvar)



		#add leading and subleading jet from only dijet event together,
		#note that for gammajet+dijet event, we need to add leading jet from gammajet and leading jet from dijet sample together
		higher_data.Add(higher_data2)
		lower_data.Add(lower_data2)
		quark_data = higher_data.Clone("")
		gluon_data = higher_data.Clone("")
		quark_pythia = higher_quark_pythia.Clone("")
		gluon_pythia = higher_quark_pythia.Clone("")
		higher_quark.Add(higher_quark2)
		higher_gluon.Add(higher_gluon2)
		lower_quark.Add(lower_quark2)
		lower_gluon.Add(lower_gluon2)

		higher_quark_pythia.Add(higher_quark2_pythia)
		higher_gluon_pythia.Add(higher_gluon2_pythia)
		lower_quark_pythia.Add(lower_quark2_pythia)
		lower_gluon_pythia.Add(lower_gluon2_pythia)

		higher_data_strap = higher_data.Clone("")     #Set aside for statistical uncertainty
		lower_data_strap = lower_data.Clone("")

		ToT_Fq2 = 0.
		ToT_Fg2 = 0.

		ToT_Cq2 = 0.
		ToT_Cg2 = 0.

 		ToT_Fq2_pythia = 0.
		ToT_Fg2_pythia = 0.

		ToT_Cq2_pythia = 0.
		ToT_Cg2_pythia = 0.

		for j in range(1,lower_quark.GetNbinsX()+1):
			ToT_Fq2+=higher_quark.GetBinContent(j)
			ToT_Cq2+=lower_quark.GetBinContent(j)
			ToT_Fg2+=higher_gluon.GetBinContent(j)
			ToT_Cg2+=lower_gluon.GetBinContent(j)

			ToT_Fq2_pythia += higher_quark_pythia.GetBinContent(j)
			ToT_Cq2_pythia += lower_quark_pythia.GetBinContent(j)
			ToT_Fg2_pythia += higher_gluon_pythia.GetBinContent(j)
			ToT_Cg2_pythia += lower_gluon_pythia.GetBinContent(j)

		# calculate the fraction of forward(higher) / central(lower) quark or gluon jet
		fg=ToT_Fg2/(ToT_Fg2+ToT_Fq2)
		cg=ToT_Cg2/(ToT_Cq2+ToT_Cg2)
		fq=1.-fg
		cq=1.-cg

		fg_pythia = ToT_Fg2_pythia/(ToT_Fg2_pythia + ToT_Fq2_pythia)
		cg_pythia = ToT_Cg2_pythia/(ToT_Cq2_pythia + ToT_Cg2_pythia)
		fq_pythia = 1.-fg_pythia
		cq_pythia = 1.-cg_pythia



		if (doreweight):
			for i in range(1,higher_quark.GetNbinsX()+1):
				if (lower_quark.GetBinContent(i) > 0 and lower_gluon.GetBinContent(i) > 0 and lower_quark_pythia.GetBinContent(i) > 0 and lower_gluon_pythia.GetBinContent(i) > 0):
					#print i,higher_quark.GetBinContent(i)/lower_quark.GetBinContent(i),higher_gluon.GetBinContent(i)/lower_gluon.GetBinContent(i)
					factor_gluon = higher_gluon.GetBinContent(i)/lower_gluon.GetBinContent(i)
					factor_quark = higher_quark.GetBinContent(i)/lower_quark.GetBinContent(i)
					factor_quark_pythia = higher_quark_pythia.GetBinContent(i)/lower_quark_pythia.GetBinContent(i)
					factor_gluon_pythia = higher_gluon_pythia.GetBinContent(i)/lower_gluon_pythia.GetBinContent(i)

					lower_quark.SetBinContent(i,lower_quark.GetBinContent(i)*factor_quark)
					lower_gluon.SetBinContent(i,lower_gluon.GetBinContent(i)*factor_quark)
					lower_quark_pythia.SetBinContent(i,lower_quark_pythia.GetBinContent(i)*factor_quark_pythia)
					lower_gluon_pythia.SetBinContent(i,lower_gluon_pythia.GetBinContent(i)*factor_quark_pythia)
					lower_data.SetBinContent(i,lower_data.GetBinContent(i)*factor_quark)
					pass
				pass
			pass


		if(lower_quark.Integral() != 0):
			lower_quark.Scale(1./lower_quark.Integral())
		if(lower_gluon.Integral() != 0):
			lower_gluon.Scale(1./lower_gluon.Integral())
		if(higher_quark.Integral() != 0):
			higher_quark.Scale(1./higher_quark.Integral())
		if(higher_gluon.Integral() != 0):
			higher_gluon.Scale(1./higher_gluon.Integral())
		if(lower_data.Integral() != 0):
			lower_data.Scale(1./lower_data.Integral())
		if(higher_data.Integral() != 0):
			higher_data.Scale(1./higher_data.Integral())
		if(lower_quark_pythia.Integral() != 0):
			lower_quark_pythia.Scale(1./lower_quark_pythia.Integral())
		if(lower_gluon_pythia.Integral() != 0):
			lower_gluon_pythia.Scale(1./lower_gluon_pythia.Integral())
		if(higher_quark_pythia.Integral() != 0):
			higher_quark_pythia.Scale(1./higher_quark_pythia.Integral())
		if(higher_gluon_pythia.Integral() != 0):
			higher_gluon_pythia.Scale(1./higher_gluon_pythia.Integral())


		higher = higher_quark.Clone("")
		lower = higher_quark.Clone("")
                higher_pythia = higher_quark_pythia.Clone("")
                lower_pythia = higher_quark_pythia.Clone("")

		for i in range(1,higher.GetNbinsX()+1):
			higher.SetBinContent(i,fg*higher_gluon.GetBinContent(i)+fq*higher_quark.GetBinContent(i))
			lower.SetBinContent(i,cg*lower_gluon.GetBinContent(i)+cq*lower_quark.GetBinContent(i))

                        higher_pythia.SetBinContent(i,fg_pythia*higher_gluon_pythia.GetBinContent(i)+fq_pythia*higher_quark_pythia.GetBinContent(i))
                        lower_pythia.SetBinContent(i,cg_pythia*lower_gluon_pythia.GetBinContent(i)+cq_pythia*lower_quark_pythia.GetBinContent(i))
			pass


		#Now, let's solve.

		quark = higher_quark.Clone("")
		gluon = higher_quark.Clone("")
		quark_data = higher_data.Clone("")
		gluon_data = higher_data.Clone("")
                quark_pythia = higher_quark_pythia.Clone("")
                gluon_pythia = higher_quark_pythia.Clone("")

                pdf_qvals = []
                pdf_gvals = []

                for i in range(1,higher.GetNbinsX()+1):
                        pdf_qvals += [np.zeros(101)]
                        pdf_gvals += [np.zeros(101)]

		#Matrix method here
		for i in range(1,higher.GetNbinsX()+1):
			F = higher.GetBinContent(i)
			C = lower.GetBinContent(i)
			if((cg*fq-fg*cq) != 0 ):
				Q = -(C*fg-F*cg)/(cg*fq-fg*cq)
				G = (C*fq-F*cq)/(cg*fq-fg*cq)
				quark.SetBinContent(i,Q)
				gluon.SetBinContent(i,G)
				#print "   ",i,G,higher_gluon.GetBinContent(i),lower_gluon.GetBinContent(i)

                #store in lists for pdf uncertainty.
            	pdf_qvals[i-1][0] = Q
            	pdf_gvals[i-1][0] = G

                #for pythia
		for i in range(1,higher_pythia.GetNbinsX()+1):
			F = higher_pythia.GetBinContent(i)
			C = lower_pythia.GetBinContent(i)
			if((cg_pythia*fq_pythia-fg_pythia*cq_pythia) != 0):
				Q = -(C*fg_pythia-F*cg_pythia)/(cg_pythia*fq_pythia-fg_pythia*cq_pythia)
				G = (C*fq_pythia-F*cq_pythia)/(cg_pythia*fq_pythia-fg_pythia*cq_pythia)
				quark_pythia.SetBinContent(i,Q)
				gluon_pythia.SetBinContent(i,G)
				#print "   ",i,G,higher_gluon.GetBinContent(i),lower_gluon.GetBinContent(i)

		quark_pythia.Draw("HIST")
		quark.Draw("HIST same")
#		c.Print("qtest.pdf")
		gluon_pythia.Draw("HIST")
		gluon.Draw("HIST same")
#		c.Print("gtest.pdf")

		#lower_data.Scale(1./lower_data.Integral())
		#higher_data.Scale(1./higher_data.Integral())
		#quark_data = higher_data.Clone("")
		#gluon_data = higher_data.Clone("")

		for i in range(1,higher_data.GetNbinsX()+1):
			F = higher_data.GetBinContent(i)
			C = lower_data.GetBinContent(i)
			if((cg*fq-fg*cq) != 0):
				Q = -(C*fg-F*cg)/(cg*fq-fg*cq)
				G = (C*fq-F*cq)/(cg*fq-fg*cq)
				quark_data.SetBinContent(i,Q)
				gluon_data.SetBinContent(i,G)
				#print "   ",i,"  ",G,"   ",Q
			pass

                #uncertainty calculations
                #uncertainty lists, number-of-bins lists of 4 uncertainties.
                sigma_tot_q = []
                sigma_tot_g = []

                for j in range(0,quark.GetNbinsX()):
                        sigma_tot_q += [np.zeros(4)]
                        sigma_tot_g += [np.zeros(4)]

                # do bootstrap
                #1. create lists to store bootstrapped values list of arrays of nstraps values
                nstraps = 5000
                Qvals = []
                Gvals = []

                for j in range(1,quark_data.GetNbinsX()+1):
                        Qvals += [np.zeros(nstraps)]
                        Gvals += [np.zeros(nstraps)]



                #do bootsrapping
                for k in range(nstraps):

                        forward_data_strap = higher_data.Clone("f"+str(k))
                        central_data_strap = lower_data.Clone("c"+str(k))

                        for j in range(1,higher.GetNbinsX()+1):
                                forward_data_strap.SetBinContent(j,np.random.poisson(higher_data_strap.GetBinContent(j)))
                                central_data_strap.SetBinContent(j,np.random.poisson(lower_data_strap.GetBinContent(j)))
                        for j in range(0,higher.GetNbinsX()):
                                F = forward_data_strap.GetBinContent(j)
                                C = central_data_strap.GetBinContent(j)
                                Q = -(C*fg-F*cg)/(cg*fq-fg*cq)
                                G = (C*fq-F*cq)/(cg*fq-fg*cq)

                                Qvals[j][k] = Q
                                Gvals[j][k] = G

                #compute the uncertainty and plots
                quark_strap = quark_data.Clone("")
                gluon_strap = gluon_data.Clone("")

                for j in range(0,quark_data.GetNbinsX()):
                        Qvals[j].sort()
                        Gvals[j].sort()
                        Q = np.median(Qvals[j])
                        G = np.median(Gvals[j])

                        sigmaQ = .5*(Qvals[j][int(.84*len(Qvals[j]))] - Qvals[j][int(.16*len(Qvals[j]))])
                        sigmaG = .5*(Gvals[j][int(.84*len(Gvals[j]))] - Gvals[j][int(.16*len(Gvals[j]))])

                        if(Q != 0):
                                sigmaQ = np.abs(sigmaQ/Q)
                        if(G != 0):
                                sigmaG = np.abs(sigmaG/G)

                        sigma_tot_q[j-1][0] = sigmaQ
                        sigma_tot_g[j-1][0] = sigmaG

                        quark_strap.SetBinContent(j,sigmaQ)
                        gluon_strap.SetBinContent(j,sigmaG)

                quark_negative = quark_strap.Clone("")
                gluon_negative = gluon_strap.Clone("")

                quark_negative = quark_negative * -1
                gluon_negative = gluon_negative * -1

                #mc uncertainty
                #uncertainty calculation percent difference
                quark_copy = quark.Clone("")
                gluon_copy = gluon.Clone("")

                quarkMC_negative = quark.Clone("")
                gluonMC_negative = gluon.Clone("")

                quark_copy.Add(higher_quark)
                gluon_copy.Add(higher_gluon)

                quark_copy.Scale(0.5)
                gluon_copy.Scale(0.5)

                quark_use = quark.Clone("")
                gluon_use = gluon.Clone("")

                quark_use.Add(higher_quark,-1)
                gluon_use.Add(lower_gluon,-1)

                for j in range(1,quark.GetNbinsX()+1):
                        a = quark_use.GetBinContent(j)
                        b = gluon_use.GetBinContent(j)

                        a = np.absolute(a)
                        b = np.absolute(b)

                        sigma_tot_q[j-1][1] = a
                        sigma_tot_g[j-1][1] = b

                        quark_use.SetBinContent(j,a)
                        gluon_use.SetBinContent(j,b)

                        quarkMC_negative.SetBinContent(j,-1*a)
                        gluonMC_negative.SetBinContent(j,-1*b)

                quark_use.Divide(quark_copy)
                gluon_use.Divide(gluon_copy)

                quarkMC_negative.Divide(quark_copy)
                gluonMC_negative.Divide(gluon_copy)

                for j in range(0,quark.GetNbinsX()):
                        sigma_tot_q[j][1] = quark_use.GetBinContent(j+1)
                        sigma_tot_g[j][1] = gluon_use.GetBinContent(j+1)



                #showering uncertainty extract. sherpa - pythia
                quark_show_copy = quark.Clone("") # Used for the denominator of percent difference
                gluon_show_copy = gluon.Clone("")

                quark_show_use = quark.Clone("") # Used for the numerator of percent difference
                gluon_show_use = gluon.Clone("")

                quark_show_negative = quark.Clone("") # used as negative copy of percent difference
                gluon_show_negative = quark.Clone("")

                quark_show_copy.Add(quark_pythia)
                gluon_show_copy.Add(gluon_pythia)

                quark_show_copy.Scale(0.5)
                gluon_show_copy.Scale(0.5)

                quark_show_use.Add(quark_pythia,-1)
                gluon_show_use.Add(gluon_pythia,-1)

                for j in range(1,quark.GetNbinsX()+1):
					c = quark_show_use.GetBinContent(j)
					d = gluon_show_use.GetBinContent(j)
					e = quark_show_copy.GetBinContent(j)
					f = gluon_show_copy.GetBinContent(j)

					print(100*c,e,"  ;  ",100*d,f)

					c = np.absolute(c)
					d = np.absolute(d)

					#sigma_tot_q[j-1][2] = c
					#sigma_tot_g[j-1][2] = d

					quark_show_use.SetBinContent(j,c)
					gluon_show_use.SetBinContent(j,d)

					quark_show_negative.SetBinContent(j,-1*c)
					gluon_show_negative.SetBinContent(j,-1*d)

                quark_show_use.Divide(quark_show_copy)
                gluon_show_use.Divide(gluon_show_copy)

                quark_show_negative.Divide(quark_show_copy)
                gluon_show_negative.Divide(gluon_show_copy)

                for j in range(0,quark.GetNbinsX()):
                        sigma_tot_q[j][2] = quark_show_use.GetBinContent(j+1)
                        sigma_tot_g[j][2] = gluon_show_use.GetBinContent(j+1)



                #pdf uncertainty. stdev of binvals
                #open the histograms for each pdf weight.
                for k in range(1,101):
                        if(k < 55):
                                higher_quark = ntrackall5.Get(str(min)+"_LeadingJet_Forward_Quark"+str(k)+"_"+inputvar)
                                higher_quark1 = ntrackall5.Get(str(min)+"_SubJet_Forward_Quark"+str(k)+"_"+inputvar)
                                lower_quark = ntrackall5.Get(str(min)+"_LeadingJet_Central_Quark"+str(k)+"_"+inputvar)
                                lower_quark1 = ntrackall5.Get(str(min)+"_SubJet_Central_Quark"+str(k)+"_"+inputvar)
                                higher_gluon = ntrackall5.Get(str(min)+"_LeadingJet_Forward_Quark"+str(k)+"_"+inputvar)
                                higher_gluon1 = ntrackall5.Get(str(min)+"_LeadingJet_Forward_Quark"+str(k)+"_"+inputvar)
                                lower_gluon = ntrackall5.Get(str(min)+"_LeadingJet_Forward_Quark"+str(k)+"_"+inputvar)
                                lower_gluon1 = ntrackall5.Get(str(min)+"_LeadingJet_Forward_Quark"+str(k)+"_"+inputvar)
                        else:
                                higher_quark = ntrackall6.Get(str(min)+"_LeadingJet_Forward_Quark"+str(k)+"_"+inputvar)
                                higher_quark1 = ntrackall6.Get(str(min)+"_SubJet_Forward_Quark"+str(k)+"_"+inputvar)
                                lower_quark = ntrackall6.Get(str(min)+"_LeadingJet_Central_Quark"+str(k)+"_"+inputvar)
                                lower_quark1 = ntrackall6.Get(str(min)+"_SubJet_Central_Quark"+str(k)+"_"+inputvar)
                                higher_gluon = ntrackall6.Get(str(min)+"_LeadingJet_Forward_Quark"+str(k)+"_"+inputvar)
                                higher_gluon1 = ntrackall6.Get(str(min)+"_LeadingJet_Forward_Quark"+str(k)+"_"+inputvar)
                                lower_gluon = ntrackall6.Get(str(min)+"_LeadingJet_Forward_Quark"+str(k)+"_"+inputvar)
                                lower_gluon1 = ntrackall6.Get(str(min)+"_LeadingJet_Forward_Quark"+str(k)+"_"+inputvar)

                        higher_quark.Add(higher_quark1)
                        higher_gluon.Add(higher_gluon1)
                        lower_quark.Add(lower_quark1)
                        lower_gluon.Add(lower_gluon1)

                        ToT_Fq2 = 0.
                        ToT_Fg2 = 0.

                        ToT_Cq2 = 0.
                        ToT_Cg2 = 0.

                        for j in range(1,lower_quark.GetNbinsX()+1):
                                ToT_Fq2+=higher_quark.GetBinContent(j)
                                ToT_Cq2+=lower_quark.GetBinContent(j)
                                ToT_Fg2+=higher_gluon.GetBinContent(j)
                                ToT_Cg2+=lower_gluon.GetBinContent(j)

                        # calculate the fraction of forward(higher) / central(lower) quark or gluon jet
                        fg=ToT_Fg2/(ToT_Fg2+ToT_Fq2)
                        cg=ToT_Cg2/(ToT_Cq2+ToT_Cg2)
                        fq=1.-fg
                        cq=1.-cg

                        if (doreweight):
                                for i in range(1,higher_quark.GetNbinsX()+1):
                                        if (lower_quark.GetBinContent(i) > 0 and lower_gluon.GetBinContent(i) > 0):
                                                #print i,higher_quark.GetBinContent(i)/lower_quark.GetBinContent(i),higher_gluon.GetBinContent(i)/lower_gluon.GetBinContent(i)
                                                factor_gluon = higher_gluon.GetBinContent(i)/lower_gluon.GetBinContent(i)
                                                factor_quark = higher_quark.GetBinContent(i)/lower_quark.GetBinContent(i)

                                                lower_quark.SetBinContent(i,lower_quark.GetBinContent(i)*factor_quark)
                                                lower_gluon.SetBinContent(i,lower_gluon.GetBinContent(i)*factor_quark)
                                                pass
                                        pass
                                pass


                        if(lower_quark.Integral() != 0):
                                lower_quark.Scale(1./lower_quark.Integral())
                        if(lower_gluon.Integral() != 0):
                                lower_gluon.Scale(1./lower_gluon.Integral())
                        if(higher_quark.Integral() != 0):
                                higher_quark.Scale(1./higher_quark.Integral())
                        if(higher_gluon.Integral() != 0):
                                higher_gluon.Scale(1./higher_gluon.Integral())

                        higher = higher_quark.Clone("")
                        lower = higher_quark.Clone("")

                        for i in range(1,higher.GetNbinsX()+1):
                                higher.SetBinContent(i,fg*higher_gluon.GetBinContent(i)+fq*higher_quark.GetBinContent(i))
                                lower.SetBinContent(i,cg*lower_gluon.GetBinContent(i)+cq*lower_quark.GetBinContent(i))
                                pass

                        #Now, let's solve.

                        quark = higher_quark.Clone("")
                        gluon = higher_quark.Clone("")

                        #Matrix method here
                        for i in range(1,higher.GetNbinsX()+1):
                                F = higher.GetBinContent(i)
                                C = lower.GetBinContent(i)
                                if((cg*fq-fg*cq) != 0 ):
                                        Q = -(C*fg-F*cg)/(cg*fq-fg*cq)
                                        G = (C*fq-F*cq)/(cg*fq-fg*cq)

                                        pdf_qvals[i-1][k] = Q
                                        pdf_gvals[i-1][k] = G

                quark_pdf = quark.Clone("")
                gluon_pdf = quark.Clone("")

                for j in range(0,quark.GetNbinsX()):
                        pdf_qvals[j].sort()
                        pdf_gvals[j].sort()
                        Q = np.median(pdf_qvals[j])
                        G = np.median(pdf_gvals[j])

                        pdf_sigmaQ = .5*(pdf_qvals[j][int(.84*len(pdf_qvals[j]))] - pdf_qvals[j][int(.16*len(pdf_qvals[j]))])
                        pdf_sigmaG = .5*(pdf_gvals[j][int(.84*len(pdf_gvals[j]))] - pdf_gvals[j][int(.16*len(pdf_gvals[j]))])

                        if(Q != 0):
                                pdf_sigmaQ = np.abs(pdf_sigmaQ/Q)
                        if(G != 0):
                                pdf_sigmaG = np.abs(pdf_sigmaG/G)

                        sigma_tot_q[j][3] = pdf_sigmaQ
                        sigma_tot_g[j][3] = pdf_sigmaG

                        quark_pdf.SetBinContent(j+1,pdf_sigmaQ)
                        gluon_pdf.SetBinContent(j+1,pdf_sigmaG)

                quark_pdf_negative = quark_pdf.Clone("")
                gluon_pdf_negative = gluon_pdf.Clone("")

                quark_pdf_negative = quark_pdf_negative * -1
                gluon_pdf_negative = gluon_pdf_negative * -1

                #total uncertainty
                q_sigma_tot = quark.Clone("")
                g_sigma_tot = gluon.Clone("")

                for j in range (0, quark.GetNbinsX()):
                        a = sigma_tot_q[j][0]
                        b = sigma_tot_q[j][1]
                        c = sigma_tot_q[j][2]
                        d = sigma_tot_q[j][3]
                        sigma_q_tot = np.sqrt((a**2)+(b**2)+(c**2)+(d**2))

                        a = sigma_tot_g[j][0]
                        b = sigma_tot_g[j][1]
                        c = sigma_tot_g[j][2]
                        d = sigma_tot_g[j][3]
                        sigma_g_tot = np.sqrt((a**2)+(b**2)+(c**2)+(d**2))

                        q_sigma_tot.SetBinContent(j+1,sigma_q_tot)
                        g_sigma_tot.SetBinContent(j+1,sigma_g_tot)

                q_sigma_tot.Scale(100)
                g_sigma_tot.Scale(100)

                q_sigma_tot_n = q_sigma_tot.Clone("")
                g_sigma_tot_n = g_sigma_tot.Clone("")
                q_sigma_tot_n.Scale(-1)
                g_sigma_tot_n.Scale(-1)

                quark_pdf.Scale(100)
                gluon_pdf.Scale(100)
                quark_pdf_negative.Scale(100)
                gluon_pdf_negative.Scale(100)

                quark_show_use.Scale(100)
                gluon_show_use.Scale(100)
                quark_show_negative.Scale(100)
                gluon_show_negative.Scale(100)

                quark_use.Scale(100)
                gluon_use.Scale(100)
                quarkMC_negative.Scale(100)
                gluonMC_negative.Scale(100)


                quark_strap.Scale(100)
                gluon_strap.Scale(100)
                quark_negative.Scale(100)
                gluon_negative.Scale(100)


                c = TCanvas("c","c",500,500)
		## below just do the ploting

		gPad.SetLeftMargin(0.15)
		gPad.SetTopMargin(0.05)
		gPad.SetBottomMargin(0.15)
                gPad.SetRightMargin(0.2)



		gStyle.SetOptStat(0)
		######################## for ratio plo

		quark_strap.GetYaxis().SetRangeUser(-25,25)
		quark_strap.SetLineColor(2)
		quark_strap.SetLineStyle(2)
		#quark_strap.SetMarkerColor(8)
		#quark_strap.SetMarkerSize(0.8)
		quark_negative.SetLineColor(2)
		quark_negative.SetLineStyle(2)
		#quark_negative.SetMarkerSize(0.8)
		#quark_negative.SetMarkerColor(8)

		quark_use.SetLineColor(30)
		quark_use.SetLineStyle(2)
		#quark_use.SetMarkerColor(2)
		#quark_use.SetMarkerSize(0.8)
		quarkMC_negative.SetLineColor(30)
		quarkMC_negative.SetLineStyle(2)
                #quarkMC_negative.SetMarkerColor(2)
		#quarkMC_negative.SetMarkerSize(0.8)

                quark_show_use.SetLineColor(6)
                quark_show_use.SetLineStyle(2)
                quark_show_negative.SetLineColor(6)
                quark_show_negative.SetLineStyle(2)

                quark_pdf.SetLineColor(28)
                quark_pdf.SetLineStyle(2)
                quark_pdf_negative.SetLineColor(28)
                quark_pdf_negative.SetLineStyle(2)

                q_sigma_tot.SetLineColor(4)
                q_sigma_tot.SetLineStyle(1)
                q_sigma_tot.SetLineWidth(2)
                q_sigma_tot_n.SetLineColor(4)
                q_sigma_tot_n.SetLineStyle(1)
                q_sigma_tot_n.SetLineWidth(2)

                quark_strap.GetYaxis().SetTitle("Uncertainty (%)")

                quark_strap.Draw("HIST")
                quark_negative.Draw("HIST same")
                quark_use.Draw("HIST same")
                quarkMC_negative.Draw("HIST same")
                quark_show_use.Draw("HIST same")
                quark_show_negative.Draw("HIST same")
                quark_pdf.Draw("HIST same")
                quark_pdf_negative.Draw("HIST same")
                q_sigma_tot.Draw("HIST same")
                q_sigma_tot_n.Draw("HIST same")

		leg = TLegend(0.82,0.7,0.98,0.9) ##0.6,0.5,0.9,0.7
		leg.SetTextFont(42)
		leg.SetFillColor(0)
		leg.SetBorderSize(0)
		leg.SetFillStyle(0)
		leg.SetNColumns(1)
		leg.AddEntry(quark_strap,"Statistical","l")
		leg.AddEntry(quark_use,"MC Closure","l")
                leg.AddEntry(quark_show_use,"Showering","l")
                leg.AddEntry(quark_pdf,"PDF","l")
                leg.AddEntry(q_sigma_tot,"Total","l")

		myText(0.18,0.9,"#it{#bf{#scale[1.8]{#bf{ATLAS} Internal}}}")

		leg.Draw()

		myText(0.18,0.86,"#bf{#scale[1.5]{#sqrt{s} = 13 TeV}}")
		myText(0.18,0.82,"#bf{#scale[1.5]{pT range: "+str(min)+" - "+str(max)+" GeV}}")
                myText(0.18,0.78,"#bf{#scale[1.5]{Quark jet}}")

                if(inputvar == "ntrk"):
		    line = TLine(0.,0,60,0)
                    quark_strap.GetXaxis().SetTitle("n_{Track}")
                if(inputvar == "bdt"):
		    line = TLine(-0.8,0,0.7,0)
                    quark_strap.GetXaxis().SetTitle("BDT")
#		line = TLine(0.,1,0.4,1)

#		quark_ratio.Draw()
		line.Draw("same")
		#c.Print("./plots_bdt/quark_"+str(min)+"_"+str(doreweight)+"_"+mc+"_"+var+"_fc.pdf")
		c.Print("./plots_"+var+"/quark_"+str(min)+"_"+str(doreweight)+"_"+mc+"_"+var+".pdf")


                gluon_strap.GetYaxis().SetTitle("Uncertainty (%)")
		gluon_strap.GetYaxis().SetRangeUser(-25,25)


		gluon_strap.SetLineColor(2)
		gluon_strap.SetLineStyle(2)
		#gluon_strap.SetMarkerColor(2)
		#gluon_strap.SetMarkerSize(0.8)
		gluon_negative.SetLineColor(2)
		gluon_negative.SetLineStyle(2)
		#gluon_negative.SetMarkerColor(2)
		#gluon_negative.SetMarkerSize(0.8)


		gluon_use.SetLineColor(30)
		gluon_use.SetLineStyle(2)
		#gluon_use.SetMarkerColor(30)
		#gluon_use.SetMarkerSize(0.8)
		gluonMC_negative.SetLineColor(30)
		gluonMC_negative.SetLineStyle(2)
		#gluonMC_negative.SetMarkerColor(30)
		#gluonMC_negative.SetMarkerSize(0.8)

                gluon_show_use.SetLineColor(6)
                gluon_show_use.SetLineStyle(2)
                gluon_show_negative.SetLineColor(6)
                gluon_show_negative.SetLineStyle(2)

                gluon_pdf.SetLineColor(28)
                gluon_pdf.SetLineStyle(2)
                gluon_pdf_negative.SetLineColor(28)
                gluon_pdf_negative.SetLineStyle(2)

                g_sigma_tot.SetLineColor(4)
                g_sigma_tot.SetLineStyle(1)
                g_sigma_tot.SetLineWidth(2)
                g_sigma_tot_n.SetLineColor(4)
                g_sigma_tot_n.SetLineStyle(1)
                g_sigma_tot_n.SetLineWidth(2)

                gluon_strap.Draw("HIST")
                gluon_negative.Draw("HIST same")
                gluon_use.Draw("HIST same")
                gluonMC_negative.Draw("HIST same")
                gluon_show_use.Draw("HIST same")
                gluon_show_negative.Draw("HIST same")
                gluon_pdf.Draw("HIST same")
                gluon_pdf_negative.Draw("HIST same")
                g_sigma_tot.Draw("HIST same")
                g_sigma_tot_n.Draw("HIST same")

		leg = TLegend(0.82,0.7,0.98,0.9) ##0.6,0.5,0.9,0.7
		leg.SetTextFont(42)
		leg.SetFillColor(0)
		leg.SetBorderSize(0)
		leg.SetFillStyle(0)
		leg.SetNColumns(1)
		leg.AddEntry(gluon_strap,"Statistical","l")
                leg.AddEntry(gluon_use,"MC Closure","l")
                leg.AddEntry(gluon_show_use,"Showering","l")
                leg.AddEntry(gluon_pdf,"PDF","l")
                leg.AddEntry(g_sigma_tot,"Total","l")

		myText(0.18,0.9,"#it{#bf{#scale[1.8]{#bf{ATLAS} Internal}}}")

		leg.Draw()

		myText(0.18,0.86,"#bf{#scale[1.5]{#sqrt{s} = 13 TeV}}")
		myText(0.18,0.82,"#bf{#scale[1.5]{pT range: "+str(min)+" - "+str(max)+" GeV}}")
                myText(0.18,0.78,"#bf{#scale[1.5]{Gluon jet}}")

                if(inputvar == "ntrk"):
		    line = TLine(0.,0,60,0)
                    gluon_strap.GetXaxis().SetTitle("n_{Track}")
                if(inputvar == "bdt"):
		    line = TLine(-0.8,0,0.7,0)
                    gluon_strap.GetXaxis().SetTitle("BDT")

#		bot.cd()
#		gluon_ratio.Draw()
		line.Draw("same")
		c.Print("./plots_"+var+"/gluon_"+str(min)+"_"+str(doreweight)+"_"+mc+"_"+var+".pdf")
