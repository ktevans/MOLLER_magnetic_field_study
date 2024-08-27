// Simple example macro for reroot analysis of remoll simulations for
MOLLER
//
//  Need to use reroot (CERN's root compiled with special remoll
libraries,
//  or root when you have linked to ibremoll.so, i.e. by a command
like
//    setenv LD_PRELOAD build/libremoll.so
//   needs to have a subdirectory "images"  defined for the images to
go to
//
// Run using (for example):
//   build/reroot -l -q 'scripts/PlottingExample.C(“remollout.root")'
//
//  Can put multiple root files in argument, and they will be chained
together.
//
//  Includes superimposed 2D histograms with legends.
#include <TF1.h>
void PlottingExample(const TString& files)
{
  // Allow Tree to use the root files you call
  TChain* T = new TChain("T");
  T->Add(files);
  // Define variables that we will loop over later
  Double_t rate = 0;
  std::vector<remollEventParticle_t>* parts = 0;
  std::vector<remollGenericDetectorHit_t>* hits = 0;
  // Define some branches of the Tree (which is "T")
  T->SetBranchAddress("rate", &rate);
  T->SetBranchAddress("hit", &hits);
  T->SetBranchAddress("part", &parts);
// What does this line do?
gROOT -> SetBatch(kTRUE);
//Histogram skeletons:
//TH1* h1 = new TH1I("h1", "h1 title", 100, 0.0, 4.0);
   //[1D hist]* [name] = new ["TH1I" means one integer per bin]
("name", "title of hist", [# of bins], [x_min], [x_max]);
//TH2* h2 = new TH2F("h2", "h2 title", 40, 0.0, 2.0, 30, -1.5, 3.5);
 
   //[2D hist]* [name] = new ["TH2F" means one float per bin]("name",
"title of hist", [# of x bins], [x_min], [x_max], [# of y bins],
[y_min], [y_max]);
//Could also use TH(1/2)C for one byte per bin, TH(1/2)S for one short
per bin, or TH(1/2)D for one double per bin.
//Here is me defining histograms and setting the axis titles:
//Main detector histograms
TH2F *det28_prim_xy = new TH2F("det28_prim_xy","Detector 28 primary
electron hits x vs y ",40,-2000,2000,40,-2000,2000);
det28_prim_xy -> GetXaxis() -> SetTitle("x position of hits [mm]");
det28_prim_xy -> GetYaxis() -> SetTitle("y position of hits [mm]");
TH2F* main_hole1 = new TH2F("main_hole1", "Detector 28 Primary Hit
With Hole 1", 1000,-2000,2000,1000,-2000,2000);
main_hole1->GetXaxis()->SetTitle("Position in X");
main_hole1->GetYaxis()->SetTitle("Position in Y");
main_hole1->SetMarkerColor(kBlue);
TH2F* main_hole2 = new TH2F("main_hole2", "Detector 28 Primary Hit
With Hole 2", 1000,-2000,2000,1000,-2000,2000);
main_hole2->GetXaxis()->SetTitle("Position in X");
main_hole2->GetYaxis()->SetTitle("Position in Y");
main_hole2->SetMarkerColor(kRed);
TH2F* main_hole3 = new TH2F("main_hole3", "Detector 28 Primary Hit
With Hole 3", 1000,-2000,2000,1000,-2000,2000);
main_hole3->GetXaxis()->SetTitle("Position in X");
main_hole3->GetYaxis()->SetTitle("Position in Y");
main_hole3->SetMarkerColor(kGreen);
//Energy histograms
TH2F* maindet_energy_500_below = new
TH2F("maindet_2D_energy_500_below","Detector 28  primary hits with
energy below 500",1000,-2000,2000,1000,-2000,2000);
maindet_energy_500_below->GetXaxis()->SetTitle("Position in X");
maindet_energy_500_below->GetYaxis()->SetTitle("Position in Y");
 maindet_energy_500_below->SetMarkerColor(kBlue);
TH2F* maindet_energy_500_above = new
TH2F("maindet_2D_energy_500_above","Detector 28  primary hits with
energy above 500",1000,-2000,2000,1000,-2000,2000);
maindet_energy_500_above->GetXaxis()->SetTitle("Position in X");
maindet_energy_500_above->GetYaxis()->SetTitle("Position in Y");
 maindet_energy_500_above->SetMarkerColor(kRed);
 
  //These are dummy histograms that I will use to help make the Legends
later. They are filled with the colors that I want to grab.
 auto h1color = new TH1F("h1color","TLegend help",1,-1,1);
 h1color->FillRandom("gaus",3);
 h1color->SetFillColor(kBlue);
 auto h2color = new TH1F("h2color","TLegend help",1,-1,1);
 h2color->FillRandom("gaus",3);
 h2color->SetFillColor(kRed);
 auto h3color = new TH1F("h3color","TLegend help",1,-1,1);
 h3color->FillRandom("gaus",3);
 h3color->SetFillColor(kGreen);
// define logical flag for each hole
bool hole_1 = false;
bool hole_2 = false;
bool hole_3 = false;
  // Loop over all events
  for (size_t iev = 0; iev < T->GetEntries(); iev++) {
    T->GetEntry(iev);
    hole_1 = false;
    hole_2 = false;
    hole_3 = false;
    // Process hits: loop over all the hits in this event
    for (size_t ihit = 0; ihit < hits->size(); ihit++) {
      remollGenericDetectorHit_t hit = hits->at(ihit);
      //only plot primary electrons (trid = 1 or 2) hitting the main
detector (28)
      if ((hit.det == 28 && hit.trid == 1) || (hit.det == 28 &&
hit.trid == 2)) {
        det28_prim_xy -> Fill(hit.x,hit.y,rate); //"rate" weights the
histogram properly
          if(hit.e>500) {
              maindet_energy_500_above -> Fill(hit.x,hit.y,rate);
          }
          if(hit.e<500) {
              maindet_energy_500_below -> Fill(hit.x,hit.y,rate);
          }

}
      //test if primary electrons went through sieve holes. Detectors
1001, 1002, and 1003 are on each set of holes
      if ((hit.det == 1001 && hit.trid == 1) || (hit.det == 1001 &&
hit.trid == 2)) {
          hole_1 = true;
      }
      if ((hit.det == 1002 && hit.trid == 1) || (hit.det == 1002 &&
hit.trid == 2)) {
          hole_2 = true;
      }
      if ((hit.det == 1003 && hit.trid == 1) || (hit.det == 1003 &&
hit.trid == 2)) {
          hole_3 = true;
      }
    }  // end loop over hits
    // Process hits again and separate them by which hole the primary
electrons went through
    for (size_t ihit = 0; ihit < hits->size(); ihit++) {
      remollGenericDetectorHit_t hit = hits->at(ihit);
      if((hit.det == 28 && hole_1 && hit.trid == 1) || (hit.det == 28
&& hole_1 && hit.trid == 2)) {
          main_hole1 -> Fill(hit.x,hit.y,rate);
      }
      if((hit.det == 28 && hole_2 && hit.trid == 1) || (hit.det == 28
&& hole_2 && hit.trid == 2)) {
          main_hole2 -> Fill(hit.x,hit.y,rate);
      }
      if((hit.det == 28 && hole_3 && hit.trid == 1) || (hit.det == 28
&& hole_3 && hit.trid == 2)) {
          main_hole3 -> Fill(hit.x,hit.y,rate);
      }
    }  // end 2nd loop over hits
  }    //end loop over events
//--------------------------------------------------------------------
--
  // Draw and save the histograms
  TCanvas *c1 = new TCanvas("c1","Primary Electron Energies at Main
Detector",100,100,500,500);
 
  //Get rid of automatic title:
  gStyle->SetOptTitle(0);
  maindet_energy_500_below->Draw();
  //Superimpose the second energy histogram using "SAMES". "SAME" can
be used as well, but it will not redraw the statistics box.
  maindet_energy_500_above->Draw("SAMES");
  //Make test for new title. Coordinates are NDC (x_min, y_min, x_max,
y_max).
  auto titl = new TPaveLabel(0.1,0.92,0.8,1.0,"Primary Electron
Energies at Main Detector","brNDC");
  titl->Draw();
  //You have to update the canvas so that in the next line when you
call "stats", it doesn't return a null.
  gPad->Update();
  //Now, you can place each stat box where you want it. Here I am just
moving them in the Y direction, but you could make them wider too. The
histogram is plotted between (0.1,0.1) and (0.9,0.9) in NDC. (0,0) is
the bottom left of the canvas, and (1,1) is the top right.
  TPaveStats *s1 = (TPaveStats*)maindet_energy_500_below-
>GetListOfFunctions()->FindObject("stats");
  s1->SetY1NDC(0.9); //starting y position
  s1->SetY2NDC(0.6); //ending y position
  TPaveStats *s2 = (TPaveStats*)maindet_energy_500_above-
>GetListOfFunctions()->FindObject("stats");
  s2->SetY1NDC(0.6);
  s2->SetY2NDC(0.3);
  //Create and draw legend
  auto legend1 = new TLegend();
  //h(1/2/3)color is the variable used in the dummy histograms to
label the fill color for those histograms. The final spot in AddEntry,
"f", means we want this entry in the histogram to be a box filled with
the fill color. We can call the same color that the energy histogram
markers are from the dummy histograms.
  legend1->AddEntry(h1color,"Energies Below 500keV","f");
  legend1->AddEntry(h2color,"Energies Above 500keV","f");
 
  legend1->Draw();
  //This will save a .png file with your canvas on it.
  c1->SaveAs("images/PrimaryElectronEnergies.png");
  //Same process for primary hits
  TCanvas *c2 = new TCanvas("c2","Primary Electrons at Main Detector
Separated by hole",100,100,500,500);
  gStyle->SetOptTitle(0);
  main_hole1->Draw();
  main_hole2->Draw("SAMES");
  main_hole3->Draw("SAMES");
  auto titl2 = new TPaveLabel(0.1,0.92,0.9,1.0,"Primary Electron
Energies at Main Detector Separated by Sieve Hole","brNDC");
  titl2->Draw();
   gPad->Update();
  TPaveStats *st1 = (TPaveStats*)main_hole1->GetListOfFunctions()-
>FindObject("stats");
  st1->SetY1NDC(0.9);
  st1->SetY2NDC(0.65);
  TPaveStats *st2 = (TPaveStats*)main_hole2->GetListOfFunctions()-
>FindObject("stats");
  st2->SetY1NDC(0.65);
  st2->SetY2NDC(0.4);
  TPaveStats *st3 = (TPaveStats*)main_hole3->GetListOfFunctions()-
>FindObject("stats");
  st3->SetY1NDC(0.4);
  st3->SetY2NDC(0.15);
  auto legend = new TLegend ();
  legend->AddEntry(h1color,"Electrons from Hole 1","f");
  legend->AddEntry(h2color,"Electrons from Hole 2","f");
  legend->AddEntry(h3color,"Electrons from Hole 3","f");
  legend->Draw();
  c2->SaveAs("images/PrimaryElectronHoles.png");
}
 
