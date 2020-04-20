from ROOT import *

def myText(x,y,text,color=1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass

bin = [0,50,100,150,200,300,400,500,600,800,1000,1200,1500,2000]

f = TFile("../root-files/dijet-sherpa-py-nan.root")

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

for i in range (8,13):
    pt_fq = f.Get(str(bin[i])+"_LeadingJet_Forward_Quark_pt")
    pt_fo = f.Get(str(bin[i])+"_LeadingJet_Forward_Other_pt")

    pt_500_fq.Add(pt_fq)
    pt_500_fq.Add(pt_fo)

    pt_fg = f.Get(str(bin[i])+"_LeadingJet_Forward_Gluon_pt")
    pt_cq = f.Get(str(bin[i])+"_LeadingJet_Central_Quark_pt")
    pt_cg = f.Get(str(bin[i])+"_LeadingJet_Central_Gluon_pt")
    pt_co = f.Get(str(bin[i])+"_LeadingJet_Central_Other_pt")

    pt_500_fq.Add(pt_cq)
    pt_500_fq.Add(pt_cg)
    pt_500_fq.Add(pt_co)
    pt_500_fq.Add(pt_fg)

c = TCanvas("c","c",500,500)
gPad.SetLogy()
gStyle.SetOptStat(0)
c.SetGrid()
gStyle.SetGridStyle(2)
gStyle.SetGridColor(15)
pt_500_fq.GetXaxis().SetTitle("p_{T} (GeV)")
pt_500_fq.Draw("HIST")

myText(0.48,0.84,'#it{#bf{#scale[1.4]{#bf{ATLAS} Simulation Preliminary}}}')
myText(0.48,0.80,'#bf{#scale[1.2]{#sqrt{s}=13 TeV}}')
myText(0.48,0.76,'#bf{#scale[1.2]{Anti-K_{t} EM+JES R=0.4}}')
myText(0.48,0.72,'#bf{#scale[1.2]{Leading Jet p_{T} Spectrum, Sherpa}}')

c.Print("pt-sherpa.pdf")
