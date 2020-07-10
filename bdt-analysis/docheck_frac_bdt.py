from ROOT import *
#import numpy as np


doreweight = 0   #decide if we want to do the reweighting process

var = "ntrk" #change the var name according to the inputvar you want to read
mc = "sherpa_MC"   #do not change
inputvar = var  #by setting it as bdt (or ntrk,width,c1..), it will read the corresponding histogram, but remember to change the TLine range according to X-axis of different variable, one can check it by browsing the histograms in root file.

def myText(x,y,text, color = 1):
	l = TLatex()
	l.SetTextSize(0.025)
	l.SetNDC()
	l.SetTextColor(color)
	l.DrawLatex(x,y,text)
	pass

bdtbin = [-0.8,-0.4,-0.2,0,0.2,0.4,0.8]
ptbin = [500,600,800,1000,1200,1500,2000]

ntrackall = TFile("../root-files/dijet-sherpa-py-bdt.root")
ntrackall3 = TFile("../root-files/dijet-data-py-bdt.root")

for m in range(0,6):   #for only dijet event, start from jet pT>500 GeV
#for i in range(13):	#for gamma+jet combined with dijet event, start from jet pT>0 GeV
	for n in range(0,6):
                print(m)
		ptmin = ptbin[m]
		ptmax = ptbin[m+1]

		bdtmin = bdtbin[n]
		bdtmax = bdtbin[n+1]
                
                print(ptmin)
		print(bdtmin)

                higher_quark2 = ntrackall.Get(str(ptmin)+"_"+str(bdtmin)+"_LeadingJet_Forward_Quark_"+inputvar)
                higher_gluon2 = ntrackall.Get(str(ptmin)+"_"+str(bdtmin)+"_LeadingJet_Forward_Gluon_"+inputvar)
                higher_data2 = ntrackall3.Get(str(ptmin)+"_"+str(bdtmin)+"_LeadingJet_Forward_Data_"+inputvar)
                lower_quark2 = ntrackall.Get(str(ptmin)+"_"+str(bdtmin)+"_LeadingJet_Central_Quark_"+inputvar)
                lower_gluon2 = ntrackall.Get(str(ptmin)+"_"+str(bdtmin)+"_LeadingJet_Central_Gluon_"+inputvar)
                lower_data2 = ntrackall3.Get(str(ptmin)+"_"+str(bdtmin)+"_LeadingJet_Central_Data_"+inputvar)

                higher_quark = ntrackall.Get(str(ptmin)+"_"+str(bdtmin)+"_SubJet_Forward_Quark_"+inputvar)
                higher_gluon = ntrackall.Get(str(ptmin)+"_"+str(bdtmin)+"_SubJet_Forward_Gluon_"+inputvar)

                lower_quark = ntrackall.Get(str(ptmin)+"_"+str(bdtmin)+"_SubJet_Central_Quark_"+inputvar)
                lower_gluon = ntrackall.Get(str(ptmin)+"_"+str(bdtmin)+"_SubJet_Central_Gluon_"+inputvar)

                higher_data = ntrackall3.Get(str(ptmin)+"_"+str(bdtmin)+"_SubJet_Forward_Data_"+inputvar)
                lower_data = ntrackall3.Get(str(ptmin)+"_"+str(bdtmin)+"_SubJet_Central_Data_"+inputvar)


                #add leading and subleading jet from only dijet event together,
                #note that for gammajet+dijet event, we need to add leading jet from gammajet and leading jet from dijet sample together
                higher_data.Add(higher_data2)
                lower_data.Add(lower_data2)
                higher_quark.Add(higher_quark2)
                higher_gluon.Add(higher_gluon2)
                lower_quark.Add(lower_quark2)
                lower_gluon.Add(lower_gluon2)

                ToT_Fq2 = 0.
                ToT_Fg2 = 0.

                ToT_Cq2 =0.
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


                c = TCanvas("c","c",500,500)
                if (doreweight):
                    for i in range(1,higher_quark.GetNbinsX()+1):
                        if (lower_quark.GetBinContent(i) > 0 and lower_gluon.GetBinContent(i) > 0):
                            #print i,higher_quark.GetBinContent(i)/lower_quark.GetBinContent(i),higher_gluon.GetBinContent(i)/lower_gluon.GetBinContent(i)
                            factor_gluon = higher_gluon.GetBinContent(i)/lower_gluon.GetBinContent(i)
                            factor_quark = higher_quark.GetBinContent(i)/lower_quark.GetBinContent(i)
                            lower_quark.SetBinContent(i,lower_quark.GetBinContent(i)*factor_quark)
                            lower_gluon.SetBinContent(i,lower_gluon.GetBinContent(i)*factor_quark)
                            lower_data.SetBinContent(i,lower_data.GetBinContent(i)*factor_quark)
                            pass
                        pass
                        pass


                if (lower_quark.Integral() != 0):
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



                higher = higher_quark.Clone("")
                lower = higher_quark.Clone("")

                for i in range(1,higher.GetNbinsX()+1):
                        higher.SetBinContent(i,fg*higher_gluon.GetBinContent(i)+fq*higher_quark.GetBinContent(i))
                        lower.SetBinContent(i,cg*lower_gluon.GetBinContent(i)+cq*lower_quark.GetBinContent(i))
                        pass

                #Now, let's solve.

                quark = higher_quark.Clone("")
                gluon = higher_quark.Clone("")
                quark_data = higher_data.Clone("")
                gluon_data = higher_data.Clone("")

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
                        pass



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


                ## below just do the ploting

                gPad.SetLeftMargin(0.15)
                gPad.SetTopMargin(0.05)
                gPad.SetBottomMargin(0.15)

                if "SF" in mc:
                        quark_ratio = quark_data.Clone("")
                        gluon_ratio = gluon_data.Clone("")
                        quark_ratio.GetYaxis().SetTitle("Data/MC") #Data/MC
                        gluon_ratio.GetYaxis().SetTitle("Data/MC") #Data/MC
                if "MC" in mc:
                        quark_ratio = higher_quark.Clone("")
                        gluon_ratio = higher_gluon.Clone("")
                        quark_ratio.GetYaxis().SetTitle("MC Closure") #Data/MC
                        gluon_ratio.GetYaxis().SetTitle("MC Closure") #Data/MC

                quark_ratio.Divide(quark)
                gluon_ratio.Divide(gluon)

                print("plotting...")

                gStyle.SetOptStat(0)
                ######################## for ratio plot
                c.Divide(2,1)

                top = c.cd(1)
                top.SetPad(0.0,0.0,1.0,1.0)
                top.SetFillColor(0)
                top.SetBorderMode(0)
                top.SetBorderSize(2)
                top.SetTickx(1)
                top.SetTicky(1)
                top.SetLeftMargin(0.14)
                top.SetRightMargin(0.055)
                top.SetBottomMargin(0.3)#0.25
                top.SetFrameBorderMode(0)
                #top.SetLogy(1)

                bot = c.cd(2)
                bot.SetPad(0.0,0.0,1.0,0.3)
                bot.SetFillColor(0)
                bot.SetBorderMode(0)
                bot.SetBorderSize(2)
                bot.SetTickx(1)
                bot.SetTicky(1)
                bot.SetLeftMargin(0.14)
                bot.SetRightMargin(0.055)
                bot.SetTopMargin(0.045)
                bot.SetBottomMargin(0.4)
                bot.SetFrameBorderMode(0)

                quark.SetTitle("")
                quark.GetXaxis().SetTitle(var)
                quark.GetYaxis().SetTitle("Normalized to unity")
                quark.GetYaxis().SetNdivisions(505)
                quark.GetYaxis().SetRangeUser(-0.01,quark.GetMaximum()*1.5)
                #quark.GetYaxis().SetRangeUser(-0.01,0.05)
                quark.SetMarkerColor(8)
                quark.SetLineColor(8)
                quark.SetMarkerSize(0.5)
                quark.SetMarkerStyle(20)


                quark_data.SetMarkerColor(1)
                quark_data.SetLineColor(1)
                quark_data.SetMarkerSize(0.8)
                quark_data.SetMarkerStyle(29)

                higher_quark.SetMarkerColor(2)
                higher_quark.SetLineColor(2)
                higher_quark.SetMarkerSize(0.5)
                higher_quark.SetMarkerStyle(21)

                lower_quark.SetMarkerColor(4)
                lower_quark.SetLineColor(4)
                lower_quark.SetMarkerSize(0.5)
                lower_quark.SetMarkerStyle(22)


                quark_ratio.SetTitle("")
                quark_ratio.GetYaxis().SetRangeUser(0.7,1.3)
                quark_ratio.GetXaxis().SetTitle(var)
                quark_ratio.GetXaxis().SetTitleOffset(1)
                quark_ratio.GetXaxis().SetTitleSize(0.11)
                quark_ratio.GetXaxis().SetLabelSize(0.1)
                quark_ratio.GetXaxis().SetLabelOffset(0.03)
                quark_ratio.GetYaxis().SetTitleSize(0.1)
                quark_ratio.GetYaxis().SetTitleOffset(0.5)
                #quark_ratio.GetYaxis().SetLabelSize(0.2)
                quark_ratio.GetYaxis().SetLabelOffset(0.01)


                top.cd()
                quark.Draw()
                #		lower1.Draw("same")
                if "SF" in mc:
                    quark_data.Draw("same")
                if "MC" in mc:
                    higher_quark.Draw("same")
                #		lower_quark.Draw("same")
                #higher_data.Draw("same")
                #lower_data.Draw("same")

                leg = TLegend(0.6,0.5,0.9,0.7) ##0.6,0.5,0.9,0.7
                leg.SetTextFont(42)
                leg.SetFillColor(0)
                leg.SetBorderSize(0)
                leg.SetFillStyle(0)
                leg.SetNColumns(1)
                leg.AddEntry(quark,"Extracted quark (mc)","p")
                if "SF" in mc:
                    myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Internal}}}")
                    leg.AddEntry(quark_data,"Extracted quark (data)","p")
                if "MC" in mc:
                    leg.AddEntry(higher_quark,"higher quark (mc)","p")
                    myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Simulation Internal}}}")
                #leg.AddEntry(lower_quark,"lower quark (mc)","p")
                #leg.AddEntry(higher1,"higher (mc)","p")
                #leg.AddEntry(lower1,"lower (mc)","p")
                leg.Draw()

                myText(0.18,0.80,"#bf{#scale[1.5]{#sqrt{s} = 13 TeV}}")
                myText(0.18,0.76,"#bf{#scale[1.5]{BDT range: "+str(ptmin)+" - "+str(ptmax)+"}}")
                myText(0.18,0.72,"#bf{#scale[1.5]{p_{T} range: "+str(ptmin)+" - "+str(ptmax)+" GeV}}")

                if(inputvar == "ntrk"):
                        line = TLine(0.,1,60,1)
                if(inputvar == "bdt"):
                        line = TLine(-0.8,1,0.7,1)
                if(inputvar == "pt"):
                        line = TLine(0,1,2000,1)
                if(inputvar == "c1"):
                        line = TLine(0,1,0.4,1)
                if(inputvar == "eta"):
                        line = TLine(-2.5,1,2.5,1)
                if(inputvar == "width"):
                        line = TLine(0,1,0.4,1)
                #line = TLine(0.,1,0.4,1)
                '''
                pt_range = []

                if(var == "pt"):
                        for k in range(1,quark.GetNbinsX()):
                        if(quark.GetBinContent(k) != 0):
                                pt_range.append(quark.GetBinContent(k))

                print(min(pt_range),max(pt_range))
                '''
                bot.cd()
                quark_ratio.Draw()
                line.Draw("same")
                #c.Print("./plots_bdt/quark_"+str(min)+"_"+str(doreweight)+"_"+mc+"_"+var+"_fc.pdf")
                c.Print(var+"/quark_"+str(ptmin)+"_"+str(bdtmin)+"_"+str(doreweight)+"_"+mc+"_"+var+".pdf")




                gluon.SetTitle("")
                gluon.GetXaxis().SetTitle(var)
                gluon.GetYaxis().SetTitle("Normalized to unity")
                gluon.GetYaxis().SetNdivisions(505)
                #gluon.GetYaxis().SetRangeUser(-0.01,0.05)
                gluon.GetYaxis().SetRangeUser(-0.01,gluon.GetMaximum()*1.5)
                gluon.SetMarkerColor(8)
                gluon.SetLineColor(8)
                gluon.SetMarkerSize(0.5)
                gluon.SetMarkerStyle(20)

                gluon_data.SetMarkerColor(1)
                gluon_data.SetLineColor(1)
                gluon_data.SetMarkerSize(0.8)
                gluon_data.SetMarkerStyle(29)

                higher_gluon.SetMarkerColor(2)
                higher_gluon.SetLineColor(2)
                higher_gluon.SetMarkerSize(0.5)
                higher_gluon.SetMarkerStyle(21)

                lower_gluon.SetMarkerColor(4)
                lower_gluon.SetLineColor(4)
                lower_gluon.SetMarkerSize(0.5)
                lower_gluon.SetMarkerStyle(22)


                gluon_ratio.SetTitle("")
                gluon_ratio.GetYaxis().SetRangeUser(0.7,1.3)
                gluon_ratio.GetXaxis().SetTitle(var)
                gluon_ratio.GetXaxis().SetTitleOffset(1)
                gluon_ratio.GetXaxis().SetTitleSize(0.11)
                gluon_ratio.GetXaxis().SetLabelSize(0.1)
                gluon_ratio.GetXaxis().SetLabelOffset(0.03)
                gluon_ratio.GetYaxis().SetTitleSize(0.1)
                gluon_ratio.GetYaxis().SetTitleOffset(0.5)
                #gluon_ratio.GetYaxis().SetLabelSize(0.2)
                gluon_ratio.GetYaxis().SetLabelOffset(0.01)


                top.cd()
                gluon.Draw()
                if "SF" in mc:
                    gluon_data.Draw("same")
                if "MC" in mc:
                    higher_gluon.Draw("same")
                #lower_gluon.Draw("same")
                #higher_data.Draw("same")
                #lower_data.Draw("same")

                #leg = TLegend(0.3,0.4,0.6,0.6)
                #leg = TLegend(0.6,0.5,0.9,0.7) ##0.6,0.5,0.9,0.7
                leg = TLegend(0.2,0.5,0.5,0.7) ##0.6,0.5,0.9,0.7
                leg.SetTextFont(42)
                leg.SetFillColor(0)
                leg.SetBorderSize(0)
                leg.SetFillStyle(0)
                leg.SetNColumns(1)
                leg.AddEntry(gluon,"Extracted gluon (mc)","p")
                if "SF" in mc:
                    leg.AddEntry(gluon_data,"Extracted gluon (data)","p")
                    myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Internal}}}")
                if "MC" in mc:
                    myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Simulation Internal}}}")
                    leg.AddEntry(higher_gluon,"higher gluon (mc)","p")
                #leg.AddEntry(lower_gluon,"lower gluon (mc)","p")
                leg.Draw()

                myText(0.18,0.80,"#bf{#scale[1.5]{#sqrt{s} = 13 TeV}}")
                myText(0.18,0.76,"#bf{#scale[1.5]{BDT range: "+str(bdtmin)+" - "+str(bdtmax)+"}}")
                myText(0.18,0.72,"#bf{#scale[1.5]{p_{T} range: "+str(ptmin)+" - "+str(ptmax)+" GeV}}")

                if(inputvar == "ntrk"):
                        line = TLine(0.,1,60,1)
                if(inputvar == "bdt"):
                        line = TLine(-0.8,1,0.7,1)
                if(inputvar == "pt"):
                        line = TLine(0,1,2000,1)
                if(inputvar == "c1"):
                        line = TLine(0,1,0.4,1)
                if(inputvar == "eta"):
                        line = TLine(-2.5,1,2.5,1)
                if(inputvar == "width"):
                        line = TLine(0,1,0.4,1)

                bot.cd()
                gluon_ratio.Draw()
                line.Draw("same")
                c.Print(var+"/gluon_"+str(ptmin)+"_"+str(bdtmin)+"_"+str(doreweight)+"_"+mc+"_"+var+".pdf")
