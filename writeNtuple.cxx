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

void writeNtuple() {
    TFile fout("dijet-pythia-bdt.root","recreate");
    
    int sample = 0;
    int index_prev = 0;
    vector<float> xsec;
    int total_entries = 0;
    	
	UInt_t mcChannelNumber;
	Bool_t pass_HLT_j400;
	Bool_t j1_is_truth_jet;
	Bool_t j2_is_truth_jet;
	Bool_t j3_is_truth_jet;
	Float_t j1_pT;
	Float_t j2_pT;
	Float_t j3_pT;
	Float_t j1_pT_truth;
	Float_t j2_pT_truth;
	Float_t j3_pT_truth;
	Float_t j1_eta;
	Float_t j2_eta;
	Float_t j3_eta;
	Float_t j1_eta_truth;
	Float_t j2_eta_truth;
	Float_t j3_eta_truth;
	Float_t weight;
	Float_t weight_ptslice;
	Float_t weight_pileup;
	Float_t pdfWeights[101];
	Float_t j2_bdt_resp;
	Float_t j1_bdt_resp;
	Float_t j3_bdt_resp;
	Float_t j1_trackWidth;
	Float_t j2_trackWidth;
	Float_t j3_trackWidth;
	Float_t j1_trackC1;
	Float_t j2_trackC1;
	Float_t j3_trackC1;
	Int_t j1_NumTrkPt500;
	Int_t j2_NumTrkPt500;
	Int_t j3_NumTrkPt500;
	Int_t j1_partonLabel;
	Int_t j2_partonLabel;
	Int_t j3_partonLabel;
	Float_t filter_efficiency;
	Float_t xsection;
	Float_t mc_weight;

	TTree *tree = new TTree("AntiKt4EMPFlow_dijet_insitu","");
	tree->Branch("mcChannelNumber",&mcChannelNumber);
	tree->Branch("j1_pT",&j1_pT);
	tree->Branch("j2_pT",&j2_pT);
	tree->Branch("j3_pT",&j2_pT);
	tree->Branch("j1_eta",&j1_eta);
	tree->Branch("j2_eta",&j2_eta);
	tree->Branch("j3_eta",&j2_eta);
	tree->Branch("j1_NumTrkPt500",&j1_NumTrkPt500);
	tree->Branch("j2_NumTrkPt500",&j2_NumTrkPt500);
	tree->Branch("j3_NumTrkPt500",&j2_NumTrkPt500);
	tree->Branch("j1_trackC1",&j1_trackC1);
	tree->Branch("j2_trackC1",&j2_trackC1);
	tree->Branch("j3_trackC1",&j2_trackC1);
	tree->Branch("j1_trackWidth",&j1_trackWidth);
	tree->Branch("j2_trackWidth",&j2_trackWidth);
	tree->Branch("j3_trackWidth",&j2_trackWidth);
	tree->Branch("j1_bdt_resp",&j1_bdt_resp);
	tree->Branch("j2_bdt_resp",&j2_bdt_resp);
	tree->Branch("j3_bdt_resp",&j2_bdt_resp);
	tree->Branch("j1_partonLabel",&j1_partonLabel);
	tree->Branch("j2_partonLabel",&j2_partonLabel);
	tree->Branch("j3_partonLabel",&j2_partonLabel);
	tree->Branch("pass_HLT_j400",&pass_HLT_j400);
	tree->Branch("weight_pileup",&weight_pileup);
	tree->Branch("weight",&weight);
	tree->Branch("pdfWeights",&pdfWeights);
	tree->Branch("weight_ptslice",&weight_ptslice);
	tree->Branch("filter_efficiency",&filter_efficiency);
	tree->Branch("xsection",&xsection);
	tree->Branch("mc_weight", &mc_weight);

	string root_lists = "/eos/user/e/esaraiva/dijet-pythia/dijet-pythia-bdt.txt";
	string sLine="";
	ifstream infile;
	infile.open(root_lists.c_str());//Data());

	while(getline(infile,sLine)) {
		TFile f2(sLine.c_str());

		cout << sLine.c_str() << endl;

		TTree *t1 = (TTree*)f2.Get("AntiKt4EMPFlow_dijet_insitu");

		t1->SetBranchStatus("*",0);
		t1->SetBranchStatus("mcChannelNumber",1);
		t1->SetBranchStatus("pass_HLT_j400",1);
		t1->SetBranchStatus("j1_pT",1);
		t1->SetBranchStatus("j2_pT",1);
		t1->SetBranchStatus("j3_pT",1);
		t1->SetBranchStatus("j1_eta",1);
		t1->SetBranchStatus("j2_eta",1);
		t1->SetBranchStatus("j3_eta",1);
		t1->SetBranchStatus("weight_ptslice",1);
		t1->SetBranchStatus("weight",1);
		t1->SetBranchStatus("weight_pileup",1);
		t1->SetBranchStatus("pdfWeights",1);
		t1->SetBranchStatus("j1_NumTrkPt500",1);
		t1->SetBranchStatus("j2_NumTrkPt500",1);
		t1->SetBranchStatus("j3_NumTrkPt500",1);
		t1->SetBranchStatus("j1_trackWidth",1);
		t1->SetBranchStatus("j2_trackWidth",1);
		t1->SetBranchStatus("j3_trackWidth",1);
		t1->SetBranchStatus("j1_trackC1",1);
		t1->SetBranchStatus("j2_trackC1",1);
		t1->SetBranchStatus("j3_trackC1",1);
		t1->SetBranchStatus("j1_bdt_resp",1);
		t1->SetBranchStatus("j2_bdt_resp",1);
		t1->SetBranchStatus("j3_bdt_resp",1);
		t1->SetBranchStatus("j1_partonLabel",1);
		t1->SetBranchStatus("j2_partonLabel",1);
		t1->SetBranchStatus("j3_partonLabel",1);

		t1->SetBranchAddress("mcChannelNumber",&mcChannelNumber);
		t1->SetBranchAddress("j1_pT",&j1_pT);
		t1->SetBranchAddress("j2_pT",&j2_pT);
		t1->SetBranchAddress("j3_pT",&j2_pT);
		t1->SetBranchAddress("j1_eta",&j1_eta);
		t1->SetBranchAddress("j2_eta",&j2_eta);
		t1->SetBranchAddress("j3_eta",&j2_eta);
		t1->SetBranchAddress("j1_NumTrkPt500",&j1_NumTrkPt500);
		t1->SetBranchAddress("j2_NumTrkPt500",&j2_NumTrkPt500);
		t1->SetBranchAddress("j3_NumTrkPt500",&j2_NumTrkPt500);
		t1->SetBranchAddress("j1_trackC1",&j1_trackC1);
		t1->SetBranchAddress("j2_trackC1",&j2_trackC1);
		t1->SetBranchAddress("j3_trackC1",&j2_trackC1);
		t1->SetBranchAddress("j1_trackWidth",&j1_trackWidth);
		t1->SetBranchAddress("j2_trackWidth",&j2_trackWidth);
		t1->SetBranchAddress("j3_trackWidth",&j2_trackWidth);
		t1->SetBranchAddress("j1_bdt_resp",&j1_bdt_resp);
		t1->SetBranchAddress("j2_bdt_resp",&j2_bdt_resp);
		t1->SetBranchAddress("j3_bdt_resp",&j2_bdt_resp);
		t1->SetBranchAddress("j1_partonLabel",&j1_partonLabel);
		t1->SetBranchAddress("j2_partonLabel",&j2_partonLabel);
		t1->SetBranchAddress("j3_partonLabel",&j2_partonLabel);
		t1->SetBranchAddress("pass_HLT_j400",&pass_HLT_j400);
		t1->SetBranchAddress("weight_pileup",&weight_pileup);
		t1->SetBranchAddress("weight",&weight);
		t1->SetBranchAddress("pdfWeights",&pdfWeights);
		t1->SetBranchAddress("weight_ptslice",&weight_ptslice);

		t1->GetEntry(1);

		int mc_mod = 0;
		float w;
		int entries;
		float efficiency;
		float xsection;
		int index;

		mc_mod = mcChannelNumber % 10;
		index = (mcChannelNumber % 100);
		
		while(index > 12) {
		    index = index - 10;
		}
		
		//cout << index << endl;
		
		if(index == 0 && index_prev == 12) {
		    sample = sample + 1;
		}
		//cout << sample << endl;
		
		if(sample == 0) { xsec = {78100000000.0,78100000000.0,2430000000.0,26500000.0,255000.0,4550.0,258.0,16.2,0.625,0.0196,0.0012,0.0000423,0.00000104};
	    }
    	if(sample == 1) { xsec = {78100000000.0,78100000000.0,2430000000.0,26500000.0,255000.0,4550.0,258.0,16.2,0.625,0.0196,0.00120,0.0000423,0.00000104};  
    	}
	    if(sample == 2) { xsec = {780500000000.0,780500000000.0,24330000000.0,26450000.0,254610.0,4553.0,257.540,16.215,0.625060,0.019639,0.001196,0.00004263,0.000001037};
	    }
	    vector<float> eff = {0.97536,0.024447,0.0098699,0.011663,0.013369,0.014529,0.0094734,0.011099,0.010156,0.012057,0.005894,0.0026734,0.00042898};

		TString mod = Form("AntiKt4EMPFlow_J%d_sumOfWeights",mc_mod);
		TH1 *h = (TH1F*)f2.Get(mod);
		mc_weight = h->GetBinContent(1);
		xsection = xsec.at(index);
		filter_efficiency = eff.at(index);

		entries = t1->GetEntries();
		total_entries += entries;
		cout << total_entries << endl;

        for(int i=0; i<entries; ++i) {
            t1->GetEntry(i);
            if(j1_pT > 500 && j1_pT < 2000 && abs(j1_eta) < 2.1 && abs(j2_eta) < 2.1 and j1_pT/j2_pT < 1.5 && pass_HLT_j400 == 1) { cout << "Event that should pass in ReadingTree" << " " << j1_eta << " " << j2_eta << " " << j1_pT/j2_pT << endl;
            }
            tree->Fill();
        }
		cout << total_entries << endl;
		index_prev = index;
	}
	fout.cd();
	tree->Write();
	fout.Write();
	fout.Close();
}
