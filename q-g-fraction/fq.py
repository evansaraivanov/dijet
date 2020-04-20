from ROOT import *
import numpy as np

def myText(x,y,text,color=1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass

var = "bdt"

file1 = TFile("../root-files/dijet-sherpa-py-nan.root")
file2 = TFile("../root-files/dijet-sherpa-eta.root")

bin = np.array([500.,600.,800.,1000.,1200.,1500.,2000.])
bin2 = np.array([0.0,0.5,1.0,2.1])

gStyle.SetOptStat(0)
c = TCanvas("","",500,500)
gPad.SetTickx()
gPad.SetTicky()

pt_higher_quark =  TH1F("pt_higher_quark","",6,bin)
pt_higher_gluon =  TH1F("pt_higher_gluon","",6,bin)
pt_lower_quark = TH1F("pt_lower_quark","",6,bin)
pt_lower_gluon = TH1F("pt_lower_gluon","",6,bin)

eta_higher_quark = TH1F("eta_higher_quark","",3,bin2)
eta_higher_gluon = TH1F("eta_higher_gluon","",3,bin2)
eta_lower_quark = TH1F("eta_lower","",3,bin2)
eta_lower_gluon = TH1F("eta_lower_gluon","",3,bin2)

bin = np.array([500,600,800,1000,1200,1500,2000])

fq1_list = np.zeros(6) #these will hold fq values for different pt ranges
fq2_list = np.zeros(6)

for i in range(0,6):
    higher_quark = file1.Get(str(bin[i])+"_SubJet_Forward_Quark_"+var)
    higher_gluon = file1.Get(str(bin[i])+"_SubJet_Forward_Gluon_"+var)

    if(bin[i] != 800):
        higher_quark1 = file1.Get(str(bin[i])+"_LeadingJet_Forward_Quark_"+var)
        higher_gluon1 = file1.Get(str(bin[i])+"_LeadingJet_Forward_Gluon_"+var)
        higher_quark.Add(higher_quark1)
        higher_gluon.Add(higher_gluon1)

    lower_quark = file1.Get(str(bin[i])+"_LeadingJet_Central_Quark_"+var)
    lower_quark1 = file1.Get(str(bin[i])+"_SubJet_Central_Quark_"+var)
    lower_gluon = file1.Get(str(bin[i])+"_LeadingJet_Central_Gluon_"+var)
    lower_gluon1 = file1.Get(str(bin[i])+"_SubJet_Central_Gluon_"+var)


    lower_quark.Add(lower_quark1)
    lower_gluon.Add(lower_gluon1)

    tq1 = 0.  #1 refers to higher eta jet, 2 refers to lower eta
    tg1 = 0.
    tq2 = 0.
    tg2 = 0.

    var_q1 = 0.
    var_q2 = 0.
    var_g1 = 0.
    var_g2 = 0.

    for j in range(1, higher_quark.GetNbinsX()+1):
        tq1 += higher_quark.GetBinContent(j)
        tg1 += higher_gluon.GetBinContent(j)
        tq2 += lower_quark.GetBinContent(j)
        tg2 += lower_gluon.GetBinContent(j)

        var_q1 += (higher_quark.GetBinError(j)*higher_quark.GetBinError(j))
        var_q2 += (lower_quark.GetBinError(j)*lower_quark.GetBinError(j))
        var_g1 += (higher_gluon.GetBinError(j)*higher_gluon.GetBinError(j))
        var_g2 += (lower_gluon.GetBinError(j)*lower_gluon.GetBinError(j))

    var_tot_1 = var_q1 + var_g1
    var_tot_2 = var_q2 + var_g2

    fq1 = tq1/(tq1+tg1)
    fq2 = tq2/(tq2+tg2)
    fg1 = 1.-fq1
    fg2 = 1.-fq2

    var_fq1 = fq1*fq1 * ((var_tot_1 / ((tq1+tg1)*(tq1+tg1))) + (var_q1/(tq1*tq1)))
    var_fq2 = fq2*fq2 * ((var_tot_2 / ((tq2+tg2)*(tq2+tg2))) + (var_q2/(tq2*tq2)))
    var_fg1 = fg1*fg1 * ((var_tot_1 / ((tq1+tg1)*(tq1+tg1))) + (var_q1/(tq1*tq1)))
    var_fg2 = fg2*fg2 * ((var_tot_2 / ((tq2+tg2)*(tq2+tg2))) + (var_q2/(tq2*tq2)))

    pt_higher_quark.SetBinContent(i+1,fq1)
    pt_higher_gluon.SetBinContent(i+1,fg1)
    pt_lower_quark.SetBinContent(i+1,fq2)
    pt_lower_gluon.SetBinContent(i+1,fg2)

    pt_higher_quark.SetBinError(i+1,np.sqrt(var_fq1))
    pt_higher_gluon.SetBinError(i+1,np.sqrt(var_fg1))
    pt_lower_quark.SetBinError(i+1,np.sqrt(var_fq2))
    pt_lower_gluon.SetBinError(i+1,np.sqrt(var_fg2))

pt_higher_quark.SetMaximum(1.)
pt_higher_quark.SetMinimum(0.)
pt_higher_quark.GetYaxis().SetTitle("Fraction")
pt_higher_quark.GetXaxis().SetTitle("p_{T} (GeV)")

pt_higher_quark.SetLineColor(6)
pt_higher_gluon.SetLineColor(2)
pt_lower_quark.SetLineColor(4)
pt_lower_gluon.SetLineColor(8)

pt_higher_quark.SetLineWidth(2)
pt_higher_gluon.SetLineWidth(2)
pt_lower_quark.SetLineWidth(2)
pt_lower_gluon.SetLineWidth(2)

leg1 = TLegend(.15,0.15,0.45,0.3)
leg1.SetNColumns(2)
leg1.AddEntry(pt_higher_quark,"f_{H,Q}","l")
leg1.AddEntry(pt_higher_gluon,"f_{H,G}","l")
leg1.AddEntry(pt_lower_quark,"f_{L,Q}","l")
leg1.AddEntry(pt_lower_gluon,"f_{L,G}","l")
leg1.SetBorderSize(0)
leg1.SetFillStyle(0)

line = TLine(500.,0.5,2000.,0.5)
line.SetLineColor(1)
line.SetLineWidth(2)

pt_higher_quark.Draw("HIST E")
pt_higher_gluon.Draw("HIST E same")
pt_lower_quark.Draw("HIST E same")
pt_lower_gluon.Draw("HIST E same")
line.Draw("same")
leg1.Draw("same")

myText(0.14,0.84,'#it{#bf{#scale[1.4]{#bf{ATLAS} Simulation Preliminary}}}')
myText(0.14,0.80,'#bf{#scale[1.2]{#sqrt{s}=13 TeV}}')
myText(0.14,0.76,'#bf{#scale[1.2]{Anti-K_{t} EM+JES R=0.4}}')

c.Print("pt-fraction.pdf")

#for eta range
for i in range(0,3):
    higher_quark_eta = file2.Get(str(bin2[i])+"_SubJet_Forward_Quark_"+var)
    higher_gluon_eta = file2.Get(str(bin2[i])+"_SubJet_Forward_Gluon_"+var)

    if(bin2[i] != 1.0):
        higher_quark1_eta = file2.Get(str(bin2[i])+"_LeadingJet_Forward_Quark_"+var)
        higher_gluon1_eta = file2.Get(str(bin2[i])+"_LeadingJet_Forward_Gluon_"+var)

        higher_quark_eta.Add(higher_quark1_eta)
        higher_gluon_eta.Add(higher_gluon1_eta)

    lower_quark_eta = file2.Get(str(bin2[i])+"_LeadingJet_Central_Quark_"+var)
    lower_quark1_eta = file2.Get(str(bin2[i])+"_SubJet_Central_Quark_"+var)
    lower_gluon_eta = file2.Get(str(bin2[i])+"_LeadingJet_Central_Gluon_"+var)
    lower_gluon1_eta = file2.Get(str(bin2[i])+"_SubJet_Central_Gluon_"+var)

    lower_quark_eta.Add(lower_quark1_eta)
    lower_gluon_eta.Add(lower_gluon1_eta)

    tq1 = 0. #1 refers to higher eta jet, 2 refers to lower eta
    tg1 = 0.
    tq2 = 0.
    tg2 = 0.

    var_q1 = 0.
    var_q2 = 0.
    var_g1 = 0.
    var_g2 = 0.

    for j in range(1, higher_quark.GetNbinsX()+1):
        tq1 += higher_quark_eta.GetBinContent(j)
        tg1 += higher_gluon_eta.GetBinContent(j)
        tq2 += lower_quark_eta.GetBinContent(j)
        tg2 += lower_gluon_eta.GetBinContent(j)

        var_q1 += (higher_quark.GetBinError(j)*higher_quark.GetBinError(j))
        var_q2 += (lower_quark.GetBinError(j)*lower_quark.GetBinError(j))
        var_g1 += (higher_gluon.GetBinError(j)*higher_gluon.GetBinError(j))
        var_g2 += (lower_gluon.GetBinError(j)*lower_gluon.GetBinError(j))

    var_tot_1 = var_q1 + var_g1
    var_tot_2 = var_q2 + var_g2

    fq1 = tq1/(tq1+tg1)
    fq2 = tq2/(tq2+tg2)
    fg1 = 1.-fq1
    fg2 = 1.-fq2

    var_fq1 = fq1*fq1 * ((var_tot_1 / ((tq1+tg1)*(tq1+tg1))) + (var_q1/(tq1*tq1)))
    var_fq2 = fq2*fq2 * ((var_tot_2 / ((tq2+tg2)*(tq2+tg2))) + (var_q2/(tq2*tq2)))
    var_fg1 = fg1*fg1 * ((var_tot_1 / ((tq1+tg1)*(tq1+tg1))) + (var_q1/(tq1*tq1)))
    var_fg2 = fg2*fg2 * ((var_tot_2 / ((tq2+tg2)*(tq2+tg2))) + (var_q2/(tq2*tq2)))

    eta_higher_quark.SetBinContent(i+1,fq1)
    eta_higher_gluon.SetBinContent(i+1,fg1)
    eta_lower_quark.SetBinContent(i+1,fq2)
    eta_lower_gluon.SetBinContent(i+1,fg2)

    eta_higher_quark.SetBinError(i+1,np.sqrt(var_fq1))
    eta_lower_quark.SetBinError(i+1,np.sqrt(var_fq2))
    eta_higher_gluon.SetBinError(i+1,np.sqrt(var_fg1))
    eta_lower_gluon.SetBinError(i+1,np.sqrt(var_fg2))

eta_higher_quark.SetMaximum(1.)
eta_higher_quark.SetMinimum(0.)
eta_higher_quark.GetYaxis().SetTitle("Fraction")
eta_higher_quark.GetXaxis().SetTitle("|\eta|")

eta_higher_quark.SetLineColor(6)
eta_higher_gluon.SetLineColor(2)
eta_lower_quark.SetLineColor(4)
eta_lower_gluon.SetLineColor(8)

eta_higher_quark.SetLineWidth(2)
eta_higher_gluon.SetLineWidth(2)
eta_lower_quark.SetLineWidth(2)
eta_lower_gluon.SetLineWidth(2)

leg1 = TLegend(.15,0.15,0.45,0.3)
leg1.SetNColumns(2)
leg1.AddEntry(pt_higher_quark,"f_{H,Q}","l")
leg1.AddEntry(pt_higher_gluon,"f_{H,G}","l")
leg1.AddEntry(pt_lower_quark,"f_{L,Q}","l")
leg1.AddEntry(pt_lower_gluon,"f_{L,G}","l")
leg1.SetBorderSize(0)
leg1.SetFillStyle(0)

line = TLine(0.0,0.5,2.1,0.5)
line.SetLineColor(1)
line.SetLineWidth(2)

eta_higher_quark.Draw("HIST E")
eta_higher_gluon.Draw("HIST E same")
eta_lower_quark.Draw("HIST E same")
eta_lower_gluon.Draw("HIST E same")
line.Draw("same")
leg1.Draw("same")

myText(0.14,0.84,'#it{#bf{#scale[1.4]{#bf{ATLAS} Simulation Preliminary}}}')
myText(0.14,0.80,'#bf{#scale[1.2]{#sqrt{s}=13 TeV}}')
myText(0.14,0.76,'#bf{#scale[1.2]{Anti-K_{t} EM+JES R=0.4}}')

c.Print("eta-fraction.pdf")
