from ROOT import *

# This scripts read ttree as inputs and produce different histograms of distribution of variables in different pT range

#1.Select trigger "pass_HLT_j400
#2. select event :EMPFlowAntiKti4 jets with 1st pt :500-2000,   leading jet pt/sub-leading jet  pt < 1.5,  both jets |eta|<2.1    
#3.if the jets are MC, select leading and subleading reconstruction jets related to the truth jets. If jets are Data, skip this step .
#4.for each leading jet pT range, determinate forward or central assignment to 1st and 2nd jet, then categorise each jet as quark/gluon/other or  data
#5.fill hist with variables :Ntrk / BDT 
#


bins = [300, 400, 500, 600, 800, 1000, 1200, 1500, 2000]  #this bin range is for only dijet event
#bins = [0, 50, 100, 150, 200, 300, 400, 500, 600, 800, 1000, 1200, 1500, 2000]  #this bin range is for gammajet+dijet event
HistMap = {}
JetList = []

###### define functions
def GetHistBin(histname):
	if 'pt' in histname:
		return 60,0,2000
	elif 'eta' in histname:
		return 50,-2.5,2.5
	elif 'ntrk' in histname:
		return 60,0,60
	elif 'bdt' in histname:
		return 60,-0.8,0.7
	elif 'width' in histname:
		return 60,0.,0.4
	elif 'c1' in histname:
		return 60,0.,0.4

def FillTH1F(histname, var, w):
	if 'Data' in histname:
		w = 1
	if histname in HistMap:
		HistMap[histname].Fill(var, w)
	else:
		nbin,bmin,bmax = GetHistBin(histname)
		HistMap[histname]= TH1F(histname,"", nbin, bmin, bmax)
		HistMap[histname].Fill(var, w)


def FillHisto(prefix, jetlist, w):
	FillTH1F(prefix+"_ntrk", jetlist[0], w)
	FillTH1F(prefix+"_bdt", jetlist[1], w)
	FillTH1F(prefix+"_width", jetlist[2], w)
	FillTH1F(prefix+"_c1", jetlist[3], w)
	FillTH1F(prefix+"_pt", jetlist[4], w)
	FillTH1F(prefix+"_eta", jetlist[5], w)


def GetJetType(label):
	if label == -99:
		return "Data"
	elif label == 21:
		return "Gluon"
	elif label > 0 and label < 5:
		return "Quark"
	else:
		return "Other"


def FindBinIndex(jet_pt,ptbin):
	for i in range(len(ptbin)-1):
		if jet_pt >= ptbin[i] and jet_pt < ptbin[i+1]:
			return ptbin[i]

	print "error: jet pT ",jet_pt,"outside the bin range"
	return -1


######## read and excute TTree from root file 
finput = TFile.Open("/eos/user/e/esaraiva/dijet-data-bdt/dijet_sherpa_bdt.root")
#finput = TFile.Open("/eos/user/e/esaraiva/dijet-data-bdt/dijet_data_bdt.root")
t1 = finput.Get("AntiKt4EMPFlow_dijet_insitu")

for i in t1:
	if i.pass_HLT_j400 == 1 :#and i.j1_is_truth_jet and i.j2_is_truth_jet:
		if i.j1_pT > 500 and i.j1_pT < 2000 and abs(i.j1_eta) < 2.1 and abs(i.j2_eta) < 2.1 and i.j1_pT/i.j2_pT < 1.5:
			pTbin1 = FindBinIndex(i.j1_pT, bins)
			pTbin2 = FindBinIndex(i.j2_pT, bins)

			JetList = [[i.j1_NumTrkPt500, i.j1_bdt_resp, i.j1_trackWidth, i.j1_trackC1, i.j1_pT, i.j1_eta],[i.j2_NumTrkPt500,i.j2_bdt_resp, i.j2_trackWidth, i.j2_trackC1, i.j2_pT, i.j2_eta]] # JetList[0] for 1st jet, JetList[1] for 2nd jet

			label1 = GetJetType(i.j1_partonLabel)
			label2 = GetJetType(i.j2_partonLabel)

			eta1 = "Central"
			eta2 = "Forward"
			if abs(i.j1_eta) > abs(i.j2_eta):
				eta1 = "Forward"
				eta2 = "Central"

			weight_all = i.weight*i.weight_ptslice*i.pdfWeights[0]  #i.pdfWeights[0] is nominal
			FillHisto(str(pTbin1)+"_LeadingJet_"+eta1+"_"+label1, JetList[0], weight_all)
			FillHisto(str(pTbin2)+"_SubJet_"+eta2+"_"+label2, JetList[1], weight_all)


#foutput = TFile("dijet-data-py.root","recreate")
foutput = TFile("dijet-sherpa-py.root","recreate")
for hist in HistMap.values():
	#for i in range(len(bins)):
		#if str(bins[i]) in HistMap.keys():
		#	td = foutput.mkdir("pT: "+str(bins[i])+"-"+str(bins[i+1]))
		#	td.cd()
	hist.Write()

foutput.Write()
foutput.Close()
