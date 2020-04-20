from ROOT import *
import numpy as np

var = ["ntrk","width","c1","bdt"]
varmc = TFile("../root-files/dijet_sherpa_py.root")

bin = [300,400,500,600,800,1000,1200,1500,2000]

def myText(x,y,text, color=1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass

for i in range(2,8):
    higherGraph = [] #will hold list of plot x and y variabls in pairs for each analysis variable.
    lowerGraph = []

    for k in range(0,4):
        var1 = var[k] #iterate through variables

        higherQuark = varmc.Get(str(bin[i])+"_LeadingJet_Forward_Quark_"+var1+";1")
        lowerQuark = varmc.Get(str(bin[i])+"_LeadingJet_Central_Quark_"+var1+";1")

        higherGluon = varmc.Get(str(bin[i])+"_LeadingJet_Forward_Gluon_"+var1+";1")
        lowerGluon = varmc.Get(str(bin[i])+"_LeadingJet_Central_Gluon_"+var1+";1")

        #Normalize histograms
        if(higherQuark.Integral() != 0):
            higherQuark.Scale(1./higherQuark.Integral())
        if(lowerQuark.Integral() != 0):
            lowerQuark.Scale(1./lowerQuark.Integral())
        if(higherGluon.Integral() != 0):
            higherGluon.Scale(1./higherGluon.Integral())
        if(lowerGluon.Integral() != 0):
            lowerGluon.Scale(1./lowerGluon.Integral())

        x = np.empty(60)
        y = np.empty(60)
        u = np.empty(60)
        v = np.empty(60)

        for j in range(60):
            x[j] = (higherQuark.Integral(0,j))
            y[j] = (1. - higherGluon.Integral(0,j))
            u[j] = (lowerQuark.Integral(0,j))
            v[j] = (1. - lowerGluon.Integral(0,j))

        higherGraph.append(x)
        higherGraph.append(y)
        lowerGraph.append(u)
        lowerGraph.append(v)

#        print("made graph for "+var1)

    a = np.array([0.0000001,0.9999999])
    b = np.array([0.9999999,0.0000001])

    c1 = TCanvas("c1","c1",500,500)
    c1.SetGrid()

    gr1 = TGraph(60,higherGraph[0],higherGraph[1])
    gr2 = TGraph(60,higherGraph[2],higherGraph[3])
    gr3 = TGraph(60,higherGraph[4],higherGraph[5])
    gr4 = TGraph(60,higherGraph[6],higherGraph[7])
    gr5 = TGraph(2,a,b)

    gr1.SetLineColor(8)
    gr2.SetLineColor(6)
    gr3.SetLineColor(4)
    gr4.SetLineColor(2)
    gr5.SetLineStyle(2)

    gr5.GetXaxis().SetTitle("Quark Efficiency")
    gr5.GetYaxis().SetTitle("Gluon Rejection")

    gr5.GetXaxis().SetLimits(0.,1.)
    gr5.SetMinimum(0.)
    gr5.SetMaximum(1.)

    gPad.SetTickx()
    gPad.SetTicky()
    gStyle.SetGridStyle(2)
    gStyle.SetGridColor(15)
    gr5.SetLineStyle(2)

    leg1 = TLegend(0.16,0.42,0.35,0.6)
    leg1.SetBorderSize(0)
    leg1.SetFillStyle(0)
    leg1.AddEntry(gr1,"N_{trk}","L")
    leg1.AddEntry(gr2,"Track width","L")
    leg1.AddEntry(gr3,"C1","L")
    leg1.AddEntry(gr4,"qg-BDT","L")

    gr5.SetTitle("")

    gr5.Draw("AL")
    gr1.Draw("C same")
    gr2.Draw("C same")
    gr3.Draw("C same")
    gr4.Draw("C same")
    leg1.Draw("same")

    myText(0.13,0.30,'#it{#bf{#scale[1.4]{#bf{ATLAS} Simulation Preliminary}}}')
    myText(0.13,0.26,'#bf{#scale[1.2]{#sqrt{s}=13 GeV}}')
    myText(0.13,0.22,'#bf{#scale[1.2]{Anti-K_{t} EM+JES R=0.4}}')
    myText(0.13,0.18,'#bf{#scale[1.2]{|\eta|<2.1}}')
    myText(0.13,0.14,'#bf{#scale[1.3]{'+str(bin[i])+' < p_{T} < '+str(bin[i+1])+' GeV}}')

    c1.Print("./all-vars/"+str(bin[i])+"-"+str(bin[i+1])+"-higher.pdf")

    c1 = TCanvas("c1","c1",500,500)
    c1.SetGrid()

    gr1 = TGraph(60,lowerGraph[0],lowerGraph[1])
    gr2 = TGraph(60,lowerGraph[2],lowerGraph[3])
    gr3 = TGraph(60,lowerGraph[4],lowerGraph[5])
    gr4 = TGraph(60,lowerGraph[6],lowerGraph[7])
    gr5 = TGraph(2,a,b)

    gr5.SetTitle("")

    gr1.SetLineColor(8)
    gr2.SetLineColor(6)
    gr3.SetLineColor(4)
    gr4.SetLineColor(2)
    gr5.SetLineStyle(2)

    gr5.GetXaxis().SetTitle("Quark Efficiency")
    gr5.GetYaxis().SetTitle("Gluon Rejection")

    gr5.GetXaxis().SetLimits(0.,1.)
    gr5.SetMinimum(0.)
    gr5.SetMaximum(1.)

    gPad.SetTickx()
    gPad.SetTicky()
    gStyle.SetGridStyle(2)
    gStyle.SetGridColor(15)

    leg1 = TLegend(0.16,0.42,0.35,0.6)
    leg1.SetBorderSize(0)
    leg1.SetFillStyle(0)
    leg1.AddEntry(gr1,"N_{trk}","L")
    leg1.AddEntry(gr2,"Track width","L")
    leg1.AddEntry(gr3,"C1","L")
    leg1.AddEntry(gr4,"qg-BDT","L")

    gr5.Draw("AL")
    gr1.Draw("C same")
    gr2.Draw("C same")
    gr3.Draw("C same")
    gr4.Draw("C same")
    leg1.Draw("same")

    myText(0.13,0.30,'#it{#bf{#scale[1.4]{#bf{ATLAS} Simulation Preliminary}}}')
    myText(0.13,0.26,'#bf{#scale[1.2]{#sqrt{s}=13 GeV}}')
    myText(0.13,0.22,'#bf{#scale[1.2]{Anti-K_{t} EM+JES R=0.4}}')
    myText(0.13,0.18,'#bf{#scale[1.2]{|\eta|<2.1}}')
    myText(0.13,0.14,'#bf{#scale[1.3]{'+str(bin[i])+' < p_{T} < '+str(bin[i+1])+' GeV}}')

    c1.Print("./all-vars/"+str(bin[i])+"-"+str(bin[i+1])+"-lower.pdf")
