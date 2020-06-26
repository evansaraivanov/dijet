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
#include <map>
using namespace std;

void drawPTspectrum_pythia_e() {
	map<int, TH1*> histmap;
	map<int, TH1*>::iterator it = histmap.begin();

	TCanvas *c1 = new TCanvas("c1","c1",500,500);

	TH1 *hj0 = new TH1D("hj0","",60,0,3000);
	TH1 *hj1 = new TH1D("hj1","",60,0,3000);
	TH1 *hj2 = new TH1D("hj2","",60,0,3000);
	TH1 *hj3 = new TH1D("hj3","",60,0,3000);
	TH1 *hj4 = new TH1D("hj4","",60,0,3000);
	TH1 *hj5 = new TH1D("hj5","",60,0,3000);
	TH1 *hj6 = new TH1D("hj6","",60,0,3000);
	TH1 *hj7 = new TH1D("hj7","",60,0,3000);
	TH1 *hj8 = new TH1D("hj8","",60,0,3000);
	TH1 *hj9 = new TH1D("hj9","",60,0,3000);

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

	cout << histmap[0] << endl;

	string root_lists = "/eos/user/e/esaraiva/dijet-pythia/dijet_pythia_e.txt";
	//string root_lists = "/eos/user/w/wasu/AQT_dijet_data_bdt/dijet_data_bdt.txt";
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

		float mc_weight;
		int mc_mod;
		float w;
		int entries;

		mc_mod = mcChannelNumber % 10;
		cout << mc_mod << endl << endl;
		TString mod = Form("AntiKt4EMPFlow_J%d_sumOfWeights",mc_mod);
		TH1 *h = (TH1F*)f2.Get(mod);
		mc_weight = h->GetBinContent(1);

		entries = t1->GetEntries();

		for (int i=0; i<entries; ++i) {
			t1->GetEvent(i);
//			cout << pass_HLT_j400 << "  ;  " << j1_pT << " ; " << abs(j1_eta) << " ; " << abs(j2_eta) << " ; " << abs(j1_eta)/abs(j2_eta) << endl;
			if(j1_pT > 0 && j1_pT < 3000) { // abs(j1_eta) < 2.1 && abs(j2_eta) < 2.1 &&  abs(j1_eta)/abs(j2_eta) <  1.5) {
		    	w = weight * mc_weight;
	    		cout << w << " ; " << "Filling Histogram..." << endl;
    			TH1 *hist = histmap.find(mc_mod)->second;
//				cout << j1_pT << endl;
				hist->Fill(j1_pT,w);
			}
		}
	}

	TFile fout("dijet-pythia-e-pt.root","recreate");
	fout.cd();

	for(it = histmap.begin();it != histmap.end();it++) {
		cout << "writing histograms..." << endl;
		TH1 *hist = it->second;
		hist->Write();
	}

	fout.Write();
	fout.Close();
}
