#include "Riostream.h"
#include "TH1.h"
#include "TChain.h"
#include "TString.h"
#include "TLegend.h"
#include "TTree.h"
#include "TPad.h"
#include "TLine.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TLatex.h"
#include <string.h> // used in another function within the same file
#include <fstream>
#include <sstream>
#include <iostream>
#include <cmath>
#include <math.h>
#include <map>
using namespace std;

void drawPTspectrum_pythia_a() {
	map<int, TH1*> histmap;
	map<int, TH1*>::iterator it = histmap.begin();
	
	int index_prev;
	int sample = 0;
	
    vector<float> xsec; //= {78100000000.0,78100000000.0,2430000000.0,26500000.0,255000.0,4550.0,258.0,16.2,0.625,0.0196,0.0012,0.0000423,0.00000104};
    vector<float> eff; //= {0.97536,0.024447,0.0098699,0.011663,0.013369,0.014529,0.0094734,0.011099,0.010156,0.012057,0.005894,0.0026734,0.00042898};

	TCanvas *c1 = new TCanvas("c1","c1",500,500);

	TH1 *hj0 = new TH1D("hj0","",60,0,5000);
	TH1 *hj1 = new TH1D("hj1","",60,0,5000);
	TH1 *hj2 = new TH1D("hj2","",60,0,5000);
	TH1 *hj3 = new TH1D("hj3","",60,0,5000);
	TH1 *hj4 = new TH1D("hj4","",60,0,5000);
	TH1 *hj5 = new TH1D("hj5","",60,0,5000);
	TH1 *hj6 = new TH1D("hj6","",60,0,5000);
	TH1 *hj7 = new TH1D("hj7","",60,0,5000);
	TH1 *hj8 = new TH1D("hj8","",60,0,5000);
	TH1 *hj9 = new TH1D("hj9","",60,0,5000);
	TH1 *hj10 = new TH1D("hj10","",60,0,5000);
	TH1 *hj11 = new TH1D("hj11","",60,0,5000);
	TH1 *hj12 = new TH1D("hj12","",60,0,5000);

	histmap[0] = hj0;
	histmap[1] = hj1;
	histmap[2] = hj2;
	histmap[3] = hj3;
	histmap[4] = hj4;
	histmap[5] = hj5;
	histmap[6] = hj6;
	histmap[7] = hj7;
	histmap[8] = hj8;
	histmap[9] = hj9;
	histmap[10] = hj10;
	histmap[11] = hj11;
	histmap[12] = hj12;

	string root_lists = "/eos/user/e/esaraiva/dijet-pythia/dijet-pythia-bdt.txt";
	string sLine="";
	ifstream infile;
	infile.open(root_lists.c_str());//Data());

	while(getline(infile,sLine))  {
		TFile f2(sLine.c_str());

		cout << sLine.c_str() << endl;

		TTree *t1 = (TTree*)f2.Get("AntiKt4EMPFlow_dijet_insitu");

		Bool_t pass_HLT_j400;
		UInt_t mcChannelNumber;
		Float_t j1_pT;
		Float_t j2_pT;
		Float_t weight;
		Float_t weight_pileup;
		Float_t pdfWeights[101];
		Float_t j1_eta;
		Float_t j2_eta;

		t1->SetBranchStatus("*",0);
		t1->SetBranchStatus("pass_HLT_j400",1);
		t1->SetBranchStatus("mcChannelNumber",1);
		t1->SetBranchStatus("j1_pT",1);
		t1->SetBranchStatus("j2_pT",1);
		t1->SetBranchStatus("j1_eta",1);
		t1->SetBranchStatus("j2_eta",1);
		t1->SetBranchStatus("weight",1);
		t1->SetBranchStatus("weight_pileup",1);
		t1->SetBranchStatus("pdfWeights",1);
		t1->SetBranchAddress("mcChannelNumber",&mcChannelNumber);
		t1->SetBranchAddress("j1_pT",&j1_pT);
		t1->SetBranchAddress("j2_pT",&j2_pT);
		t1->SetBranchAddress("pass_HLT_j400",&pass_HLT_j400);
		t1->SetBranchAddress("weight_pileup",&weight_pileup);
		t1->SetBranchAddress("weight",&weight);
		t1->SetBranchAddress("pdfWeights",&pdfWeights);
		
		t1->GetEntry(1);

		float mc_weight;
		int mc_mod = 0;
		float w;
		int entries;
		float efficiency;
		float xsection;
		int index;
		
		cout << mcChannelNumber << endl;

		mc_mod = mcChannelNumber % 10;
		index = (mcChannelNumber % 100);
		if(index > 12) {
		    index = index-10;
		}
		
		if(index == 0 && index_prev == 12) {
		    sample = sample + 1;
		}
		cout << sample << endl;
		
		if(sample == 0) { xsec = {78100000000.0,78100000000.0,2430000000.0,26500000.0,255000.0,4550.0,258.0,16.2,0.625,0.0196,0.0012,0.0000423,0.00000104};
	    }
    	if(sample == 1) { xsec = {78100000000.0,78100000000.0,2430000000.0,26500000.0,255000.0,4550.0,258.0,16.2,0.625,0.0196,0.0012,0.0000423,0.00000104};  
    	}
	    if(sample == 2) { xsec = {78100000000.0,78100000000.0,2430000000.0,26500000.0,255000.0,4550.0,258.0,16.2,0.625,0.0196,0.0012,0.0000423,0.00000104};
	    }
	    vector<float> eff = {0.97536,0.024447,0.0098631,0.011658,0.013366,0.014526,0.0094734,0.011097,0.010156,0.012056,0.0058933,0.002673,0.00042889};

		
		TString mod = Form("AntiKt4EMPFlow_J%d_sumOfWeights",mc_mod);
		TH1 *h = (TH1F*)f2.Get(mod);
		mc_weight = h->GetBinContent(1);
		xsection = xsec.at(index);
		efficiency = eff.at(index);

		entries = t1->GetEntries();

		for (int i=0; i<entries; ++i) {
			t1->GetEvent(i);
			if(j1_pT > 0 && j1_pT < 5000) { // abs(j1_eta) < 2.1 && abs(j2_eta) < 2.1 &&  abs(j1_eta)/abs(j2_eta) <  1.5) {
		    	w = weight * efficiency * xsection / mc_weight;
    			TH1 *hist = histmap.find(index)->second;
				hist->Fill(j2_pT,w);
			}
		}
		index_prev = index;
	}

	TFile fout("dijet-pythia-pt.root","recreate");
	fout.cd();

	for(it = histmap.begin();it != histmap.end();it++) {
		cout << "writing histograms..." << endl;
		TH1 *hist = it->second;
		hist->Write();
	}

	fout.Write();
	fout.Close();
}
