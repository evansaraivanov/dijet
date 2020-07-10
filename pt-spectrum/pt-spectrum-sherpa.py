from ROOT import *

def myText(x,y,text,color=1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass

bin = [0,50,100,150,200,300,400,500,600,800,1000,1200,1500,2000]

#Change file based on sample you want to plot
#file = "../root-files/dijet-sherpa-py-nan.root"
file = "../root-files/dijet-pythia-py.root"

f = TFile(file)

pt_500_fq = f.Get("500_LeadingJet_Forward_Quark_pt")
pt_500_cq = f.Get("500_LeadingJet_Central_Quark_pt")
pt_500_fg = f.Get("500_LeadingJet_Forward_Gluon_pt")
pt_500_cg = f.Get("500_LeadingJet_Central_Gluon_pt")
pt_500_fo = f.Get("500_LeadingJet_Forward_Other_pt")
pt_500_co = f.Get("500_LeadingJet_Central_Other_pt")

pt_500_fq.Add(pt_500_cq)
pt_500_fq.Add(pt_500_fg)
pt_500_fq.Add(pt_500_cg)
pt_500_fq.Add(pt_500_fo)
pt_500_fq.Add(pt_500_co)

pt_500_fg.Add(pt_500_cg)
pt_500_fg.Add(pt_500_fo)
pt_500_fg.Add(pt_500_co)

pt_500_fo.Add(pt_500_co)

for i in range (8,13):
    pt_fq = f.Get(str(bin[i])+"_LeadingJet_Forward_Quark_pt")
    pt_cq = f.Get(str(bin[i])+"_LeadingJet_Central_Quark_pt")
    pt_fg = f.Get(str(bin[i])+"_LeadingJet_Forward_Gluon_pt")
    pt_cg = f.Get(str(bin[i])+"_LeadingJet_Central_Gluon_pt")
    pt_fo = f.Get(str(bin[i])+"_LeadingJet_Forward_Other_pt")
    pt_co = f.Get(str(bin[i])+"_LeadingJet_Central_Other_pt")

    pt_500_fq.Add(pt_fq)
    pt_500_fq.Add(pt_fo)
    pt_500_fq.Add(pt_cq)
    pt_500_fq.Add(pt_cg)
    pt_500_fq.Add(pt_co)
    pt_500_fq.Add(pt_fg)

    pt_500_fg.Add(pt_fg)
    pt_500_fg.Add(pt_cg)
    pt_500_fg.Add(pt_fo)
    pt_500_fg.Add(pt_co)

    pt_500_fo.Add(pt_fo)
    pt_500_fo.Add(pt_co)

c = TCanvas("c","c",500,500)
gPad.SetLogy()
gStyle.SetOptStat(0)
c.SetGrid()
gStyle.SetGridStyle(2)
gStyle.SetGridColor(15)
pt_500_fq.GetXaxis().SetTitle("p_{T} (GeV)")

if "sherpa" in file:
    pt_500_fq.SetMaximum(100)
    pt_500_fq.SetMinimum(10**(-8))
if "pythia" in file:
    pt_500_fq.SetMaximum(10000000)
    pt_500_fq.SetMinimum(10**(-6))

pt_500_fo.SetFillColor(2)
pt_500_fo.SetLineColor(2)
pt_500_fg.SetFillColor(4)
pt_500_fg.SetLineColor(4)
pt_500_fq.SetFillColor(8)
pt_500_fq.SetLineColor(1)
pt_500_fq.SetLineWidth(2)

leg = TLegend(0.62,0.6,0.88,0.88)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.AddEntry(pt_500_fq,"Total","l")
leg.AddEntry(pt_500_fq,"Quark Jet","f")
leg.AddEntry(pt_500_fg,"Gluon Jet","f")
leg.AddEntry(pt_500_fo,"Other Jet","f")

pt_500_fq.Draw("HIST ][")
pt_500_fg.Draw("hist same")
pt_500_fo.Draw("hist same")
leg.Draw("same")

myText(0.14,0.84,'#it{#bf{#scale[1.4]{#bf{ATLAS} Simulation Preliminary}}}')
myText(0.14,0.80,'#bf{#scale[1.2]{#sqrt{s}=13 TeV}}')
myText(0.14,0.76,'#bf{#scale[1.2]{Anti-K_{t} EM+JES R=0.4}}')
#myText(0.12,0.72,'#bf{#scale[1.2]{Leading Jet p_{T} Spectrum, Sherpa}}')

if "sherpa" in file:
    c.Print("pt-sherpa.pdf")
if "pythia" in file:
    c.Print("pt-pythia.pdf")
